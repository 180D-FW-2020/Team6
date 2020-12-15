#from tutorial:
# https://realpython.com/python-gui-tkinter/
# http://openbookproject.net/courses/python4fun/tkphone1.html
# https://www.geeksforgeeks.org/gui-chat-application-using-tkinter-in-python/

import tkinter as tk
from PIL import Image, ImageTk
from imutils.video import VideoStream
import io
import cv2
import sys
import threading
import os
import sub_cmd
import pub_cmd

# sys.path.append("../../comms")
# import AudioClient	# pylint: disable=import-error

#img_speaker =  tk.PhotoImage()

class GUI:
	def __init__(self):

		# Making a GUI window
		self.window = tk.Tk()
		self.window.geometry("480x550")
		self.window.configure(bg="#4DA8DA")

		# Title of GUI
		self.greeting = tk.Label(text="Night Light Baby Monitor",
		                         font="Helvetica 20 bold", bg="#4DA8DA", fg="#EEFBFB")
		self.greeting.pack(fill=tk.BOTH)
		self.app = tk.Frame(self.window)
		self.app.pack()

		# Showing the action in the main display
		self.lmain = tk.Label(self.app)
		self.lmain.pack()

		# Setting the main display
		self.main_display()
		# Showing the button in the display
		self.button_frame = tk.Frame(self.window)
		self.button_frame.configure(bg="#4DA8DA")
		self.button_frame.pack()

		# Inserting a rounded button for MIC
		# self.loadimage = tk.PhotoImage(file = "mic2.png")

		# Creating buttons
		self.button_a = tk.Button(self.button_frame, text="Watch the baby", font="Helvetica 11 bold",
		                          width=14, height=5, bg="BLUE", fg="#EEFBFB", command=self.video_stream)
		self.button_b = tk.Button(self.button_frame, text="Play lullaby", font="Helvetica 11 bold",
		                          width=14, height=5, bg="BLUE", fg="#EEFBFB", command=self.handle_click_lullaby)
		self.button_c = tk.Button(self.button_frame, text="Listen", font="Helvetica 11 bold",
		                          width=14, height=5, bg="NAVY BLUE", fg="#EEFBFB", command=self.handle_click_listen)
		# self.button_d = tk.Button(self.button_frame, text = "Send Voice Message", image = self.loadimage, bg = "#203647",fg = "#EEFBFB", borderwidth = "0", compound = "bottom")
		self.button_d = tk.Button(self.button_frame, text="Quit", font="Helvetica 11 bold",
		                          width=14, height=5, bg="NAVY BLUE", fg="#EEFBFB", command=self.quit_the_program)

		self.button_a.pack(side=tk.LEFT, fill=tk.BOTH)
		self.button_b.pack(side=tk.LEFT, fill=tk.BOTH)
		self.button_c.pack(side=tk.LEFT, fill=tk.BOTH)
		# self.button_d.pack(side = tk.RIGHT)
		self.button_d.pack(side=tk.LEFT, fill=tk.BOTH)
		# Video Streaming
		self.cap = cv2.VideoCapture(0)

		# Audio Streaming
		# self.audio_conn = AudioClient.AudioClient()
		# self.audio_conn.start()
		# self.listen = False

		self.window.mainloop()  # runs application

		#Displaying an image
		#pilfile = Image.open("image.jpg")
		#image_vid = ImageTk.PhotoImage(pilfile)
		#video_feed = tk.Label(image=image_vid)
		#video_feed.pack()


	def main_display(self):
		# Setting the main display
		try:	
			self.txt = open("notification.txt", "r")
			self.txt = self.txt.readline()
		except:
			self.txt = "How can I help you?"
		self.lmain.configure(text=self.txt, justify="center",
		                     font="Helvetica 20 bold", bg="#4DA8DA", fg="#EEFBFB")
		self.lmain.after(1000, self.main_display)

	# Event handlers

	def inserting_option(self):
		self.option.insert(tk.END, "First Lullaby")
		self.option.insert(tk.END, "Second Lullaby")
		self.option.insert(tk.END, "Third Lullaby")
		self.option.insert(tk.END, "Fourth Lullaby")
		self.option.insert(tk.END, "Fifth Lullaby")

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
		elif scrollbar_command == 'Fifth Lullaby':
			print(scrollbar_command)
	def pause_sound(self):
		pub_cmd.publish(client, "pause")
	def resume_sound(self):
		pub_cmd.publish(client, "resume")
	def stop_sound(self):	
		pub_cmd.publish(client, "stop")

	# def listen_cmd(self):
	# 	while self.listen:
	# 		self.audio_conn.recv()
	
	#Displaying Video Stream from own camera
	def video_stream(self):
		# self.video_window = tk.Toplevel(self.window)
		# _, frame = self.cap.read()
		# cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
		# img = Image.fromarray(cv2image)
		# imgtk = ImageTk.PhotoImage(image=img)
		# self.lmain.imgtk = imgtk
		# self.lmain.configure(image=imgtk)
		# self.lmain.after(1, self.video_stream)
		exec(open('vid_gui_client.py').read())

	def handle_click_lullaby(self):
		self.new_window = tk.Toplevel(self.window)
		self.new_window.configure(bg="#4DA8DA")
		# Making a scroll bar display
		self.scroll_bar = tk.Scrollbar(self.new_window)
		self.option = tk.Listbox(self.new_window, bd=0, bg="#007CC7", fg="#EEFBFB",
		                         font="Helvetica 11 bold", yscrollcommand=self.scroll_bar.set)
		self.inserting_option()
		self.option.pack(side=tk.LEFT, fill=tk.BOTH)
		self.scroll_bar.config(command=self.option.yview)

		self.select = tk.Button(self.new_window, text="Play Song", bd=0, bg="#4DA8DA",
		                        fg="#EEFBFB", font="Helvetica 11 bold", command=self.play_sound)
		self.select.pack(fill=tk.BOTH)
		
		self.pause = tk.Button(self.new_window, text="Pause Song", bd=0, bg="#4DA8DA",
		                        fg="#EEFBFB", font="Helvetica 11 bold", command= self.pause_sound)
		self.pause.pack(fill=tk.BOTH)

		self.resume = tk.Button(self.new_window, text="Resume Song", bd=0, bg="#4DA8DA",
		                        fg="#EEFBFB", font="Helvetica 11 bold", command= self.resume_sound)
		self.resume.pack(fill=tk.BOTH)

		self.stop = tk.Button(self.new_window, text="Stop Song", bd=0, bg="#4DA8DA",
		                        fg="#EEFBFB", font="Helvetica 11 bold", command= self.stop_sound)
		self.stop.pack(fill=tk.BOTH)



		self.lmain.configure(text="Button send lullaby was clicked",
		                     justify="center", font="Helvetica 20 bold")

	def handle_click_listen(self):
		self.lmain.configure(text="Button listen was clicked",
		                     justify="center", font="Helvetica 20 bold")
		
		# self.listen = not self.listen
		# if self.listen:
		# 	thread = threading.Thread(target=self.listen_cmd)
		# 	thread.start()

	def quit_the_program(self):
		os.remove("notification.txt")
		sys.exit()


client = pub_cmd.connect_mqtt()
sub_client = sub_cmd.connect_mqtt()
g = GUI()
os.remove("notification.txt")