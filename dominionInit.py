#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 01:47:06 2020

@author: maxzli
"""

import random

# definitions for Player, Card
# player supports: province, duchy, estate victory cards only
    # drawHand, buy, totalPoints


# card supports: only +cards, +actions, +buy, +treasure
    # playCard

class Player:
    def __init__(self, name, strategy = None):
        self.name = name;
        self.turns = 0;
        self.deck = [];
        self.discard = [];
        self.hand = [];
        if strategy:
            for i in range(len(strategy)-1, -1, -1):
                if strategy[i][1] <= 0:
                    strategy.pop(i)
        self.strategy = strategy
        
        
        self.terminalactions = []
        self.nontermactions = []
        self.treasures = []
        self.victories = []
        self.curses = []
                

        # initialize deck cards
        for i in range(0, 7):
            self.deck.append(Card('Copper', 0, 'T', False, []))
        for i in range(0, 3):
            self.deck.append(Card('Estate', 2, 'V', False, []))
        random.shuffle(self.deck)
        for i in range(0, 5):
            self.hand.append(self.deck.pop())
            
    def __repr__(self):
        return self.name
    
    def showAll(self): print(self.deck + self.discard + self.hand)
    
    def getName(self): return self.name
    def getHand(self): return self.hand
    
    def discardHand(self, number):
        self.hand.sort(key=lambda x: x.getCost(), reverse=True)
        for i in range(number-1, -1, -1):
            self.discard.append(self.hand.pop(i))
    def drawHand(self, number):
        while number > 0:
            if not self.deck:
                if not self.discard:
                    break
                random.shuffle(self.discard)
                self.deck = self.discard
                self.discard = []
            self.hand.append(self.deck.pop())
            number -= 1
            
    def gain(self, cardName, supply): # assuming supply pile not empty
        supply[cardName][0] -= 1;
        card = supply[cardName][1].deepCopy()
        self.discard.append(card)
        # print(card.getName() + ' gained!')
        
    def totalPoints(self):
        points = 0
        # print(self.getName())
        # self.showAll()
        
        for card in self.deck + self.discard + self.hand:
            # print(card)
            if card.getName() == 'Province':
                points += 6
            elif card.getName() == 'Duchy':
                points += 3
            elif card.getName() == 'Estate':
                points += 1
            elif card.getName() == 'Curse':
                points += -1
            elif card.getName() == 'Gardens':
                points += len(self.deck+self.discard+self.hand)//10
        return points


class Card: # card in the game
    def __init__(self, name, cost, kind, specialAction, effect):
        self.name = name;
        self.cost = cost;
        self.kind = kind;
        self.specialAction = specialAction;
        self.actionEffect = None;
        self.effect = effect; # ["description", +cards, +actions, +buy, +treasure]
    def __repr__(self): return self.name
    
    def getKind(self): return self.kind
    def getName(self): return self.name
    def getCost(self): return self.cost
    def getSpecial(self): return self.specialAction
    
    def playCard(self):
        return self.effect[1:]
    def getDescription(self):
        return self.effect[0]
    def deepCopy(self):
        effect = self.effect
        return Card(self.name, self.cost, self.kind, self.specialAction, effect)