import tkinter as tk
from PIL import Image, ImageTk
#from imutils.video import VideoStream
import io
import cv2
import sys
#import threading
import os
import light_sub
import moisture_sub
import tkinter as tk

root = tk.Tk()
# Create a frame
app = tk.Frame(root, bg="white")
app.grid()
# Create a label in the frame
lmain = tk.Label(app)
lmain.grid()

window = tk.Tk()
window.geometry("480x480")
#window.configure(bg="#4DA8DA")
window.configure(bg="green")

# Title of GUI
greeting = tk.Label(text="Garden-Protecc by Scarecrow Technologies",font="Helvetica 15 bold", bg="green", fg="#EEFBFB")
greeting.pack()
app = tk.Frame(window)
app.pack()

# Showing the action in the main display
lmain = tk.Label(app)
lmain.grid()



light_disp = tk.Label(window)
light_disp.pack()

light_display()

moisture_disp = tk.Label(window)
moisture_disp.pack()

moisture_display()
# Showing the button in the display
button_frame = tk.Frame(window)
button_frame.configure(bg="#4DA8DA")
button_frame.pack()
button_d = tk.Button(button_frame, text="Quit", font="Helvetica 7 bold",width=14, height=2, bg="white", fg="BLACK", command=quit_the_program)
button_d.pack(side=tk.LEFT, fill=tk.BOTH)
# Capture from camera
cap = cv2.VideoCapture(0)

# function for video streaming
def video_stream():
    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, video_stream)

def light_display(self):
	txt = open("light_notification.txt", "r")
	txt = txt.readline()
	if (txt == ""):
		txt = "..."
	txt = "Light Value: " + txt
	light_disp.configure(text=txt, justify="center",font="Helvetica 20 bold", bg="green", fg="#EEFBFB")
	light_disp.after(1000, light_display)

def moisture_display(self):
	txt = open("moisture.txt", "r")
	txt = txt.readline()
	if (txt == ""):
		txt = "..."
	txt = "Moisture Levels: " + txt
	moisture_disp.configure(text=txt, justify="center",font="Helvetica 20 bold", bg="green", fg="#EEFBFB")
	moisture_disp.after(1000, moisture_display)

video_stream()
root.mainloop()
os.remove("light_notification.txt")
os.remove("moisture_notification.txt")