#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 01:55:40 2020

@author: maxzli
"""

from dominionInit import Card
import random

# helper draw function
def drawDeck(player, number):
    result = []
    while number > 0:
        if not player.deck:
            if not player.discard:
                break
            random.shuffle(player.discard)
            player.deck = player.discard
            player.discard = []
        result.append(player.deck.pop())
        number -= 1
    return result

# Card('Name', cost, kind, specialAction, Effect)
# Card.Effect: [description, +cards, +actions, +buy, +treasure]

# initialize basic setup cards
ACTION_CARDS = [Card('Smithy', 4, 'A', False, ["+3 Cards", 3, 0, 0, 0]), 
                Card('Village', 3, 'A', False, ["+1 Card, +2 Actions", 1, 2, 0, 0]), 
                 Card('Gardens', 4, 'V', False, ["1 VP for every 10 cards (rounded down)", 0, 0, 0, 0]),
                 Card('Militia', 4, 'A', True, ["+2 Treasure, other players discard 2", 0, 0, 0, 2]), # special
                 Card('Bandit', 5, 'A', True, ["Gain a Gold, other players reveal top two cards and trash non-copper treasure", 0, 0, 0, 0]), # special
                 Card('Festival', 5, 'A', False, ["+2 Actions, +1 Buy, +2 Treasure", 0, 2, 1, 2]), 
                 Card('Chapel', 2, 'A', True, ["Trash up to 4 cards from hand", 0, 0, 0, 0]), # special
                 Card('Market', 5, 'A', False, ["+1 Card, +1 Action, +1 Buy, +1 Treasure", 1, 1, 1, 1]), 
                 Card('Witch', 5, 'A', True, ["+2 Cards, Other players receive a curse", 2, 0, 0, 0]), # special
                 Card('Moneylender', 4, 'A', True, ["Trash a copper for 3 treasure", 0, 0, 0, 0])] # special

OTHER_SUPPLY = [Card('Province', 8, 'V', False, []), 
                Card('Duchy', 5, 'V', False, []), 
                Card('Estate', 2, 'V', False, []),
                Card('Curse', 0, 'C', False, []), 
                Card('Gold', 6, 'T', False, []), 
                Card('Silver', 3, 'T', False, []), 
                Card('Copper', 0, 'T', False, [])]


def Chapel(myself, oppos, supply, trash):
    temp = [];
    for card in myself.treasures:
        if card.getName() != "Copper":
            temp.append(card)
        else:
            trash.append(card)
    myself.treasures = temp; 
    
    temp = [];
    for card in myself.victories:
        if card.getName() != "Estate":
            temp.append(card)
        else:
            trash.append(card)
    myself.victories = temp;
    return [0]*4
                
    
def Moneylender(myself, oppos, supply, trash):
    for i in range(0, len(myself.treasures)):
        if myself.treasures[i].getName() == "Copper":
            trash.append(myself.treasures.pop(i))
            return [0, 0, 0, 3]
    return [0] * 4

def Bandit(myself, oppos, supply, trash):
    if supply['Gold'][0] > 0:
        myself.gain('Gold', supply)

    for oppo in oppos:
        temp = drawDeck(oppo, 2)
        temp.sort(key=lambda x: x.getCost())
        if temp[0].getKind() == 'T' and temp[0].getName() != "Copper":
            trash.append(temp[0]);
            oppo.discard.append(temp[1])
        elif temp[1].getKind() == 'T' and temp[1].getName() != "Copper":
            trash.append(temp[1]);
            oppo.discard.append(temp[0])
        else:
            oppo.discard.extend(temp)
    return [0] * 4
    
    
def Militia(myself, oppos, supply, trash):
    for oppo in oppos:
        oppo.discardHand(2);
    return [0, 0, 0, 2]

def Witch(myself, oppos, supply, trash):
    for oppo in oppos:
        if supply['Curse'][0] > 0:
            oppo.gain('Curse', supply)
    return [2, 0, 0, 0]