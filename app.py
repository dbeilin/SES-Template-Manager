import boto3
import tkinter
import customtkinter

###### AWS ######
ses = boto3.client('ses')

###### Theme ######
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

###### Main ######
app = customtkinter.CTk()
app.geometry("1200x700")

###### Widgets ######

templates_list_widget = customtkinter.CTkOptionMenu(master=app)

button = customtkinter.CTkButton(master=app, text="CTkButton")
button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)

app.mainloop()