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
    __timeSkipActive = False # If a time skip is in progress so no frames can be rendered as the frameCounter is off
    
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
        self.__gymEnv = gymEnv
        self.__gymEnv.reset()


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
    @return int
    """
    def addFrameAndRunAction(self, action):
        if self.__timeSkipActive:
            return 100 # return error
        
        frame = self._runAction(action)

        if len(self.__frameArray)-1 >= self.__frameHistory:
            del self.__frameArray[0]

        self.__frameArray.append(frame) # Add the most recent frame to the array

        self.frameCounter = len(self.__frameArray)-1 # Update the frame counter to be on our current frame

        return 0 # Return success
        
    """
    Changes the frame that is being displayed as to go backwards in time

    @param frameNumber The frame number > 0 < len(__frameArray)
    @return int
    """
    def changeFrameTime(self, frameNumber):
        if frameNumber >= 0 and frameNumber <= len(self.__frameArray)-1:
            self.frameCounter = frameNumber # set the currently viewed frame
            self.__timeSkipActive = True
            return 0 # return success
        return 100 # reuturn error
    

    """
    Changes the frame counter to be at the most up to date frame to continue rendering frames

    @param None
    @return int
    """
    def resetFrameCount(self):
        self.frameCounter = len(self.__frameArray)-1 # Set frame counter to latest
        self.__timeSkipActive = False # Enable adding frames again
        return 0 


    """
    Render the frame denoted in frameCounter to image format

    @param None
    @return Pillow image
    """
    def renderFrame(self):
        self.PIL_image = Image.fromarray(np.uint8(self.__frameArray[self.frameCounter])).convert('RGB') # Render frame to Pillow Image
        return self.PIL_image
    

    """
    Moves player up
    """
    def up(self):
        return self.addFrameAndRunAction(self.__actionArray[0])
    

    """
    Moves player down
    """
    def down(self):
        return self.addFrameAndRunAction(self.__actionArray[1])
    

    """
    Moves player left
    """
    def left(self):
        return self.addFrameAndRunAction(self.__actionArray[2])
    

    """
    Moves player right
    """
    def right(self):
        return self.addFrameAndRunAction(self.__actionArray[3])

