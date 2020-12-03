#from tutorial: https://realpython.com/python-gui-tkinter/

import tkinter as tk
from PIL import Image, ImageTk
from imutils.video import VideoStream
import io
import cv2

window = tk.Tk()

#Title of GUI
greeting = tk.Label(text="Night Light Baby Monitor")
greeting.pack(fill=tk.BOTH)

#Displaying an image
#pilfile = Image.open("image.jpg")
#image_vid = ImageTk.PhotoImage(pilfile)
#video_feed = tk.Label(image=image_vid)
#video_feed.pack()

#Displaying Video Stream from own camera
app = tk.Frame(window, bg = "white")
app.pack()
lmain = tk.Label(app)
lmain.pack()
cap = cv2.VideoCapture(0)
def video_stream():
	_,frame = cap.read()
	cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
	img = Image.fromarray(cv2image)
	imgtk = ImageTk.PhotoImage(image=img)
	lmain.imgtk = imgtk
	lmain.configure(image=imgtk)
	lmain.after(1, video_stream)
video_stream()

#creating buttons and event handlers
button_a = tk.Button(text = "Play lullaby", height = 5, bg = "blue", fg = "yellow")
button_b = tk.Button(text = "send audio", height = 5, bg = "blue", fg = "yellow")
button_a.pack(side = tk.LEFT)
#event handler
def handle_click_lullaby(event):
	print("button send lullaby was clicked")
def handle_click_send_audio(event):
	print("button send audio was clicked")
button_a.bind("<Button-1>",handle_click_lullaby) #button-1 is left click event
button_b.bind("<Button-1>",handle_click_send_audio)
button_b.pack(side=tk.LEFT)




window.mainloop() #runs application