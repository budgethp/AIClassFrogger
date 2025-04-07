import pandas as pd
import gymnasium as gym
import os
from ale_py import ALEInterface, roms
import time
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import asyncio
import FrameManagment as Frogger
runLoop = True
action = 0

frog = Frogger.FrameManagment([1,4,3,2], gym.make("ALE/Frogger-v5", render_mode='rgb_array'))



def update_image():
    global frog
    global label1
    frog.addFrameAndRunAction(0)
    PIL_image = frog.renderFrame()
    tk_image = ImageTk.PhotoImage(PIL_image.resize((PIL_image.width*3, PIL_image.height*3)))
    label1.configure(image=tk_image)
    label1.image = tk_image


def update_image_no_action():
    global frog
    global label1
    PIL_image = frog.renderFrame()
    tk_image = ImageTk.PhotoImage(PIL_image.resize((PIL_image.width*3, PIL_image.height*3)))
    label1.configure(image=tk_image)
    label1.image = tk_image


def update_image_continue():
    global label1
    global runLoop
    global frog

    frog.addFrameAndRunAction(0)
    PIL_image = frog.renderFrame()
    tk_image = ImageTk.PhotoImage(PIL_image.resize((PIL_image.width*3, PIL_image.height*3)))
    label1.configure(image=tk_image)
    label1.image = tk_image
    if runLoop:
        root.after(33, update_image_continue)
    else: runLoop = True; return

def run_image_continue_start():
    global run
    global stop
    run.configure(state="disabled")
    stop.configure(state="active")
    update_image_continue()


def stop_image():
    global runLoop
    global run
    global stop
    run.configure(state="normal")
    stop.configure(state="disabled")
    runLoop = False

def quit_program():
    global root, env
    root.destroy()
    root.quit()
    exit()

def up(no):
    global frog
    frog.up()
    update_image_no_action()

def down(no):
    global frog
    frog.down()
    update_image_no_action()

def left(no):
    global frog
    frog.left()
    update_image_no_action()

def right(no):
    global frog
    frog.right()
    update_image_no_action()

def saveImage():
    global frog
    frog.renderFrame().save("Frogger/debugger/frog.png")




# make the window
root = tk.Tk()
root.geometry("700x800")
#root.mainloop()

# quit button
quit = tk.Button(root, text='Stop Program', command=quit_program)
quit.pack(expand=tk.FALSE, fill=tk.X, anchor="se", side="bottom")

# create button to generate new frame
saveBtn = tk.Button(root, text='New Frame', command=update_image)
saveBtn.pack(expand=tk.FALSE, fill=tk.X, anchor="se", side="bottom")
#saveBtn.place(relx=1.0, rely=1.0, anchor="se")

# Run Continuis
run = tk.Button(root, text='Start', command=run_image_continue_start)
run.pack(expand=tk.FALSE, fill=tk.X, anchor="se", side="bottom")
#run.place(relx=1.0, rely=1.0, anchor="se")

stop = tk.Button(root, text='Stop', command=stop_image)
stop.pack(expand=tk.FALSE, fill=tk.X, anchor="se", side="bottom")

tmp = tk.Button(root, text='Save Image as frog.png', command=saveImage)
tmp.pack(expand=tk.FALSE, fill=tk.X, anchor="se", side="bottom")

frameCounter = tk.Text(root, height=2, width=5)
frameCounter.pack(expand=tk.FALSE, fill=tk.X, anchor="ne", side="right")
frameCounter.insert(
    index='1.0', 
    chars= 'Frame Counter'
)

#convert array to PiL Image  
frog.addFrameAndRunAction(0)
PIL_image = frog.renderFrame()

tk_image = ImageTk.PhotoImage(PIL_image.resize((PIL_image.width*3, PIL_image.height*3)))
label1 = tk.Label(image=tk_image )
label1.place(x=0, y=0)





direction = ["<Up>", "<Right>", "<Left>", "<Down>"]
function = [up, right, left,  down]
for x in range(4):
    # make 4 buttons up down left right
    #tk.Button(root, text=direction[x], command=function[x]).pack(expand=tk.FALSE, fill=tk.X, anchor="se", side="bottom")
    root.bind(direction[x], function[x])





stop.configure(state="disabled")
root.mainloop()


time.sleep(5)

