import os
import smtplib
import sqlite3
import sys
from email.message import EmailMessage
from datetime import datetime

CURPATH = os.path.dirname(os.path.abspath(__file__))
DBPATH = os.path.join(CURPATH, "sql", "RPi.db")

def notify(subject, content):
    print("Pushing notification")
    # sqlite3
    db = sqlite3.connect(DBPATH)
    cursor = db.cursor()
    query = "SELECT * FROM email_info"
    receiver_query = "SELECT email FROM user WHERE alert=1"

    # RPi email
    _email, _pass = cursor.execute(query).fetchall()[0]

    receviers = [_to[0] for _to in cursor.execute(receiver_query)]
    to = ", ".join(receviers)
    
    if not to:
        # No email signed up for notification 
        # or all user turned off notification.
        return

    else:
        msg = EmailMessage()
        msg.set_content(content)
        msg["subject"] = subject
        msg["from"] = _email
        msg["to"] = to

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(_email, _pass)
        server.send_message(msg)
        
    db.close()
    server.quit()