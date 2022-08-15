import boto3

client = boto3.client('ses')

def list_templates():
    templates_list = []

    try:
        templates = client.list_templates()
        for t in templates['TemplatesMetadata']:
            template_name = t['Name']
            templates_list.append(template_name)
        return templates_list
    
    except Exception as e:
        print("Wasn't able to get the list of templates", e)

def get_template_subject(template):
    try:
        template_response = client.get_template(TemplateName=template)
        template_subject = template_response.get('Template')['SubjectPart']

        return template_subject

    except Exception as e:
        print("Wasn't able to get the template subject", e)

def get_template_body(template):
    try:
        template_response = client.get_template(TemplateName=template)
        template_body = template_response.get('Template')['TextPart']

        return template_body

    except Exception as e:
        print("Wasn't able to get the template body", e)

def show_template(template):
    print("Subject:", get_template_subject(template))
    print("Body:", get_template_body(template))
