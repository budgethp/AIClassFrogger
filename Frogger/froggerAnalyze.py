import pandas as pd
import gymnasium as gym
import os
from ale_py import ALEInterface, roms
import time
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import asyncio
import tk_async_execute as tae
runLoop = True
action = 0

env = gym.make("ALE/Frogger-v5", render_mode='rgb_array', frameskip=2)

initial_state = env.reset()


def run_action():
    global env
    global action
    # Take a step (0: NOTHING, 1: UP, 2: RIGHT, 3: LEFT, 4: DOWN)
    new_state, reward, terminated, truncated, info = env.step(action)
    print(action)

    return env.render()

def update_image():
    global label1
    PIL_image = Image.fromarray(np.uint8(run_action())).convert('RGB')
    tk_image = ImageTk.PhotoImage(PIL_image.resize((PIL_image.width*2, PIL_image.height*2)))
    label1.configure(image=tk_image)
    label1.image = tk_image


def update_image_continue():
    global label1
    global runLoop


    PIL_image = Image.fromarray(np.uint8(run_action())).convert('RGB')
    tk_image = ImageTk.PhotoImage(PIL_image.resize((PIL_image.width*2, PIL_image.height*2)))
    label1.configure(image=tk_image)
    label1.image = tk_image
    if runLoop:
        root.after(10, update_image_continue)
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
    env.reset()
    exit()

def up(no):
    global action
    action = 1
    update_image()
    action = 0
    update_image()

def down(no):
    global action
    action = 4
    update_image()
    action = 0
    update_image()

def left(no):
    global action
    action = 3
    update_image()
    action = 0
    update_image()

def right(no):
    global action
    action = 2
    update_image()
    action = 0
    update_image()




# make the window
root = tk.Tk()
root.geometry("500x600")
#root.mainloop()

#convert array to PiL Image    
PIL_image = Image.fromarray(np.uint8(run_action())).convert('RGB')

tk_image = ImageTk.PhotoImage(PIL_image.resize((PIL_image.width*2, PIL_image.height*2)))
label1 = tk.Label(image=tk_image )
label1.place(x=0, y=0)


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


direction = ["<Up>", "<Right>", "<Left>", "<Down>"]
function = [up, right, left,  down]
for x in range(4):
    # make 4 buttons up down left right
    #tk.Button(root, text=direction[x], command=function[x]).pack(expand=tk.FALSE, fill=tk.X, anchor="se", side="bottom")
    root.bind(direction[x], function[x])





stop.configure(state="disabled")
tae.start()
root.mainloop()


time.sleep(5)

env.reset()
env.close()