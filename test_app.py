import boto3
from tkinter import *
import customtkinter

###### AWS ######
ses = boto3.client('ses')

###### TK ######
app = customtkinter.CTk()
app.geometry("500x300")

###### Tkinter ######
optionmenu_var = customtkinter.StringVar(value="")  # set initial value

def optionmenu_callback(choice):
    print("optionmenu dropdown clicked:", choice)

combobox = customtkinter.CTkComboBox(master=app,
                                     values=["option 1", "option 2"],
                                     command=optionmenu_callback,
                                     variable=optionmenu_var)
combobox.pack(padx=20, pady=10)

def button_event():
    combobox.set(value='test')

button = customtkinter.CTkButton(master=app, text="CTkButton", command=button_event)
button.pack(padx=20, pady=10)

app.mainloop()