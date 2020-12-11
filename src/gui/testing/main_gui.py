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
import pub_cmd
import subprocess
import os

class GUI:
	def __init__(self):

		self.window = tk.Tk()
		self.window.geometry("470x550")
		self.window.configure(bg = "#4DA8DA")
		
		# Title of GUI
		self.greeting = tk.Label(text="Night Light Baby Monitor", font = "Helvetica 20 bold", bg = "#4DA8DA", fg = "#EEFBFB")
		self.greeting.pack(fill=tk.BOTH)
		self.app = tk.Frame(self.window)
		self.app.pack()
		
		# Showing the action in the display
		self.lmain = tk.Label(self.app)
		self.lmain.pack()
		
		# Setting the main display
		self.lmain.configure(text = "How can I help you?", justify = "center", font = "Helvetica 20 bold", bg = "#4DA8DA", fg = "#EEFBFB")
		
		# Showing the button in the display
		self.button_frame = tk.Frame(self.window)
		self.button_frame.configure(bg = "#4DA8DA")
		self.button_frame.pack()

		# Inserting a rounded button for MIC
		# self.loadimage = tk.PhotoImage(file = "mic2.png")
		
		# Creating buttons
		self.button_a = tk.Button(self.button_frame, text = "Watch the baby", font = "Helvetica 11 bold", width = 14, height = 5, bg = "#203647", fg = "#EEFBFB", command = self.video_stream)
		self.button_b = tk.Button(self.button_frame, text = "Play lullaby", font = "Helvetica 11 bold", width = 14, height = 5, bg = "#203647", fg = "#EEFBFB", command = self.handle_click_lullaby)
		self.button_c = tk.Button(self.button_frame, text = "Hearing the baby", font = "Helvetica 11 bold", width = 14, height = 5, bg = "#203647", fg = "#EEFBFB", command = self.handle_click_send_audio)
		# self.button_d = tk.Button(self.button_frame, text = "Send Voice Message", image = self.loadimage, bg = "#203647",fg = "#EEFBFB", borderwidth = "0", compound = "bottom")
		self.button_d = tk.Button(self.button_frame, text = "Quit", font = "Helvetica 11 bold", width = 14, height = 5, bg = "#203647", fg = "#EEFBFB", command = self.quit_the_program)
		
		
		self.button_a.pack(side = tk.LEFT)
		self.button_b.pack(side = tk.LEFT)
		self.button_c.pack(side = tk.LEFT)
		# self.button_d.pack(side = tk.RIGHT)
		self.button_d.pack(side = tk.LEFT)

		# Video Streaming
		# self.cap = cv2.VideoCapture(0)
		
		self.window.mainloop() #runs application
		#Displaying an image
		#pilfile = Image.open("image.jpg")
		#image_vid = ImageTk.PhotoImage(pilfile)
		#video_feed = tk.Label(image=image_vid)
		#video_feed.pack()

	# Event handlers
	
	#Displaying Video Stream from own camera
	def video_stream(self):
		os.chdir("../../video_processing/stream_client")
		os.system("vid_gui_client.py")
		# _,frame = self.cap.read()
		# cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
		# img = Image.fromarray(cv2image)
		# imgtk = ImageTk.PhotoImage(image=img)
		# self.lmain.imgtk = imgtk
		# self.lmain.configure(image=imgtk)
		# self.lmain.after(1, self.video_stream)
	
	def handle_click_lullaby(self):
		self.new_window = tk.Toplevel(self.window)
		self.lmain.configure(text = "Button send lullaby was clicked", justify = "center", font = "Helvetica 20 bold")
		pub_cmd.publish(client, "lullaby1.mp3")
	
	def handle_click_send_audio(self):
		self.lmain.configure(text = "Button send audio was clicked", justify = "center", font = "Helvetica 20 bold")

	def quit_the_program(self):
		sys.exit()

client = pub_cmd.connect_mqtt()
g = GUI()
