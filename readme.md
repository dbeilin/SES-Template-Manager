![banner](https://i.imgur.com/iFbczhY.png)
# SES Template Manager

Recently I was working on sending emails using AWS SES. What I love about SES is the option to use templated emails, which allows to easily populate variables inside of the message.

I saw that the SES Console doesn't offer a web-UI for managing my templates, you have to use the CLI. While it was ok at first I quickly grew tired of updating or creating my templates that way, so I wrote a simple GUI app in Python to do just that.

# Table Of Contents
- [Prerequisites](#prerequisites)
- [How To Use](#how-to-use)
    - [Load Existing Templates](#load-existing-templates)
    - [Modifying Templates](#modifying-templates)
- [Additional Resources](#additional-resources-📚)
- [Notes](#notes)

---

## Prerequisites 
- Make sure you ran `aws configure` or whatever method you use to access your AWS account.
---
## How To Use
1. Clone the repo.
2. Run `pip install -r requirements.txt`
3. Run `python app.py`
![cli](https://i.imgur.com/WE9aGfV.png)

![main window](https://i.imgur.com/PW1UaHl.png)

### Load Existing Templates
Clicking on "Load Templates" will populate the ComboBox below it with your existing templates
![load templates example](https://i.imgur.com/kNIFzsq.png)

### Modifying Templates
When you choose a template from the menu, it will load the contents of both the text and HTML part of that template into the corresponding tab.
![insert template data](https://i.imgur.com/7p25p7O.png)

The actions are self-explanatory:
- Update the template by clicking on "Update Template".
- Create a new template by clicking on "Create Template".
- Delete the chosen template by clicking on "Delete Template".
---
## Additional Resources 📚
- GUI was built using [Custom Tkinter](https://github.com/TomSchimansky/CustomTkinter).
- Learn more about [SES Templating](https://docs.aws.amazon.com/ses/latest/dg/send-personalized-email-api.html).
- All the functions are using [Boto3 SES](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ses.html).
---
## Notes
This is just a hobby project as I keep learning Python 😊

I welcome feedback if you have any ideas to fix/improve this tool.
