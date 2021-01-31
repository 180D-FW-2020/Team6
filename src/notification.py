import os
import smtplib
import sqlite3
from email.message import EmailMessage
from datetime import datetime

if os.name == 'nt':
    DBPATH = "sql\\RPi.db"
else:
    DBPATH = "sql/RPi.db"

_email = "nightlight.notifier@gmail.com"
_pass =  "qjhlwonnufdgvdss"

db = sqlite3.connect(DBPATH)

def notify(subject, content):
    print("Pushing notification")
    msg = EmailMessage()
    msg.set_content(content)
    msg["subject"] = subject
    msg["from"] = _email
    msg["to"] = "robertrenzorudio@gmail.com"

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