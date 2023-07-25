#!/usr/bin/env python
# coding: utf-8

# Read in all libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import math
from collections import defaultdict

# First create a function for all possible states from A10B0 to A0B10
# This function will take in an integer and return the string version to represent our state
def new_state(x):
    if len(str(x)) == 1 :
        return '0' + str(x) #need to add this 0 or else the initialization of A and B coins can't read a non base 10 number (noted from error received)
    else: return str(x)


# Simulate the game based on the die roll, with the potential probabilities of each next state (from excel table in the report)
# This function will take a starting state aka A10B0 to A0B10, in our project case, A4B4
# This function will also serve as our transition probability matrix later
def probabilities(state):
    probs = defaultdict(float) #init dictionary to store probabilities in
    
    if state == 'loss': #the ending transition which does not transition to any other state
        probs[state] = 1
        return probs

    a_coins = int(state[1:3])
    b_coins = int(state[4:6])
    pot_coins = 10 - a_coins - b_coins #coins in pot are the remainder from 10 of what A and B have
    
    # Odd turns are Player A's, goes first 
    for i in [1,2,3,4,5,6]:
        if i == 1: #player does nothing
            next_a_coins = new_state(a_coins) 
            next_pot_coins = pot_coins
            
        elif i == 2: #player takes all the coins in the pot
            next_a_coins = new_state(a_coins + pot_coins)
            next_pot_coins = 0
            
        elif i == 3: #player takes half the coins in the pot (rounded down)
            next_a_coins = new_state(a_coins + math.floor(pot_coins/2))
            next_pot_coins = pot_coins - math.ceil(pot_coins/2)
        
        #player rolls a 4,5,6 and has to put 1 coin in the pot but if player does not have a coin to give, 
        #the next transition state must be updated. Note that if Player B still has coins, the turn would go to them
        else:
            if (a_coins == 0 and b_coins > 0):
                probs['loss'] += 1/6 
                continue
            elif (a_coins == 0 and b_coins == 0):
                probs['loss'] += 1/4
                continue
            else:
                next_a_coins = new_state(a_coins - 1)
                next_pot_coins = pot_coins + 1
                
        # Even turns for Player B after Player A's roll - conditionally dep. on Player A
        next_b_coins = new_state(b_coins) #player rolls a 1, does nothing - pot stays the same from before
        probs['A' + next_a_coins + 'B' + next_b_coins] += 1/36
        
        next_b_coins = new_state(b_coins + next_pot_coins) #player rolls a 2, takes pot coins (from player A turns pot)
        probs['A' + next_a_coins + 'B' + next_b_coins] += 1/36
        
        next_b_coins = new_state(b_coins + math.floor(next_pot_coins/2)) #players rolls a 3, takes half pot coins
        probs['A' + next_a_coins + 'B' + next_b_coins] += 1/36
        
        if a_coins > 0 and b_coins == 0:
            probs['loss'] += 1/12
            
        else:
            next_b_coins = new_state(b_coins - 1)
            probs['A' + next_a_coins + 'B' + next_b_coins] += 1/12
            
    return probs

states = ['loss'] #our absorbing state

for i in range(0,11):
    for j in range(0,11):
        if (i + j <= 10): #all possible states of coins
            states.append('A' + new_state(i) + 'B' + new_state(j))
        
print(states) #states will be our keys in the dictionary probs

state_probs = defaultdict(defaultdict) #init empty dictionary

for state in states:
    state_probs[state] = probabilities(state) #populate the values in the dictionaries of probabilities previously for each state

# Create transition matrix P
P = []

for beg_state in states:
    probs = state_probs[beg_state]
    inner = [] 
    
    for loss_state in states: 
        if loss_state in probs.keys(): 
            inner.append(probs[loss_state])
        else:
            inner.append(0)
            
    P.append(inner) 
    
P = np.array(P)

# Create transition matrix diagram using matplotlib 

fig = plt.figure(figsize=(15,15))

ax = fig.add_subplot(111)
ax.set_title('Transition Matrix')
plt.imshow(P, cmap='Blues')
ax.set_aspect('equal')

plt.xticks(x, states, rotation='vertical', fontsize=10)
plt.yticks(x, states, rotation='horizontal', fontsize=10)
plt.xlabel('Starting Transition', fontsize=14)
plt.ylabel('Next Transition', fontsize=14)


# Absorbing and transient states
num_abs = 1
num_trans = P.shape[0] - num_abs

# Select the absorbing and transient states
abs_states = states[:num_abs]
trans_states = states[num_abs:]

Q = P[num_abs:,num_abs:]
R = P[num_abs:,:num_abs]

I = np.eye(num_trans)
N = np.linalg.inv(I - Q) #fundamental matrix N

# Expected cycle lengths

ones = np.ones((num_trans, 1))
t = N @ ones

t.reshape(-1,)

steps = pd.DataFrame({'Starting State': trans_states, 'Expected # of Cycles': t.reshape(-1,)})
steps = steps.sort_values(by=['Expected # of Cycles'], ascending = False) #take this output and bring into excel to get bar graph


