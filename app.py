import boto3
from tkinter import *
import customtkinter

###### AWS ######
ses = boto3.client('ses')

###### TK ######
app = customtkinter.CTk()
app.geometry("1200x700")
# app.maxsize(1200, 700)

###### Functions ######
def get_templates():
    templates_list = []
    response = ses.list_templates()
    for template in response['TemplatesMetadata']:
        templates_list.append(template['Name'])

    return templates_list

###### Tkinter ######
# Top frame
top_menu_frame = customtkinter.CTkFrame(master=app, height=40)
top_menu_frame.grid(row=0, column=1, padx=5, pady=5, sticky="news")

aws_id = customtkinter.CTkLabel(master=top_menu_frame, text="AWS Access Key ID")
aws_id.grid(row=0, column=0, padx=5, pady=5)
aws_id_entry = customtkinter.CTkEntry(top_menu_frame, width=150, height=35)
aws_id_entry.grid(row=0, column=1, padx=5, pady=5)

aws_key = customtkinter.CTkLabel(master=top_menu_frame, text="AWS Secret Access Key")
aws_key.grid(row=0, column=2, padx=5, pady=5)
aws_key_entry = customtkinter.CTkEntry(top_menu_frame, width=150, height=35, show="*")
aws_key_entry.grid(row=0, column=3, padx=5, pady=5)

aws_region = customtkinter.CTkLabel(master=top_menu_frame, text="Region")
aws_region.grid(row=0, column=4, padx=5, pady=5)
aws_region_entry = customtkinter.CTkEntry(top_menu_frame, width=150, height=35)
aws_region_entry.grid(row=0, column=5, padx=5, pady=5)

load_aws_creds = customtkinter.CTkButton(master=top_menu_frame, text="Load")
load_aws_creds.grid(row=0, column=6, padx=5, pady=5)

# Left frame
left_menu_frame = customtkinter.CTkFrame(master=app, width=300)
left_menu_frame.grid(row=1, column=0, padx=5, pady=5, sticky="news")

get_templates_button = customtkinter.CTkButton(master=left_menu_frame, text="Get Templates")
get_templates_button.grid(row=0, column=0, padx=5, pady=5)

update_template_button = customtkinter.CTkButton(master=left_menu_frame, text="Update Template")
update_template_button.grid(row=1, column=0, padx=5, pady=5)

create_template_button = customtkinter.CTkButton(master=left_menu_frame, text="Create Template")
create_template_button.grid(row=2, column=0, padx=5, pady=5)

load_template_button = customtkinter.CTkButton(master=left_menu_frame, text="Load Template", command=get_templates)
load_template_button.grid(row=3, column=0, padx=5, pady=5)

templates_list_optionmenu = customtkinter.CTkComboBox(master=left_menu_frame)
templates_list_optionmenu.grid(row=4, column=0, padx=5, pady=5)

# Right frame
text_box_frame = customtkinter.CTkFrame(master=app, width=800)
text_box_frame.grid(row=1, column=1, padx=5, pady=5, sticky="news")

template_text = customtkinter.CTkTextbox(text_box_frame, width=1000, height=600)
template_text.pack(expand=True, fill='both')

app.mainloop()