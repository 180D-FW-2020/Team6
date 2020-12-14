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
import sub_cmd
import pub_cmd


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
		if sub_cmd.get_mes() == None:
			txt = "How can I help you?"
		else:
			txt = sub_cmd.get_mes()
		self.lmain.configure(text=txt, justify="center",
		                     font="Helvetica 20 bold", bg="#4DA8DA", fg="#EEFBFB")

		# Showing the button in the display
		self.button_frame = tk.Frame(self.window)
		self.button_frame.configure(bg="#4DA8DA")
		self.button_frame.pack()

		# Inserting a rounded button for MIC
		# self.loadimage = tk.PhotoImage(file = "mic2.png")

		# Creating buttons
		self.button_a = tk.Button(self.button_frame, text="Watch the baby", font="Helvetica 11 bold",
		                          width=14, height=5, bg="#203647", fg="#EEFBFB", command=self.video_stream)
		self.button_b = tk.Button(self.button_frame, text="Play lullaby", font="Helvetica 11 bold",
		                          width=14, height=5, bg="#203647", fg="#EEFBFB", command=self.handle_click_lullaby)
		self.button_c = tk.Button(self.button_frame, text="Hearing the baby", font="Helvetica 11 bold",
		                          width=14, height=5, bg="#203647", fg="#EEFBFB", command=self.handle_click_send_audio)
		# self.button_d = tk.Button(self.button_frame, text = "Send Voice Message", image = self.loadimage, bg = "#203647",fg = "#EEFBFB", borderwidth = "0", compound = "bottom")
		self.button_d = tk.Button(self.button_frame, text="Quit", font="Helvetica 11 bold",
		                          width=14, height=5, bg="#203647", fg="#EEFBFB", command=self.quit_the_program)

		self.button_a.pack(side=tk.LEFT, fill=tk.BOTH)
		self.button_b.pack(side=tk.LEFT, fill=tk.BOTH)
		self.button_c.pack(side=tk.LEFT, fill=tk.BOTH)
		# self.button_d.pack(side = tk.RIGHT)
		self.button_d.pack(side=tk.LEFT, fill=tk.BOTH)
		# Video Streaming
		self.cap = cv2.VideoCapture(0)

		self.window.mainloop()  # runs application

		#Displaying an image
		#pilfile = Image.open("image.jpg")
		#image_vid = ImageTk.PhotoImage(pilfile)
		#video_feed = tk.Label(image=image_vid)
		#video_feed.pack()

	# Event handlers

	def inserting_option(self):
		self.option.insert(tk.END, "First Lullaby")
		self.option.insert(tk.END, "Second Lullaby")
		self.option.insert(tk.END, "Third Lullaby")
		self.option.insert(tk.END, "Fourth Lullaby")
		self.option.insert(tk.END, "Fifth Lullaby")

	def get_scrollbar_command(self):
		scrollbar_command = self.option.get('active')
		if scrollbar_command == 'First Lullaby':
			pub_cmd.publish(client, "lullaby.mp3")
		elif scrollbar_command == 'Second Lullaby':
			print(scrollbar_command)
		elif scrollbar_command == 'Third Lullaby':
			print(scrollbar_command)
		elif scrollbar_command == 'Fourth Lullaby':
			print(scrollbar_command)
		elif scrollbar_command == 'Fifth Lullaby':
			print(scrollbar_command)
		
	#Displaying Video Stream from own camera

	def video_stream(self):
		_, frame = self.cap.read()
		cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
		img = Image.fromarray(cv2image)
		imgtk = ImageTk.PhotoImage(image=img)
		self.lmain.imgtk = imgtk
		self.lmain.configure(image=imgtk)
		self.lmain.after(1, self.video_stream)
<<<<<<< HEAD

=======
		
	
>>>>>>> 11b230c6de189976a082b8a8cf47383bc7315072
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

		self.select = tk.Button(self.new_window, text="Select", bd=0, bg="#4DA8DA",
		                        fg="#EEFBFB", font="Helvetica 11 bold", command=self.get_scrollbar_command)
		self.select.pack(fill=tk.BOTH)

		self.lmain.configure(text="Button send lullaby was clicked",
		                     justify="center", font="Helvetica 20 bold")

	def handle_click_send_audio(self):
		self.lmain.configure(text="Button send audio was clicked",
		                     justify="center", font="Helvetica 20 bold")

	def quit_the_program(self):
		sys.exit()


client = pub_cmd.connect_mqtt()
g = GUI()
