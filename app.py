import boto3
# from tkinter import *
import customtkinter

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
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
        self.top_menu_frame.grid(row=0, column=1, padx=5, pady=5, sticky="news")

        self.aws_id = customtkinter.CTkLabel(master=self.top_menu_frame, text="AWS Access Key ID")
        self.aws_id.grid(row=0, column=0, padx=5, pady=5)
        self.aws_id_entry = customtkinter.CTkEntry(self.top_menu_frame, width=150, height=35)
        self.aws_id_entry.grid(row=0, column=1, padx=5, pady=5)

        self.aws_key = customtkinter.CTkLabel(master=self.top_menu_frame, text="AWS Secret Access Key")
        self.aws_key.grid(row=0, column=2, padx=5, pady=5)
        self.aws_key_entry = customtkinter.CTkEntry(self.top_menu_frame, width=150, height=35, show="*")
        self.aws_key_entry.grid(row=0, column=3, padx=5, pady=5)

        self.aws_region = customtkinter.CTkLabel(master=self.top_menu_frame, text="Region")
        self.aws_region.grid(row=0, column=4, padx=5, pady=5)
        self.aws_region_entry = customtkinter.CTkEntry(self.top_menu_frame, width=150, height=35)
        self.aws_region_entry.grid(row=0, column=5, padx=5, pady=5)

        self.load_aws_creds = customtkinter.CTkButton(master=self.top_menu_frame, text="Load")
        self.load_aws_creds.grid(row=0, column=6, padx=5, pady=5)

        # Left frame
        self.left_menu_frame = customtkinter.CTkFrame(master=self, width=300)
        self.left_menu_frame.grid(row=1, column=0, padx=5, pady=5, sticky="news")

        self.get_templates_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Get Templates")
        self.get_templates_button.grid(row=0, column=0, padx=5, pady=5)

        self.update_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Update Template")
        self.update_template_button.grid(row=1, column=0, padx=5, pady=5)

        self.create_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Create Template")
        self.create_template_button.grid(row=2, column=0, padx=5, pady=5)

        self.load_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Load Template")
        self.load_template_button.grid(row=3, column=0, padx=5, pady=5)

        self.templates_list_optionmenu = customtkinter.CTkComboBox(master=self.left_menu_frame)
        self.templates_list_optionmenu.grid(row=4, column=0, padx=5, pady=5)

        # Right frame
        self.text_box_frame = customtkinter.CTkFrame(master=self, width=800)
        self.text_box_frame.grid(row=1, column=1, padx=5, pady=5, sticky="news")

        self.template_text = customtkinter.CTkTextbox(self.text_box_frame, width=1000, height=600)
        self.template_text.pack(expand=True, fill='both')



if __name__ == "__main__":
    app = App()
    app.mainloop()