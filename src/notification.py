import smtplib
from email.message import EmailMessage

_email = "" # sender email addr
_pass =  "" # sender email password

def notify(subject, content, to):
    print("Pushing notification")
    msg = EmailMessage()
    msg.set_content(content)
    msg["subject"] = subject
    msg["from"] = _email
    msg["to"] = to 
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(_email, _pass)
    server.send_message(msg)
    server.quit()
