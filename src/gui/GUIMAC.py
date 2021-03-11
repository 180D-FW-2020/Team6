#from tutorial:
# https://realpython.com/python-gui-tkinter/
# http://openbookproject.net/courses/python4fun/tkphone1.html
# https://www.geeksforgeeks.org/gui-chat-application-using-tkinter-in-python/

import AudioClient
import tkinter as tk
from tkinter import ttk
from socket import AF_INET, socket, SHUT_RDWR, SOCK_STREAM
from imutils.video import VideoStream
from tkmacosx import Button as button
from Login_system import *
from sub_cmd import *
import io
import cv2
import sys
import threading
import os
import requests
import sub_cmd
import pub_cmd
import json
from datetime import datetime
from audioplayer import AudioPlayer
import time

# src path
SRCPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Database interface
DBPATH = os.path.join(SRCPATH, "database")
sys.path.append(DBPATH)
import DBInterface

# S3 interface
S3PATH = os.path.join(SRCPATH, "s3")
sys.path.append(S3PATH)
import s3Client
s3i = s3Client.S3Interface()

#for video
import numpy as np
import struct
import time
from PIL import Image
from PIL import ImageTk

class GUI:
    def __init__(self, information):

        # Intializing the user info
        self.user_info = information

        # Defining the current path
        self.CURPATH = os.path.dirname(os.path.abspath(__file__))
        

        # Making a GUI window
        self.window = tk.Tk()
        self.video_panel = None #video
        self.window.geometry("1050x700")
        #self.window.configure(bg="#4DA8DA")
        self.window.configure(bg="white")
        
        # Title of GUI
        tk.Label(self.window, text="Welcome,\nUser: " + self.user_info["username"] + "\n How can we help you?",
                                 font="Calibri 20 bold", bg="deep sky blue", fg="white", height = 3).pack(fill = BOTH)
        
        #App holds The video and the IMU status bar
        self.app = tk.Frame(self.window)
        self.app.configure(bg="white")
        self.app.pack(side = LEFT)

        # Showing the buttons in the display in a frame (All buttons are in a frame)
        self.button_frame = tk.Frame(self.window)
        self.button_frame.configure(bg="white")
        self.button_frame.pack(side = LEFT)
        
        # Showing the action in the main display //Holds How can I help you and the IMU info
        self.lmain = tk.Label(self.app)
        self.lmain.pack(side = BOTTOM)


        # Setting the main display
        self.main_display()

        # Accessing the file in this path (Logo Switches with video frame)
        self.path = os.path.join(self.CURPATH, "Information", "nightlight_app_logo_white.png")
        self.logo = PhotoImage(file = self.path)

        # Showing The Video Frame
        self.video_frame = tk.Label(self.app, image = self.logo)
        self.video_frame.configure(bg="white")
        self.video_frame.pack( side = LEFT)


        self.mute = True
        # Inserting the icon for each buttons
        self.path = os.path.join(self.CURPATH, "Information", "no_sound_dsb.png")
        self.loadimage = tk.PhotoImage(file = self.path)
        self.path = os.path.join(self.CURPATH, "Information", "sound_dsb.png")
        self.loadimage2 = tk.PhotoImage(file = self.path)
        self.path = os.path.join(self.CURPATH, "Information", "tv_dsb.png")
        self.loadimage3 = tk.PhotoImage(file = self.path)
        self.path = os.path.join(self.CURPATH, "Information", "music_dsb.png")
        self.loadimage4 = tk.PhotoImage(file = self.path)
        self.path = os.path.join(self.CURPATH, "Information", "user_dsb.png")
        self.loadimage5 = tk.PhotoImage(file = self.path)
        self.path = os.path.join(self.CURPATH, "Information", "chat_dsb.png")
        self.loadimage6 = tk.PhotoImage(file = self.path)
        self.path = os.path.join(self.CURPATH, "Information", "quit_dsb.png")
        self.loadimage7 = tk.PhotoImage(file = self.path)
        
        

        # Initializing the notification
        self.getting_user_info()
        if(self.notification_info2 == True):
            self.notification = "On"
        else:
            self.notification = "Off"

        self.video_stream = False
        self.video_notification = "Off"

        # Prepare recordings directory and attributes
        # Recordings 
        self.recording_path = os.path.join(SRCPATH, "recordings")
        if not os.path.exists(self.recording_path):
            try:
                os.mkdir(self.recording_path)
            except OSError:
                print("Failed to create directory as src/")
        
        self.recordings_ls = []
        try:
            self.recordings_ls = os.listdir(self.recording_path)
        except:
            pass

        # presigned url cache timer
        self.url_time_to_live = 170

        # Audio Player
        self.ap = None

        # Creating buttons
        root = Tk()
        for i in range(4):
            for j in range(2):
                self.frame = tk.Frame(master=self.button_frame, relief=tk.RAISED, borderwidth=1)
                self.frame.grid(row=i, column=j)
                if i == 0 and j == 0:

                    self.button_a = tk.Button(self.frame, text="Watch the baby" + "\n\n\n\n" + self.video_notification, font="Helvetica 11 bold",
                                   highlightbackground="deep sky blue", fg="BLACK", highlightthickness=20,image = self.loadimage3, compound = "center", command=self.handle_click_video_stream)
                    self.button_a.place(x=5, y=10, width=140, height=30)
                    self.button_a.pack() #Video
                    #tk.Button.place(x=5, y=10, width=140, height=30)
                if i == 0 and j == 1:
                    self.button_b = tk.Button(self.frame, text="Play lullaby", font="Helvetica 11 bold",
                                   highlightbackground="deep sky blue", fg="BLACK", highlightthickness=20, image = self.loadimage4, compound = "bottom", command=self.handle_click_lullaby)
                    self.button_b.place(x=5, y=10, width=140, height=30)
                    self.button_b.pack() #Lullaby
                if i == 1 and j == 0:
                    self.button_c = tk.Button(self.frame, text="Listen To Audio", font="Helvetica 11 bold",
                                   highlightbackground="deep sky blue", fg="black", highlightthickness=30,image=self.loadimage, compound="bottom", command=self.handle_click_listen)
                    self.button_c.place(x=5, y=10, width=140, height=30)
                    self.button_c.pack() #Audio
                if i == 1 and j == 1:
                    self.button_h = tk.Button(self.frame, text="Recordings", font="Helvetica 11 bold", highlightbackground="deep sky blue", fg="BLACK", highlightthickness=30,command=self.handle_click_recordings)
                    self.button_h.place(x=5, y=10, width=140, height=30)
                    self.button_h.pack() #Recordings
                if i == 2 and j == 0:
                    self.button_d = tk.Button(self.frame, text="Changing Login Info", font="Helvetica 11 bold",
                                   highlightbackground="deep sky blue", fg="BLACK", highlightthickness=20, image = self.loadimage5, compound = "bottom", command=self.handle_click_changing_login_info)
                    self.button_d.place(x=5, y=10, width=140, height=30)
                    self.button_d.pack() #Settings
                if i == 2 and j == 1:
                    self.button_e = tk.Button(self.frame, text="Open Chat Window", font="Helvetica 11 bold",
                                   highlightbackground="deep sky blue", fg="BLACK", highlightthickness=20,image = self.loadimage6, compound = "bottom", command=self.handle_click_open_chat_window)
                    self.button_e.place(x=5, y=10, width=140, height=30)
                    self.button_e.pack() #Chat
                if i == 3 and j == 0:
                    self.button_f = tk.Button(self.frame, text="Current Notification" + "\n\n" + self.notification, font="Helvetica 11 bold", 
                                     highlightbackground="deep sky blue", fg="BLACK", highlightthickness=20, command=self.handle_click_notification)
                    self.button_f.place(x=5, y=10, width=140, height=30)
                    self.button_f.pack() #Notification
                if i == 3 and j == 1:
                    self.button_g = tk.Button(self.frame, text="Quit", font="Helvetica 11 bold",
                                   highlightbackground="deep sky blue", fg="BLACK", highlightthickness=20, image = self.loadimage7, compound = "bottom", command=self.quit_the_program)
                    self.button_g.place(x=5, y=10, width=140, height=30)
                    self.button_g.pack() #Quit

        # self.window.protocol("WM_DELETE_WINDOW", self.quit_the_program)
        self.window.mainloop()  # runs application

    # Event handlers
    def main_display(self):
        # Setting the main display
        try:
            self.txt = open("notification.txt", "r")
            self.txt = self.txt.readline()
        except:
            self.txt = "-Baby Pose Sensor Unavailable-"
        # self.lmain.configure(text=self.txt,font="Helvetica 20 bold", bg="#4DA8DA", fg="#EEFBFB")
        self.lmain.configure(text=self.txt,font="Helvetica 30 bold", bg="white", fg="green")
        self.lmain.after(1000, self.main_display)
	
    
    def handle_click_video_stream(self):
      
        if (self.video_stream == False):
            self.video_stream = True
            self.video_notification = "On"
            self.button_a.config(text="Watch the baby" + "\n\n\n\n" + self.video_notification)            

            #initialize video client connections
            #use try/except for if server isn't running?
            self.gui_sock = socket()
            #gui_sock.connect(('3.140.200.49',6662)) # connect to Denny's AWS Server's public IP
            self.gui_sock.connect(('18.189.21.182',6662)) # connect to Robert's AWS Server's public IP
            print("Client User listening on port...")
            self.connection = self.gui_sock.makefile('rb')
            print("Client User connected")
            self.video_thread = threading.Thread(target=self.videoLoop,args=())
            self.video_thread.start()
            self.window.wm_title("Video Stream")
        else:
            self.video_stream = False
            self.video_notification = "Off"
            self.button_a.config(text="Watch the baby" + "\n\n\n\n" + self.video_notification)            
            self.video_frame.config(image = self.logo)

            self.connection.close()
            self.gui_sock.close()

    def videoLoop(self):
        try:
            while True:
                self.image_len = struct.unpack('<L', self.connection.read(struct.calcsize('<L')))[0]
                if not self.image_len:
                    print("invalid data from stream ")
                    break
                print(self.image_len)
                self.image_stream = io.BytesIO()
                self.image_stream.write(self.connection.read(self.image_len))
                self.image_stream.seek(0)

                self.file_bytes = np.asarray(bytearray(self.image_stream.read()),dtype=np.uint8)
                self.raw_image = cv2.imdecode(self.file_bytes,cv2.IMREAD_COLOR)
                self.rgb_image = cv2.cvtColor(self.raw_image, cv2.COLOR_BGR2RGB) #self vs no self?
                self.pil_image = Image.fromarray(self.rgb_image)
                self.pil_image = ImageTk.PhotoImage(self.pil_image)

                self.video_frame.config(image=self.pil_image)
                self.video_frame.image = self.pil_image
                self.video_frame.pack(padx=1, pady=1)
        except:
            print("Occurred Exception, closing socket")
            self.connection.close()
            self.gui_sock.close()

    def handle_click_lullaby(self):
        self.button_b.configure(state = tk.DISABLED)
        
        self.new_window = tk.Toplevel(self.window)
        self.new_window.configure(bg="white")

        # Making a scroll bar display
        self.scroll_bar = tk.Scrollbar(self.new_window)
        self.option = tk.Listbox(self.new_window, relief=tk.SUNKEN, borderwidth=3, bg="deep sky blue", fg="black",
                                 font="Helvetica 11 bold", yscrollcommand=self.scroll_bar.set)
        self.inserting_option()
        self.option.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scroll_bar.config(command=self.option.yview)

        self.select = tk.Button(self.new_window, text="Play Song", relief=tk.RAISED, borderwidth=3, bg="deep sky blue",
                                fg="BLACK", font="Helvetica 11 bold", command=self.play_sound)
        self.select.pack(fill=tk.BOTH)
        
        self.pause = tk.Button(self.new_window, text="Pause Song", relief=tk.RAISED, borderwidth=3, bg="deep sky blue",
                                fg="BLACK", font="Helvetica 11 bold", command= self.pause_sound)
        self.pause.pack(fill=tk.BOTH)

        self.resume = tk.Button(self.new_window, text="Resume Song", relief=tk.RAISED, borderwidth=3, bg="deep sky blue",
                                fg="BLACK", font="Helvetica 11 bold", command= self.resume_sound)
        self.resume.pack(fill=tk.BOTH)

        self.stop = tk.Button(self.new_window, text="Stop Song", relief=tk.RAISED, borderwidth=3, bg="deep sky blue",
                                fg="BLACK", font="Helvetica 11 bold", command= self.stop_sound)
        self.stop.pack(fill=tk.BOTH)

        self.new_window.protocol("WM_DELETE_WINDOW", self.quit_play_song_window)
    

    def handle_click_listen(self):
        
        if self.mute == True:
            self.button_c.config(image = self.loadimage2)
            # Audio Streaming
            self.audio_conn = AudioClient.AudioClient(write = False)    
            self.audio_conn.write = True
            self.audio_conn.start()
            thread = threading.Thread(target=self.audio_conn.recv)
            thread.start()
            self.mute = False 

        elif self.mute == False:
            self.button_c.config(image = self.loadimage)
            self.audio_conn.stop()
            self.audio_conn.write = False 
            self.mute = True

    def handle_click_changing_login_info(self):
        self.button_d.configure(state = tk.DISABLED)
        
        self.login_screen = tk.Toplevel(self.window)
        self.login_screen.geometry("300x300")
        self.login_screen.configure(bg="white")
        tk.Label(self.login_screen, text = "Please choose either one of these button", bg = "white", fg = "black").pack()
        tk.Label(self.login_screen, text = "", bg = "white").pack()
        self.pass_button = tk.Button(self.login_screen, text = "Changing Password", bg = "deep sky blue", fg= "black", relief=tk.RAISED, borderwidth=3, font = "Helvetica 11 bold", command = self.changing_password)
        self.pass_button.pack()
        tk.Label(self.login_screen, text = "", bg = "white").pack()
        self.email_button = tk.Button(self.login_screen, text = "Changing Email", bg = "deep sky blue", fg= "black", relief=tk.RAISED, borderwidth=3, font = "Helvetica 11 bold", command = self.changing_email)
        self.email_button.pack()

        self.login_screen.protocol("WM_DELETE_WINDOW", self.quit_login_window)
    
    def handle_click_recordings(self):
        self.button_h.configure(state = tk.DISABLED)
        
        self.record_screen = tk.Toplevel(self.window)
        self.record_screen.geometry("300x300")
        self.record_screen.configure(bg="white")
        tk.Label(self.record_screen, text = "", bg = "white").pack()
        self.download_button = tk.Button(self.record_screen, text = "Download from cloud", bg = "deep sky blue", fg= "black", relief=tk.RAISED, borderwidth=3, font = "Helvetica 11 bold", command = self.handle_download)
        self.download_button.pack()
        tk.Label(self.record_screen, text = "", bg = "white").pack()
        self.record_button = tk.Button(self.record_screen, text = "Play recordings", bg = "deep sky blue", fg= "black", relief=tk.RAISED, borderwidth=3, font = "Helvetica 11 bold", command = self.play_recordings)
        self.record_button.pack()

        self.record_screen.protocol("WM_DELETE_WINDOW", self.quit_record_window)

    def handle_download(self):
        self.download_button.configure(state = tk.DISABLED)
        
        self.new_window3 = tk.Toplevel(self.record_screen)
        self.new_window3.configure(bg="white")

        # Making a scroll bar display
        self.scroll_bar = tk.Scrollbar(self.new_window3)
        self.option = tk.Listbox(self.new_window3, selectmode=MULTIPLE, bd=0, bg="deep sky blue", fg="black", relief=tk.SUNKEN, borderwidth=3,
                                 font="Helvetica 11 bold", yscrollcommand=self.scroll_bar.set)
        self.s3_ls_recordings()
        self.option.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scroll_bar.config(command=self.option.yview)

        self.select = tk.Button(self.new_window3, text="Download", bd=0, bg="deep sky blue",
                                fg="BLACK", relief=tk.RAISED, borderwidth=3, font="Helvetica 11 bold", command=self.get_recordings)
        self.select.pack(fill=tk.BOTH)

        self.new_window3.protocol("WM_DELETE_WINDOW", self.quit_play_song_window3)

    def play_recordings(self):
        self.record_button.configure(state = tk.DISABLED)
        
        self.new_window2 = tk.Toplevel(self.record_screen)
        self.new_window2.configure(bg="white")

        # Making a scroll bar display
        self.scroll_bar = tk.Scrollbar(self.new_window2)
        self.option = tk.Listbox(self.new_window2, bd=0, bg="deep sky blue", fg="white", relief=tk.SUNKEN, borderwidth=3,
                                 font="Helvetica 11 bold", yscrollcommand=self.scroll_bar.set)
        self.ls_recordings()
        self.option.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scroll_bar.config(command=self.option.yview)

        self.select = tk.Button(self.new_window2, text="Play", relief=tk.RAISED, borderwidth=3, bg="deep sky blue",
                                fg="BLACK", font="Helvetica 11 bold", command=self.play_sound_local)
        self.select.pack(fill=tk.BOTH)

        self.pause = tk.Button(self.new_window2, text="Pause", relief=tk.RAISED, borderwidth=3, bg="deep sky blue",
                                fg="BLACK", font="Helvetica 11 bold", command= self.pause_sound_local)
        self.pause.pack(fill=tk.BOTH)

        self.resume = tk.Button(self.new_window2, text="Resume", relief=tk.RAISED, borderwidth=3, bg="deep sky blue",
                                fg="BLACK", font="Helvetica 11 bold", command= self.resume_sound_local)
        self.resume.pack(fill=tk.BOTH)

        self.delete = tk.Button(self.new_window2, text="Delete", relief=tk.RAISED, borderwidth=3, bg="deep sky blue",
                                fg="BLACK", font="Helvetica 11 bold", command= self.delete_recording)
        self.delete.pack(fill=tk.BOTH)

        self.new_window2.protocol("WM_DELETE_WINDOW", self.quit_play_song_window2)


    def handle_click_open_chat_window(self):
        self.button_e.configure(state = tk.DISABLED)
        
        self.chat_window = tk.Toplevel(self.window)
        self.chat_window.title("Chatter")

        self.messages_frame = tk.Frame(self.chat_window)
        self.my_msg = tk.StringVar()  # For the messages to be sent.
        self.scrollbar = tk.Scrollbar(self.messages_frame)  # To navigate through past messages.
        
        # Following will contain the messages.
        self.msg_list = tk.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side= tk.RIGHT, fill= tk.Y)
        self.msg_list.pack(side= tk.LEFT, fill= tk.BOTH)
        self.msg_list.pack()
        self.messages_frame.pack()


        self.guide = tk.Label(self.chat_window, text = "Type your messages below")
        self.guide.pack()
        self.entry_field = tk.Entry(self.chat_window, textvariable = self.my_msg)
        self.entry_field.bind("<Return>", self.send)
        self.entry_field.pack()
        self.send_button = tk.Button(self.chat_window, text="Send", bg = "deep sky blue", fg = "black", relief=tk.RAISED, borderwidth=3, command = self.send)
        self.send_button.pack()
        
        self.chat_window.protocol("WM_DELETE_WINDOW", self.on_closing)

        #----Now comes the sockets part----
        HOST = '18.189.21.182'#input('Enter host: ')
        PORT = int (33000)

        self.BUFSIZ = 1024
        ADDR = (HOST, PORT)

        self.client_socket = socket(AF_INET, SOCK_STREAM)
        self.client_socket.connect(ADDR)
        self.client_socket.send(self.username_info2.encode("utf8"))
        receive_thread = threading.Thread(target = self.receive)
        receive_thread.start()



    def handle_click_notification(self):
        
        db = DBInterface.DBInterface()
        if(self.notification == "On"):
            self.notification = "Off"
            self.button_f.config(text="Current Notification" + "\n\n" + self.notification)
            pub_cmd.publish(client, "update email")
            db.switch_notification(self.ID_info2, False)
        elif (self.notification == "Off"):
            self.notification = "On"
            self.button_f.config(text="Current Notification" + "\n\n" + self.notification)
            pub_cmd.publish(client, "update email")
            db.switch_notification(self.ID_info2, True)


    def quit_the_program(self):
        if(self.mute == False):
            self.audio_conn.stop()
            self.audio_conn.write = False
        if(self.video_stream == True):
            self.connection.close()
            self.gui_sock.close()
        sys.exit()


    # Some funcions for play song button
    def inserting_option(self):
        self.option.insert(tk.END, "First Lullaby")
        self.option.insert(tk.END, "Second Lullaby")
        self.option.insert(tk.END, "Third Lullaby")
        self.option.insert(tk.END, "Fourth Lullaby")

    def url_cache_timer(self, name):
        time.sleep(self.url_time_to_live)
        try:
            self.recordings[name]["isAlive"] = False
        except:
            # self.recordings is wiped
            pass

    def s3_ls_recordings(self):
        self.recordings = {}
        names = s3i.get_all()["names"]
        for name in names:
            if name in self.recordings_ls:
                continue

            name = os.path.splitext(name)[0]
            self.recordings[name] = {"url": None, "isAlive": False}
            self.option.insert(tk.END, name)
    
    def ls_recordings(self):
        for name in self.recordings_ls:
            name = os.path.splitext(name)[0]
            self.option.insert(tk.END, name)

    def play_sound(self):
        scrollbar_command = self.option.get('active')
        if scrollbar_command == 'First Lullaby':
            pub_cmd.publish(client, "lullaby1.mp3")
        elif scrollbar_command == 'Second Lullaby':
            pub_cmd.publish(client, "lullaby2.mp3")
        elif scrollbar_command == 'Third Lullaby':
            pub_cmd.publish(client, "lullaby3.mp3")
        elif scrollbar_command == 'Fourth Lullaby':
            pub_cmd.publish(client, "lullaby4.mp3")
    
    def play_sound_local(self):
        audio_path = self.option.get('active')
        audio_path = os.path.join(self.recording_path, audio_path) + ".wav"
        self.ap = AudioPlayer(audio_path)
        self.ap.play(block=False)
    
    def pause_sound_local(self):
        self.ap.pause()

    def resume_sound_local(self):
        self.ap.resume()
    
    def delete_recording(self):
        name = self.option.get('active')
        audio_path = os.path.join(self.recording_path, name) + ".wav"
        
        if self.ap is not None:
            self.ap.stop()
            self.ap.close()
        
        try:
            os.remove(audio_path)
        except OSError:
            print("Failed to delete recordings")
        else:
            self.recordings_ls.remove(name + ".wav")
            self.option.delete(self.option.curselection())
    
    def get_recordings(self):
        selected_options = self.option.curselection()
        for opt in selected_options[::-1]:
            name = self.option.get(opt)
            name_ext = name +".wav"

            if name not in self.recordings:
                return
            
            url_info = self.recordings[name]
            if url_info["isAlive"]:
                url = url_info["url"]

            else:
                res = s3i.get_one(name_ext)
                if res["status"]:
                    url = res["url"]
                    self.recordings[name]["isAlive"] = True
                    self.recordings[name]["url"] = url

                    # Start cache timer
                    url_timer = threading.Thread(target=self.url_cache_timer, args=(name,))
                    url_timer.setDaemon(True)
                    url_timer.start()

                    download = threading.Thread(target=self._download, args=(url, name_ext))
                    download.start()

                    self.option.delete(opt)

                else:
                    print("Error in fetching data")
                    return

    def _download(self, url, name_ext):
        get_res = requests.get(url=url)

        fname = os.path.join(self.recording_path, name_ext)
        try:
            with open(fname, "wb") as f:
                f.write(get_res.content)

        except OSError:
            print("Failed to write in file.")

        else:
            self.recordings_ls.append(name_ext)

    def quit_record_window(self):
        self.record_screen.destroy()
        self.button_h.configure(state = tk.NORMAL)
    
    def quit_play_song_window3(self):
        self.new_window3.destroy()
        self.download_button.configure(state = tk.NORMAL)
    
    def quit_play_song_window2(self):
        self.new_window2.destroy()
        self.record_button.configure(state = tk.NORMAL)
    


    def pause_sound(self):
        pub_cmd.publish(client, "pause")

    def resume_sound(self):
        pub_cmd.publish(client, "resume")
    
    def stop_sound(self):
        pub_cmd.publish(client, "pause")
    
    def quit_play_song_window(self):
        self.new_window.destroy()
        self.button_b.configure(state = tk.NORMAL)


    # Some Functions for Chat Client
    def receive(self):
        """Handles receiving of messages."""
        while True:
            try:
                self.msg = self.client_socket.recv(self.BUFSIZ).decode("utf8")
                self.msg_list.insert(tk.END, self.msg)
            except OSError:  # Possibly client has left the chat.
                break
    
    def send(self, event=None):  # event is passed by binders.
        """Handles sending of messages."""
        self.msg = self.my_msg.get()
        self.my_msg.set("")  # Clears input field.
        self.client_socket.send(bytes(self.msg, "utf8"))
        if self.msg == "quit":
            self.chat_window.destroy()
            self.client_socket.shutdown(SHUT_RDWR)
            self.client_socket.close()
    
    def on_closing(self, event=None):
        """This function is to be called when the chat window is closed."""
        self.button_e.configure(state = tk.NORMAL)
        self.my_msg.set("quit")
        self.send()
    

    # Some functions for changing login info
    def changing_password(self):
        self.pass_button.configure(state = tk.DISABLED)
        self.password = tk.StringVar()
        self.password2 = tk.StringVar()
        self.password_screen = tk.Toplevel(self.login_screen)
        self.password_screen.geometry("300x300")
        self.password_screen.configure(bg = "white")
        self.password_lable = Label(self.password_screen, text="Current Password * ", bg = "white")
        self.password_lable.pack()
        self.password_entry = Entry(self.password_screen, textvariable=self.password, show='*')
        self.password_entry.pack()
        tk.Label(self.password_screen, text="", bg = "white").pack()
        self.password_lable2 = Label(self.password_screen, text="New Password * ", bg = "white")
        self.password_lable2.pack()
        self.password_entry2 = Entry(self.password_screen, textvariable=self.password2, show='*')
        self.password_entry2.pack()
        tk.Label(self.password_screen, text="" , bg = "white").pack()
        tk.Button(self.password_screen, text="Update", width=10, height=1, bg = "deep sky blue", relief=tk.RAISED, borderwidth=3, command = self.register_pass).pack()

        self.info_screen = tk.Frame(self.password_screen)
        self.info_screen.pack()
        self.info_regis = tk.Label(self.info_screen)
        self.info_regis.pack()
        self.password_screen.protocol("WM_DELETE_WINDOW", self.quit_password_window)


    def changing_email(self):
        self.email_button.configure(state = tk.DISABLED)
        self.email_address = tk.StringVar()
        self.email_screen = tk.Toplevel(self.login_screen)
        self.email_screen.geometry("300x300")
        self.email_screen.configure(bg = "white")
        self.password_lable = Label(self.email_screen, text="Current Password * ", bg = "white")
        self.password_lable.pack()
        self.password_entry = Entry(self.email_screen, textvariable=self.password, show='*')
        self.password_entry.pack()
        tk.Label(self.email_screen, text="", bg = "white").pack()
        self.email_lable = Label(self.email_screen, text="Email Address * ", bg = "white")
        self.email_lable.pack()
        self.email_address_entry = Entry(self.email_screen, textvariable=self.email_address)
        self.email_address_entry.pack()
        tk.Label(self.email_screen, text="" , bg = "white").pack()
        tk.Button(self.email_screen, text="Update", width=10, height=1, bg = "deep sky blue", relief=tk.RAISED, borderwidth=3, command = self.register_email).pack()

        self.info_screen = tk.Frame(self.email_screen)
        self.info_screen.pack()
        self.info_regis = tk.Label(self.info_screen)
        self.info_regis.pack()

        self.email_screen.protocol("WM_DELETE_WINDOW", self.quit_email_window)

    def register_pass(self):
        self.password_info = self.password.get()
        self.password_entry.delete(0, END)
        self.password_info2 = self.password2.get()
        self.password_entry2.delete(0, END)

        if(isBlank(self.password_info) or isBlank(self.password_info2)):
            self.empty_filler()
            self.info_regis.configure(text="Failed", justify = "center", bg = "white", fg="deep sky blue", font=("calibri", 11))
        else:
            db = DBInterface.DBInterface()
            log = db.login(self.username_info2, self.password_info)
            data2 = json.loads(log)
            if(data2["status"] == True):
                db.update_password(self.ID_info2, self.password_info, self.password_info2)
                self.info_regis.configure(text="Success Changing Password", justify = "center", bg = "white", fg="deep sky blue", font=("calibri", 11))
            else:
                self.info_regis.configure(text="Wrong Current Password", justify = "center", bg = "white", fg="deep sky blue", font=("calibri", 11))

    
    def register_email(self):
        self.password_info = self.password.get()
        self.password_entry.delete(0, END)
        self.email_info = self.email_address.get()
        self.email_address_entry.delete(0, END)

        if(isBlank(self.email_info) or isBlank(self.password_info)):
            self.empty_filler()
            self.info_regis.configure(text="Failed", justify = "center", bg = "white", fg="deep sky blue", font=("calibri", 11))
        else:
            db = DBInterface.DBInterface()
            log = db.login(self.username_info2, self.password_info)
            data2 = json.loads(log)
            if(data2["status"] == True):
                db.update_email(self.ID_info2, self.email_info2, self.email_info, self.password_info)
                pub_cmd.publish(client, "update email")
                self.info_regis.configure(text="Success Changing Email", justify = "center", bg = "white", fg="deep sky blue", font=("calibri", 11))
            else:
                self.info_regis.configure(text="Wrong Current Password", justify = "center", bg = "white", fg="deep sky blue", font=("calibri", 11))
    
    def quit_login_window(self):
        self.login_screen.destroy()
        self.button_d.configure(state = tk.NORMAL)

    def quit_password_window(self):
        self.password_screen.destroy()
        self.pass_button.configure(state = tk.NORMAL)
    
    def quit_email_window(self):
        self.email_screen.destroy()
        self.email_button.configure(state = tk.NORMAL)

    # Some Useful Functions
    def getting_user_info(self):
        self.username_info2 = self.user_info["username"]
        self.email_info2 = self.user_info["email"] 
        self.notification_info2 = self.user_info["notification"]
        self.ID_info2 = self.user_info["id"]
        
    def empty_filler(self):
        self.empty_filler_screen = Toplevel()
        self.empty_filler_screen.title("Error Registration")
        self.empty_filler_screen.geometry("200x100")
        Label(self.empty_filler_screen, text="You have not filled the filler box").pack()
        Button(self.empty_filler_screen, text="OK", bg = "deep sky blue", relief=tk.RAISED, borderwidth=3, command= self.delete_empty_filler_screen).pack()

    def delete_empty_filler_screen(self):
        self.empty_filler_screen.destroy()

    def isBlank(self, my_string):
        if my_string and my_string.strip():
            return False
        return True

main_account_screen()
information = get_user_info()
if (verified() == True):
    client = pub_cmd.connect_mqtt()
    sub_client = sub_cmd.connect_mqtt()
    g = GUI(information)

# client = pub_cmd.connect_mqtt()
# sub_client = sub_cmd.connect_mqtt()
# g = GUI("Leondi")
