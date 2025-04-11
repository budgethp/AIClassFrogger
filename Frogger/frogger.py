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


def trainModel(episodes=1000, #How many episodes to run
               maxStep=50000): #Uhh i think this is how many steps it can take
    action_size = env.action_space.n
    model = build_model(action_size)
    target_model = build_model(action_size)
    target_model.set_weights(model.get_weights())

    memory = makeSnapshotSystem()
    
    gamma = 0.99
    epsilon = 1.0
    epsilon_min = 0.1
    epsilon_decay = 0.995
    batch_size = 32
    update_target_freq = 10 

    for episode in range(episodes):
        state_raw, _ = env.reset()
        state = reduceFrame(state_raw)
        state = np.expand_dims(state, axis=-1) 
        done = False
        total_reward = 0
        step = 0

        while not done and step < maxStep:
            step += 1

            if random.random() < epsilon:
                action = random.randint(0, action_size - 1)
            else:
                q_values = model.predict(np.expand_dims(state, axis=0), verbose=0)
                action = np.argmax(q_values[0])

            next_state_raw, reward, terminated, truncated, _ = env.step(action)
            done = terminated or truncated
            next_state = reduceFrame(next_state_raw)
            next_state = np.expand_dims(next_state, axis=-1)

            memory.append((state, action, reward, next_state, done))
            state = next_state
            total_reward += reward

            if len(memory) >= batch_size:
                minibatch = random.sample(memory, batch_size)
                states = np.array([m[0] for m in minibatch])
                actions = np.array([m[1] for m in minibatch])
                rewards = np.array([m[2] for m in minibatch])
                next_states = np.array([m[3] for m in minibatch])
                dones = np.array([m[4] for m in minibatch])

                target_qs = target_model.predict(next_states, verbose=0)
                targets = model.predict(states, verbose=0)

                for i in range(batch_size):
                    if dones[i]:
                        targets[i][actions[i]] = rewards[i]
                    else:
                        targets[i][actions[i]] = rewards[i] + gamma * np.max(target_qs[i])

                model.fit(states, targets, epochs=1, verbose=0)

        if epsilon > epsilon_min:
            epsilon *= epsilon_decay

        if episode % update_target_freq == 0:
            target_model.set_weights(model.get_weights())

        print(f"Episode {episode}: Total Reward = {total_reward:.2f}, Epsilon = {epsilon:.3f}")
    
    
    pass