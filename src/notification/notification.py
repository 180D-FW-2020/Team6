import os
import smtplib
import sqlite3
import sys
from email.message import EmailMessage
from datetime import datetime

CURPATH = os.path.dirname(os.path.abspath(__file__))
EMAILPATH = os.path.join(CURPATH, 'emails.txt')

_email = "nightlight.notifier@gmail.com"
_pass =  "qjhlwonnufdgvdss"

def notify(subject="Nightlight Notifier", content="Content"):
    if not os.path.exists(EMAILPATH):
        return
    
    f = open(EMAILPATH) 
    emails = f.readline().split(',')

    for to in emails:
        msg = EmailMessage()
        msg.set_content(content)
        msg["subject"] = subject
        msg["from"] = _email
        msg["to"] = to + ','

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(_email, _pass)

        try:
            server.send_message(msg)
        except:
            pass
    
    server.quit()