import json
import os
import random
import string
import sys

# Append database path
CURDIR = os.path.dirname(os.path.abspath(__file__))
ROOTDIR = os.path.dirname(os.path.dirname(CURDIR))
DBPATH = os.path.join(ROOTDIR, "src", "database")
sys.path.append(DBPATH)
import DBInterface #pylint: disable=import-error

def main():
    # Create DBInterface object
    dbi = DBInterface.DBInterface()

    # Correct user info
    raw = dbi.login(user="test_name", pswd="test")
    data = json.loads(raw)
    print("correct_login: " + str(data) + "\n")

    # Incorrect username
    raw = dbi.login(user="incorrect_user", pswd="test")
    data = json.loads(raw)
    print("incorrect_login_username: " + str(data) + "\n")

    # Incorrect password
    raw = dbi.login(user="test_name", pswd="incorrect_pswd")
    data = json.loads(raw)
    print("incorrect_login_password: " + str(data) + "\n")

    # Username and email taken
    raw = dbi.register(user="test_name", email="test_email@gmail.com", pswd="temp")
    data = json.loads(raw)
    print("failed_register_username_email_taken: " + str(data) + "\n")

    # Username taken
    raw = dbi.register(user="test_name", email="new@gmail.com", pswd="temp")
    data = json.loads(raw)
    print("failed_register_username_taken: " + str(data) + "\n")

    # Email taken
    raw = dbi.register(user="new", email="test_email@gmail.com", pswd="temp")
    data = json.loads(raw)
    print("failed_register_email_taken: " + str(data) + "\n")

    # Good register
    user = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    email = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    pswd = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    raw = dbi.register(user=user, email=email , pswd=pswd)
    data = json.loads(raw)
    print("good_register: " + str(data) + "\n")

    # Login with new account
    raw = dbi.login(user=user, pswd=pswd)
    data = json.loads(raw)
    print("login_with_new_account: " + str(data) + "\n")
    iD = data['id']
    notif = data['notification']

    # Update with wrong password 
    new_user = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    raw = dbi.update_username(iD=iD, old_user=user, new_user=new_user, pswd="wrong")
    data = json.loads(raw)
    print("update_wrong_pass: " + str(data) + "\n")

    # Update username
    new_user = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    raw = dbi.update_username(iD=iD, old_user=user, new_user=new_user, pswd=pswd)
    data = json.loads(raw)
    print("update_username: " + str(data) + "\n")

    # Update email
    new_email = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    raw = dbi.update_email(iD=iD, old_email=email, new_email=new_email, pswd=pswd)
    data = json.loads(raw)
    print("update_email: " + str(data) + "\n")

    # Update password
    new_pswd = ''.join(random.choice(string.ascii_lowercase) for i in range(10))
    raw = dbi.update_password(iD=iD, old_pswd=pswd, new_pswd=new_pswd)
    data = json.loads(raw)
    print("update_password " + str(data) + "\n")

    # Switch notifcation
    raw = dbi.switch_notification(iD=iD, notification=(not notif))
    data = json.loads(raw)
    print("switch_notification " + str(data) + "\n")

    # Login with updated credentials.
    raw = dbi.login(user=new_user, pswd=new_pswd)
    data = json.loads(raw)
    print("login_updated: " + str(data) + "\n")

if __name__ == "__main__":
    main()
