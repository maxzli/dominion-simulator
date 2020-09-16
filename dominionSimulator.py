#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 02:00:58 2020

@author: maxzli
"""
from IPython import get_ipython
get_ipython().magic('reset -sf')

from dominionInit import Player
from dominionCards import ACTION_CARDS
from dominionGame import dominion_game
import copy

def displaySupply(actions, selected):
    display = "";
    for i in range(0, 5):
        if actions[i] not in selected:
            display += actions[i] + " "
    display += "\n"
    for i in range(5, 10):
        if actions[i] not in selected:
            display += actions[i] + " "
    print("Supply cards include:\n\n" + display)
    return input("Name a card for strategy, or type DONE to finish: ")

wins = {}

# # first mover advantage simulation
# wins[1] = 0; wins[2] = 0; wins[3] = 0; trials = 1000;
# for trial in range(0, trials):
#     strategy = []; # shared strategy
#     result = dominion_game(Player("first", strategy), Player("second", strategy), Player("third", strategy));
#     if result[0][0] in result[-1]:
#         wins[1] += 1/len(result[-1])
#     if result[1][0] in result[-1]:
#         wins[2] += 1/len(result[-1])
#     if result[2][0] in result[-1]:
#         wins[3] += 1/len(result[-1])
# for winner in wins:
#     wins[winner] = round(wins[winner]/trials, 3)
# print("Strategy:", strategy)
# print("first", wins[1]) 
# print("second", wins[2])
# print("third", wins[3])
# print()
    

# strategy simulation
wins['tester'] = 0; wins['bot1'] = 0; wins['bot2'] = 0; trials = 1000;

temp = ""
actions = []; selected = [];
ACTION_CARDS.sort(key=lambda x: x.getCost(), reverse=True)
for index in range(4, -6, -1):
    actions.append(ACTION_CARDS[index].getName())
strategy = []

while temp != "DONE":
    ## handle displaying 
    temp = displaySupply(actions, selected) # return input
    temp2 = None
    if temp != "DONE" and temp not in actions:
        print("\nInvalid choice!\n")
        
    elif temp in actions:
        while type(temp2) != int and temp2 != "UNDO":
            if temp2 != "UNDO":
                try:
                    temp2 = input("How many? Or type UNDO to go back: ")
                    if temp2 != "UNDO":
                        temp2 = int(temp2)
                except:
                    print('Enter integer')
        if temp2 != "UNDO":
            strategy.append([temp, temp2])
            selected.append(temp)
        print()


for trial in range(0, trials):
    # testerStrategy =  [['Smithy', 6]]
    testerStrategy = strategy
    
    # second player strategy hardcoded
    botStrategy = [['Smithy', 5], ['Festival', 2]]

    # third player only buys treasure and victory points
    noStrategy = [] 
    
    
    tS = Player('tester', copy.deepcopy(testerStrategy))
    nS = Player('bot1', copy.deepcopy(noStrategy))
    bS = Player('bot2', copy.deepcopy(botStrategy))

    result = dominion_game(tS, nS, bS)
    
    for winner in result[-1]:
        wins[winner] += 1/len(result[-1])
for winner in wins:
    wins[winner] = round(wins[winner]/trials, 3)
print(wins['tester'], testerStrategy)
print(wins['bot1'], noStrategy)
print(wins['bot2'], botStrategy)