import boto3
import tkinter
import customtkinter

###### AWS ######
ses = boto3.client('ses')


###### TK ######
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

app = customtkinter.CTk()
app.geometry("1200x700")

###### Functions ######
def get_templates():
    templates_list = []
    response = ses.list_templates()
    for template in response['TemplatesMetadata']:
        templates_list.append(template['Name'])

    return templates_list

###### Widgets ######
templates_list_combobox = customtkinter.CTkComboBox(master=app, values=get_templates())

button = customtkinter.CTkButton(master=app, text="CTkButton")
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

templates_list_combobox.pack()
button.pack()

app.mainloop()