import pandas as pd
import gymnasium as gym
import os
from ale_py import ALEInterface, roms
import time
import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import asyncio


class FrameManagment:
    __frameArray = [] # The main array for frames this is our timeline
    __frames = 0  # Variable for the ammount of frames that have passed reguardless of the episode count
    __actionArray = [] # Integer Array for possible actions arranged in a list ex: [1, 2, 3, 4] for up down left right respectfully 
                        # this is used in the direction formatting ex: up() will run action __actionArray[0] so it will run whatever action is associated with 1 in gymnasium
    frameCounter = 0 # The current frame being displayed
    PIL_image = None # Variable to define the current displayed image in PhotoImage format
    __gymEnv = None # Gymnasium environment
    __frameHistory = None # ammount of frame history to keep
    
    """
    Setup for the class

    @param Action array as described above
    @param gymEnv The gym environment to use (this is designed for the frogger one)
    @param history Ammount of frames to keep in the history
    @return None
    """
    def __init__(self, actionArray, gymEnv, history=100):
        self.__actionArray = actionArray
        self.__frameHistory = history


    """
    Generate a frame return it and add it to the frame array

    @param action Action to be preformed
    @return rgb_array the frame represented in an array of RGB
    """
    def _runAction(self, action):
        new_state, reward, terminated, truncated, info = self.__gymEnv.step(action) # Take the action and apply it
        return self.__gymEnv.render()
    

    """
    Add a frame to the frame array for later use

    @param frame Frame to be added
    @return None
    """
    def addFrame(self, frame):
        if len(self.__frameArray)-1 >= self.__frameHistory:
            self.__frameArray = self.__frameArray.pop(0) # remove the oldest frame in the list 
        self.__frameArray.append(frame) # Add the most recent frame to the array

        self.frameCounter = len(self.__frameArray)-1 # Update the frame counter to be on our current frame


    


