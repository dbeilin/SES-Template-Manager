import boto3
import botocore.exceptions
import tkinter as tk
import customtkinter

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# AWS
ses = boto3.client('ses')

# Custom Tkinter
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("SES Template Manager")
        self.geometry(f"{1210}x{700}")
        icon = tk.PhotoImage(file = "app-icon.png")
        self.wm_iconphoto(True, icon)

        # Top frame (Template name and subject)
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

        # Left frame
        self.left_menu_frame = customtkinter.CTkFrame(master=self, width=300)
        self.left_menu_frame.grid(row=1, column=0, padx=5, pady=5, sticky="news")

        self.update_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Update Template", command=self.update_template)
        self.update_template_button.grid(row=0, column=0, padx=5, pady=5)

        self.create_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Create Template", command=self.create_template)
        self.create_template_button.grid(row=1, column=0, padx=5, pady=5)

        self.load_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Load Templates", command=self.get_templates)
        self.load_template_button.grid(row=2, column=0, padx=5, pady=5)

        self.combobox_var = customtkinter.StringVar()
        self.templates_list_cb = customtkinter.CTkComboBox(master=self.left_menu_frame, variable=self.combobox_var, values=[''], command=self.insert_template)
        self.templates_list_cb.grid(row=3, column=0, padx=5, pady=5)

        self.delete_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Delete Template", command=self.open_delete_window)
        self.delete_template_button.grid(row=4, column=0, padx=5, pady=5)

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

        # Bottom frame
        self.bottom_frame = customtkinter.CTkFrame(master=self, width=300, height=5)
        self.bottom_frame.grid_rowconfigure(0, weight=0)
        self.bottom_frame.grid(row=2, column=1, padx=7, pady=3, sticky="news")

        self.status_lbl = customtkinter.CTkLabel(master=self.bottom_frame, text="Idle", width=50)
        self.status_lbl.grid(row=0, column=0, padx=5, pady=3, sticky="news")

    def get_templates(self):
        '''
        Loads templates from SES service.
        Prints all templates and lists them
        inside the ComboBox.
        '''
        try:
            templates_list = []
            response = ses.list_templates()
            for template in response['TemplatesMetadata']:
                templates_list.append(template['Name'])

            print(f"Found {len(templates_list)} Templates:")
            for t in templates_list:
                print(t)

            self.status_lbl.configure(text=f"Found {len(templates_list)} Templates", text_color="green")
            self.templates_list_cb.configure(values=templates_list)
            return templates_list

        except Exception as e:
            print("Error getting templates:\n", e)
    
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

            '''
            Templates can be created without both the text and HTML parts filled in,
            we avoid the exception of not finding the appropriate key in case either
            the text or HTML part are missing.
            '''
            # Template text part
            if not 'TextPart' in response['Template'].keys():
                self.template_text.insert("0.0", "")
            else:
                self.template_text.insert("0.0", response['Template']['TextPart'])

            # Template HTML part
            if not 'HtmlPart' in response['Template'].keys():
                self.template_text_html.insert("0.0", "")
            else:
                self.template_text_html.insert("0.0", response['Template']['HtmlPart'])

            return response

        except Exception as e:
            self.status_lbl.configure(text=f"Error inserting data from template into widgets", text_color="red")
            print(e)

    def create_template(self):
        try:
            response = ses.create_template(
                Template={
                    'TemplateName': self.template_name.get(),
                    'SubjectPart': self.template_subject.get(),
                    'TextPart': self.template_text.get("0.0", customtkinter.END),
                    'HtmlPart': self.template_text_html.get("0.0", customtkinter.END)
                })

            self.get_templates() # Reload ComboBox values
            self.status_lbl.configure(text=f"Successfully created the template {self.template_name.get()}", text_color="green")
            return response

        except ses.exceptions.AlreadyExistsException:
            self.status_lbl.configure(text=f"A template with this name already exists", text_color="red")

        except ses.exceptions.InvalidTemplateException:
            self.status_lbl.configure(text=f"Invalid template exception", text_color="red")

        except Exception as e:
            self.status_lbl.configure(text=f"Error creating template", text_color="red")
            print(e)

    def update_template(self):
        try:
            response = ses.update_template(
                Template={
                    'TemplateName': self.template_name.get(),
                    'SubjectPart': self.template_subject.get(),
                    'TextPart': self.template_text.get("0.0", customtkinter.END),
                    'HtmlPart': self.template_text_html.get("0.0", customtkinter.END)
                })

            self.status_lbl.configure(text=f"Successfully updated the template {self.template_name.get()}", text_color="green")
            return response

        except ses.exceptions.TemplateDoesNotExistException:
            self.status_lbl.configure(text=f"Template does not exist", text_color="red")

        except Exception as e:
            self.status_lbl.configure(text=f"Error updating template", text_color="red")
            print(e)
    
    def delete_template(self):
        try:
            response = ses.delete_template(
                TemplateName=self.templates_list_cb.get()
            )
            self.get_templates() # Update ComboBox
            self.status_lbl.configure(text=f"Template {self.templates_list_cb.get()} was deleted successfully", text_color="green")
            return response

        except Exception as e:
            self.status_lbl.configure(text=f"Error deleting the template", text_color="red")
            print(e)
    
    def open_delete_window(self):
        '''
        Deletes a chosen template and opens another
        window to confirm the delete action.
        '''
        confirm_delete_window = customtkinter.CTkToplevel(self)
        confirm_delete_window.geometry("300x200")
        confirm_delete_window.title("Delete Template")

        # create label on CTkToplevel window
        confirm_delete_lbl = customtkinter.CTkLabel(confirm_delete_window, text=f"Are you sure you want to delete template {self.templates_list_cb.get()}?")
        confirm_delete_lbl.pack(side="top", fill="both", expand=True, padx=10, pady=10)

        confirm_delete_button = customtkinter.CTkButton(master=confirm_delete_window, text="Yes", command=self.delete_template, fg_color="red", hover_color="red")
        confirm_delete_button.pack(side="top", fill="both", padx=20, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()