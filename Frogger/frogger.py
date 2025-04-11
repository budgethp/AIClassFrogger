# REQUIRES PYTHON 3.12.0
import gymnasium as gym
import numpy as np
import tensorflow as tf
from tensorflow import keras
from keras.models import Sequential
from keras.layers import Conv2D, Flatten, Dense
from keras.optimizers import Adam
import cv2
import random
from collections import deque
import time
import os
from ale_py import ALEInterface, roms


env = gym.make("ALE/Frogger-v5", render_mode='rgb_array')


def reduceFrame(frame): # Make frame B&W and slim it down to reduce compute time
    gar=cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)
    crap=gar[12:-30, 7:-7]
    resized = cv2.resize(crap, (84, 110), interpolation=cv2.INTER_AREA)
    return resized 




def build_model(action_size):
    """CNN architecture"""
    model = Sequential()
    model.add(Conv2D(32, (8, 8), strides=(4, 4), activation='relu', input_shape=(210, 160, 1)))
    model.add(Conv2D(64, (4, 4), strides=(2, 2), activation='relu'))
    model.add(Conv2D(64, (3, 3), strides=(1, 1), activation='relu'))
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dense(action_size, activation='linear'))
    
    model.compile(loss='mse', optimizer=Adam(learning_rate=0.00025))
    return model

def makeSnapshotSystem(size=100000): # Make the memory space for snapshots and history tracking
    return deque(maxlen=size)

def addSnapshot(snapshots): # TODO I need to finish this 
    # snapshots.append((state, action, reward, next_state, done))
    pass


def trainModel(episodes=1000 # How many episodes to run
               maxStep=50000 # Max ammount of steps the frog can take before giving up
               
               ):
    pass