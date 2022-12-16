import boto3
import botocore.exceptions
# from tkinter import *
import customtkinter

customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

###### AWS ######
ses = boto3.client('ses')

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("SES Template Manager")
        self.geometry(f"{1200}x{700}")

        # Top frame
        self.top_menu_frame = customtkinter.CTkFrame(master=self, height=40)
        self.top_menu_frame.grid_rowconfigure(0, weight=0)
        self.top_menu_frame.grid_columnconfigure(1, weight=3)
        self.top_menu_frame.grid(row=0, column=1, padx=5, pady=5, sticky="news")

        self.template_name_lbl = customtkinter.CTkLabel(master=self.top_menu_frame, text="Template Name:", width=50)
        self.template_name_lbl.grid(row=0, column=0, padx=5, pady=5)
        self.template_name = customtkinter.CTkEntry(master=self.top_menu_frame, placeholder_text="Template Name", width=400)
        self.template_name.grid(row=0, column=1, padx=5, pady=5)

        self.template_subject_lbl = customtkinter.CTkLabel(master=self.top_menu_frame, text="Template Subject:", width=50)
        self.template_subject_lbl.grid(row=0, column=2, padx=5, pady=5)
        self.template_subject = customtkinter.CTkEntry(master=self.top_menu_frame, placeholder_text="Template Subject", width=400)
        self.template_subject.grid(row=0, column=3, padx=5, pady=5)

        # self.aws_id = customtkinter.CTkLabel(master=self.top_menu_frame, text="AWS Access Key ID")
        # self.aws_id.grid(row=0, column=0, padx=5, pady=5)
        # self.aws_id_entry = customtkinter.CTkEntry(self.top_menu_frame, width=150, height=35)
        # self.aws_id_entry.grid(row=0, column=1, padx=5, pady=5)

        # self.aws_key = customtkinter.CTkLabel(master=self.top_menu_frame, text="AWS Secret Access Key")
        # self.aws_key.grid(row=0, column=2, padx=5, pady=5)
        # self.aws_key_entry = customtkinter.CTkEntry(self.top_menu_frame, width=150, height=35, show="*")
        # self.aws_key_entry.grid(row=0, column=3, padx=5, pady=5)

        # self.aws_region = customtkinter.CTkLabel(master=self.top_menu_frame, text="Region")
        # self.aws_region.grid(row=0, column=4, padx=5, pady=5)
        # self.aws_region_entry = customtkinter.CTkEntry(self.top_menu_frame, width=150, height=35)
        # self.aws_region_entry.grid(row=0, column=5, padx=5, pady=5)

        # self.load_aws_creds = customtkinter.CTkButton(master=self.top_menu_frame, text="Load")
        # self.load_aws_creds.grid(row=0, column=6, padx=5, pady=5)

        # Left frame
        self.left_menu_frame = customtkinter.CTkFrame(master=self, width=300)
        self.left_menu_frame.grid(row=1, column=0, padx=5, pady=5, sticky="news")

        self.update_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Update Template", command=self.update_template)
        self.update_template_button.grid(row=0, column=0, padx=5, pady=5)

        self.create_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Create Template", command=self.create_template)
        self.create_template_button.grid(row=1, column=0, padx=5, pady=5)

        self.load_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Load Templates", command=self.get_templates)
        self.load_template_button.grid(row=2, column=0, padx=5, pady=5)

        combobox_var = customtkinter.StringVar()
        self.templates_list_cb = customtkinter.CTkComboBox(master=self.left_menu_frame, variable=combobox_var, state='readonly', values=[''], command=self.insert_template)
        self.templates_list_cb.grid(row=3, column=0, padx=5, pady=5)

        # Right frame (Tab View)
        self.tabView = customtkinter.CTkTabview(self, height=600, width=1025)
        self.tabView.add("Text")
        self.tabView.add("HTML")
        self.tabView.grid(row=1, column=1, padx=5, pady=5, sticky="news")
        self.tabView.tab("Text").grid_columnconfigure(0, weight=1)
        self.tabView.tab("HTML").grid_columnconfigure(0, weight=1)

        self.template_text = customtkinter.CTkTextbox(master=self.tabView.tab('Text'))
        self.template_text.pack(expand=True, fill='both')

        self.template_text_html = customtkinter.CTkTextbox(master=self.tabView.tab('HTML'))
        self.template_text_html.pack(expand=True, fill='both')
        
        # # Bottom frame
        # self.left_menu_frame = customtkinter.CTkFrame(master=self, height=20)
        # self.left_menu_frame.grid(row=2, column=1, padx=5, pady=5, sticky="news")
    
    def get_templates(self):
        '''
        Loads templates from SES service.
        Prints all templates and lists them
        inside the ComboBox.
        '''
        templates_list = []
        response = ses.list_templates()
        for template in response['TemplatesMetadata']:
            templates_list.append(template['Name'])

        print(f"Found {len(templates_list)} Templates:")
        for t in templates_list:
            print(t)

        self.templates_list_cb.configure(values=templates_list)
        return templates_list

    def insert_template(self, *args):
        '''
        Insert contents of chosen template to the text box
        both in HTML and Text (if exists).
        '''
        try:
            response = ses.get_template(TemplateName=self.templates_list_cb.get())

            # Always clear text when switching between templates
            self.template_text.delete("0.0", customtkinter.END)
            self.template_text_html.delete("0.0", customtkinter.END)
            self.template_subject.delete(0, customtkinter.END)
            self.template_name.delete(0, customtkinter.END)
            
            # Template name part
            self.template_name.insert(0, response['Template']['TemplateName'])

            # Teplate subject part
            self.template_subject.insert(0, response['Template']['SubjectPart'])

            # Template text part
            if not 'TextPart' in response['Template'].keys():
                self.template_text.insert("0.0", "Text part is null")
            else:
                self.template_text.insert("0.0", response['Template']['TextPart'])

            # Template HTML part
            if not 'HtmlPart' in response['Template'].keys():
                self.template_text_html.insert("0.0", "HTML part is null")
            else:
                self.template_text_html.insert("0.0", response['Template']['HtmlPart'])

            return response

        except Exception as e:
            print("Error inserting data from template into widgets:\n", e)

    def create_template(self):
        try:
            response = ses.create_template(
                Template={
                    'TemplateName': self.template_name.get(),
                    'SubjectPart': self.template_subject.get(),
                    'TextPart': self.template_text.get("0.0", customtkinter.END),
                    'HtmlPart': self.template_text_html.get("0.0", customtkinter.END)
                })
            print("Successfully created the template", self.template_name.get())
            self.get_templates()
            return response

        except ses.exceptions.AlreadyExistsException:
            print("A template with this name already exists")

        except ses.exceptions.InvalidTemplateException:
            print("Invalid template exception")

        except Exception as e:
            print("Error creating template:", e)

    def update_template(self):
        try:
            response = ses.update_template(
                Template={
                    'TemplateName': self.template_name.get(),
                    'SubjectPart': self.template_subject.get(),
                    'TextPart': self.template_text.get("0.0", customtkinter.END),
                    'HtmlPart': self.template_text_html.get("0.0", customtkinter.END)
                })

            print("Successfully updated the template", self.template_name.get())
            return response

        except ses.exceptions.TemplateDoesNotExistException:
            print("Template does not exist")

        except Exception as e:
            print("Error creating template:", e)

if __name__ == "__main__":
    app = App()
    app.mainloop()