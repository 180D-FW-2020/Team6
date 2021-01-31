import smtplib
import os
from email.message import EmailMessage
from datetime import datetime

if os.name == 'nt':
    EMAILPATH = "commands\\email.txt"
else:
    EMAILPATH = "commands/email.txt"

_email = "nightlight.notifier@gmail.com"
_pass =  "qjhlwonnufdgvdss"

def notify(subject, content):
    print("Pushing notification")
    msg = EmailMessage()
    msg.set_content(content)
    msg["subject"] = subject
    msg["from"] = _email

    with open(EMAILPATH, "r") as f:
        emails = f.readlines()

    to = ""
    for email in emails:
        to = to + email.strip("\n")
    
    msg["to"] = to

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(_email, _pass)
    server.send_message(msg)

    t = datetime.now()
    t = t.strftime("%Y-%M-%d %H:%M:%S")
    log = t + " " + subject + "\n"

    logf = open("notif.log", "a")
    logf.write(log)

    server.quit()
