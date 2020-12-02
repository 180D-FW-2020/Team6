#from tutorial: https://realpython.com/python-gui-tkinter/

import tkinter as tk
from PIL import Image, ImageTk

window = tk.Tk()
greeting = tk.Label(text="Night Light Baby Monitor")
greeting.pack(fill=tk.BOTH)
pilfile = Image.open("image.jpg")
image_vid = ImageTk.PhotoImage(pilfile)
video_feed = tk.Label(image=image_vid)
video_feed.pack()
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


# frame_a = tk.Frame()
# frame_a.pack()
# frame_b = tk.Frame()
# frame_b.pack()
# label_a = tk.Label(master=frame_a, text="Frame A")
# label_a.pack()
# label_b = tk.Label(master = frame_b, text = "Frame B")
# label_b.pack()
# label = tk.Label( text = "Hello",fg = "white",bg = "black",width = 10, height = 10)
# label.pack(fill=tk.X) #responsive to window resize
window.mainloop() #runs application
