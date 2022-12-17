import tkinter as tk
import customtkinter
import template_functions.template_functions as f

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

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

        self.update_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Update Template", command=f.update_template)
        self.update_template_button.grid(row=0, column=0, padx=5, pady=5)

        self.create_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Create Template", command=f.create_template)
        self.create_template_button.grid(row=1, column=0, padx=5, pady=5)

        self.load_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Load Templates", command=f.get_templates)
        self.load_template_button.grid(row=2, column=0, padx=5, pady=5)

        self.combobox_var = customtkinter.StringVar()
        self.templates_list_cb = customtkinter.CTkComboBox(master=self.left_menu_frame, variable=self.combobox_var, values=[''], command=f.insert_template)
        self.templates_list_cb.grid(row=3, column=0, padx=5, pady=5)

        self.delete_template_button = customtkinter.CTkButton(master=self.left_menu_frame, text="Delete Template", command=f.open_delete_window)
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