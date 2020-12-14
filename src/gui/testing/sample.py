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


class GUI:
	def __init__(self):

		self.window = tk.Tk()
		
		# Title of GUI
		self.greeting = tk.Label(text="Night Light Baby Monitor")
		self.greeting.pack(fill=tk.BOTH)
		self.app = tk.Frame(self.window, bg = "black")
		self.app.pack()
		
		# Showing the action in the display
		self.lmain = tk.Label(self.app, bg = "white")
		self.lmain.pack()
		
		# Setting the main display
		self.lmain.configure(text = "How can I help you?", justify = "center", font = "Helvetica 20 bold", bg = "white")
		
		# Showing the button in the display
		self.button_frame = tk.Frame(self.window)
		self.button_frame.pack()

		# Inserting a rounded button for MIC
		self.loadimage = tk.PhotoImage(file = "mic2.png")
		# Creating buttons
		self.button_a = tk.Button(self.button_frame, text = "Watch the baby", height = 5, bg = "blue", fg = "yellow", command = self.video_stream)
		self.button_b = tk.Button(self.button_frame, text = "Play lullaby", height = 5, bg = "blue", fg = "yellow", command = self.handle_click_lullaby)
		self.button_c = tk.Button(self.button_frame, text = "Hearing the baby", height = 5, bg = "blue", fg = "yellow", command = self.handle_click_send_audio)
		self.button_d = tk.Button(self.button_frame, text = "Send Voice Message", image = self.loadimage, bg = "white", borderwidth = "0", compound = "bottom")
		self.button_e = tk.Button(self.button_frame, text = "Quit", height = 5, bg = "blue", fg = "yellow", command = self.quit_the_program)
		
		self.button_a.pack(side = tk.LEFT)
		self.button_b.pack(side = tk.LEFT)
		self.button_c.pack(side = tk.LEFT)
		self.button_d.pack(side = tk.RIGHT)
		self.button_e.pack(side = tk.LEFT)
		# Video Streaming
		self.cap = cv2.VideoCapture(0)
		
		self.window.mainloop() #runs application
		#Displaying an image
		#pilfile = Image.open("image.jpg")
		#image_vid = ImageTk.PhotoImage(pilfile)
		#video_feed = tk.Label(image=image_vid)
		#video_feed.pack()

	# Event handlers
	
	#Displaying Video Stream from own camera
	def video_stream(self):
		# _,frame = self.cap.read()
		# cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
		# img = Image.fromarray(cv2image)
		# imgtk = ImageTk.PhotoImage(image=img)
		# self.lmain.imgtk = imgtk
		# self.lmain.configure(image=imgtk)
		# self.lmain.after(1, self.video_stream)
		
	
	def handle_click_lullaby(self):
		self.lmain.configure(text = "Button send lullaby was clicked", justify = "center", font = "Helvetica 20 bold")
		pub_cmd.publish(client, "lullaby1.mp3")
	
	def handle_click_send_audio(self):
		self.lmain.configure(text = "Button send audio was clicked", justify = "center", font = "Helvetica 20 bold")

	def quit_the_program(self):
		sys.exit()

client = pub_cmd.connect_mqtt()
g = GUI()
