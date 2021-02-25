# Reference: https://www.simplifiedpython.net/python-gui-login/

from tkinter import *
import pub_cmd
import os
import json
import DBInterface

CURPATH = os.path.dirname(os.path.abspath(__file__))

# Designing Main(first) window
def main_account_screen():
    global main_screen
    main_screen = Tk()
    main_screen.geometry("300x450")
    main_screen.configure(bg = "white")
    main_screen.title("Account Login")
    Label(text="Select Your Choice", bg = "deep sky blue", fg = "black", width="300", height="2", font=("Calibri", 13)).pack()
    Label(text="", bg = "white").pack()

    path = os.path.join(CURPATH, "Information", "night_light_logo.PNG")
    logo = PhotoImage(file = path)
    
    Label(image = logo, bg = "white").pack()
    Label(text="", bg = "white").pack()
    Button(text="Login to Your Account", bg = "cyan", height="2", width="30", command = login).pack()
    Label(text="", bg = "white").pack()
    Button(text="Add Another Account", bg = "cyan", height="2", width="30", command=register).pack()
 
    main_screen.mainloop()

# Designing window for registration
 
def register():
    global register_screen
    register_screen = Toplevel(main_screen)
    register_screen.title("Add Another Account")
    register_screen.geometry("300x300")
    register_screen. configure(bg = "white")

    global username
    global password
    global email_address
    global username_entry
    global password_entry
    global email_address_entry

    username = StringVar()
    password = StringVar()
    email_address = StringVar()
 
    Label(register_screen, text= "Please fill out the details below", bg = "white").pack()
    Label(register_screen, text="" , bg = "white").pack()
    username_lable = Label(register_screen, text="Username * ", bg = "white")
    username_lable.pack()
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
    email_lable = Label(register_screen, text="Email Address * ", bg = "white")
    email_lable.pack()
    email_address_entry = Entry(register_screen, textvariable=email_address)
    email_address_entry.pack()
    password_lable = Label(register_screen, text="Password * ", bg = "white")
    password_lable.pack()
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    Label(register_screen, text="" , bg = "white").pack()
    Button(register_screen, text="Register", width=10, height=1, bg = "cyan", command = register_user).pack()

    global info_regis
    info_screen = Frame(register_screen)
    info_screen.pack()
    info_regis = Label(info_screen)
    info_regis.pack()
 


# Designing window for login 
 
def login():
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    login_screen.configure(bg = "white")

    Label(login_screen, text="Please fill out the details below", bg = "white").pack()
    Label(login_screen, text="", bg = "white").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
 
    global username_login_entry
    global password_login_entry
 
    Label(login_screen, text="Username * ", bg = "white").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="", bg = "white").pack()
    Label(login_screen, text="Password * ", bg = "white").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="", bg = "white").pack()
    Button(login_screen, text="Login", bg = "cyan", width=10, height=1, command = login_verify).pack()


 
# Implementing event on register button
 
def register_user():
 
    username_info = username.get()
    password_info = password.get()
    email_info = email_address.get()

    username_entry.delete(0, END)
    password_entry.delete(0, END)
    email_address_entry.delete(0, END)

    db = DBInterface.DBInterface()

    if(isBlank(username_info) or isBlank(password_info) or isBlank(email_info)):
        empty_filler()
        info_regis.configure(text="Registration Failed", justify = "center", bg = "white", fg="green", font=("calibri", 11))
    else:
        reg = db.register(username_info, email_info, password_info)
        data = json.loads(reg)
        
        if (data["status"] == True):
            pub_cmd.publish(client, "update email")
            info_regis.configure(text="Registration Success", justify = "center", bg = "white", fg="green", font=("calibri", 11))
        else:
            user_info_exist(data["err"])
            info_regis.configure(text="Registration Failed", justify = "center", bg = "white", fg="green", font=("calibri", 11))

           
# Implementing event on login button 
 
def login_verify():
    
    username1 = username_verify.get()
    password1 = password_verify.get()
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)

    global data2
    db = DBInterface.DBInterface()
    log = db.login(username1, password1)
    data2 = json.loads(log)
    
    if(data2["status"] == True):
        global check
        data2["username"] = username1
        login_sucess()
        check = True
    else:
        user_and_password_not_recognised()


def verified():
    return check

def get_user_info():
    return data2

# Designing popup for login success
 
def login_sucess():
    delete_login_success()

# Designing popup for login invalid password
 
def user_and_password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Error Password")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Username and Password do not match").pack()
    Button(password_not_recog_screen, text="OK", bg = "cyan", command=delete_password_not_recognised).pack()
 

# Designing popup for username has been used
def user_info_exist(information):
    global username_exist_screen
    username_exist_screen = Toplevel(register_screen)
    username_exist_screen.title("Error Registaration")
    username_exist_screen.geometry("200x100")
    Label(username_exist_screen, text= information).pack()
    Button(username_exist_screen, text="OK", bg = "cyan", command=delete_username_exist_screen).pack()

# Designing popup for the filler of registration are not filled
def empty_filler():
    global empty_filler_screen
    empty_filler_screen = Toplevel(register_screen)
    empty_filler_screen.title("Error Registration")
    empty_filler_screen.geometry("200x100")
    Label(empty_filler_screen, text="You have not filled the filler box").pack()
    Button(empty_filler_screen, text="OK", bg = "cyan", command=delete_empty_filler_screen).pack()


# Deleting popups
 
def delete_login_success():
    login_screen.destroy()
    main_screen.destroy()

def delete_password_not_recognised():
    password_not_recog_screen.destroy()
  
# def delete_user_not_found_screen():
#     user_not_found_screen.destroy()
 
def delete_username_exist_screen():
    username_exist_screen.destroy()

def delete_empty_filler_screen():
    empty_filler_screen.destroy()

def isBlank(my_string):
    if my_string and my_string.strip():
        return False
    return True


client = pub_cmd.connect_mqtt()
