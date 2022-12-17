import boto3
import botocore.exceptions
import customtkinter
import user_interface.ui

# AWS
ses = boto3.client('ses')

# App
app = user_interface.ui.App()

def get_templates(app):
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

        app.status_lbl.configure(text=f"Found {len(templates_list)} Templates", text_color="green")
        app.templates_list_cb.configure(values=templates_list)
        return templates_list

    except Exception as e:
        print("Error getting templates:\n", e)

def insert_template(app, *args):
    '''
    Insert contents of chosen template to the text box
    both in HTML and Text (if exists).
    '''
    try:
        
        response = ses.get_template(TemplateName=app.templates_list_cb.get())

        # Always clear text when switching between templates
        app.template_text.delete("0.0", customtkinter.END)
        app.template_text_html.delete("0.0", customtkinter.END)
        app.template_subject.delete(0, customtkinter.END)
        app.template_name.delete(0, customtkinter.END)
        
        # Template name part
        app.template_name.insert(0, response['Template']['TemplateName'])

        # Teplate subject part
        app.template_subject.insert(0, response['Template']['SubjectPart'])

        '''
        Templates can be created without both the text and HTML parts filled in,
        we avoid the exception of not finding the appropriate key in case either
        the text or HTML part are missing.
        '''
        # Template text part
        if not 'TextPart' in response['Template'].keys():
            app.template_text.insert("0.0", "")
        else:
            app.template_text.insert("0.0", response['Template']['TextPart'])

        # Template HTML part
        if not 'HtmlPart' in response['Template'].keys():
            app.template_text_html.insert("0.0", "")
        else:
            app.template_text_html.insert("0.0", response['Template']['HtmlPart'])

        return response

    except Exception as e:
        app.status_lbl.configure(text=f"Error inserting data from template into widgets", text_color="red")
        print(e)

def create_template(app):
    try:
        response = ses.create_template(
            Template={
                'TemplateName': app.template_name.get(),
                'SubjectPart': app.template_subject.get(),
                'TextPart': app.template_text.get("0.0", customtkinter.END),
                'HtmlPart': app.template_text_html.get("0.0", customtkinter.END)
            })

        app.get_templates() # Reload ComboBox values
        app.status_lbl.configure(text=f"Successfully created the template {app.template_name.get()}", text_color="green")
        return response

    except ses.exceptions.AlreadyExistsException:
        app.status_lbl.configure(text=f"A template with this name already exists", text_color="red")

    except ses.exceptions.InvalidTemplateException:
        app.status_lbl.configure(text=f"Invalid template exception", text_color="red")

    except Exception as e:
        app.status_lbl.configure(text=f"Error creating template", text_color="red")
        print(e)

def update_template(app):
    try:
        response = ses.update_template(
            Template={
                'TemplateName': app.template_name.get(),
                'SubjectPart': app.template_subject.get(),
                'TextPart': app.template_text.get("0.0", customtkinter.END),
                'HtmlPart': app.template_text_html.get("0.0", customtkinter.END)
            })

        app.status_lbl.configure(text=f"Successfully updated the template {app.template_name.get()}", text_color="green")
        return response

    except ses.exceptions.TemplateDoesNotExistException:
        app.status_lbl.configure(text=f"Template does not exist", text_color="red")

    except Exception as e:
        app.status_lbl.configure(text=f"Error updating template", text_color="red")
        print(e)

def delete_template(app):
    try:
        response = ses.delete_template(
            TemplateName=app.templates_list_cb.get()
        )
        app.get_templates() # Update ComboBox
        app.status_lbl.configure(text=f"Template {app.templates_list_cb.get()} was deleted successfully", text_color="green")
        return response

    except Exception as e:
        app.status_lbl.configure(text=f"Error deleting the template", text_color="red")
        print(e)

def open_delete_window(app):
    '''
    Deletes a chosen template and opens another
    window to confirm the delete action.
    '''
    confirm_delete_window = customtkinter.CTkToplevel(app)
    confirm_delete_window.geometry("400x200")
    confirm_delete_window.title("Delete Template")

    # create label on CTkToplevel window
    confirm_delete_lbl = customtkinter.CTkLabel(confirm_delete_window, text=f"Are you sure you want to delete template {app.templates_list_cb.get()}?")
    confirm_delete_lbl.pack(side="top", fill="both", expand=True, padx=10, pady=10)

    confirm_delete_button = customtkinter.CTkButton(master=confirm_delete_window, text="Yes", command=app.delete_template, fg_color="red", hover_color="red")
    confirm_delete_button.pack(side="top", fill="both", padx=20, pady=10)
