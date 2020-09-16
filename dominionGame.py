#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 16:54:28 2020

@author: maxzli

"""

import random

from dominionCards import ACTION_CARDS, OTHER_SUPPLY
import dominionCards


# game simulator
def dominion_game(tester, bot1, bot2):
    # dominion_game returns a result list of
    # [(name, turnCount, totalScore), (name, turnCount, totalScore), (name, turnCount, totalScore), winnerName]
    
    
    # handle the type of card
    def processCard(card, terminalactions, nontermactions, treasures, victories, curses):
        if card.getKind() == 'A':
            if card.playCard()[1] > 0:
                nontermactions.append(card)
            else:
                terminalactions.append(card)
        elif card.getKind() == 'T': 
            treasures.append(card)
        elif card.getKind() == 'V':
            victories.append(card)
        else:
            curses.append(card)
        return
    
    
    # supply dictionary tracks count
    supply = {}; # supply[card name] = (count, card)
    for card in ACTION_CARDS:
        if card.getKind() == 'A':
            supply[card.getName()] = [10, card] # 10 action cards
        elif card.getKind() == 'V':
            supply[card.getName()] = [12, card] # 12 victory cards
            
    for card in OTHER_SUPPLY:
        supply[card.getName()] = [0, card]
    for card in [('Province', 12), ('Duchy', 12), ('Estate', 12), ('Curse', 20), ('Gold', 30), ('Silver', 40), ('Copper', 39)]:
        supply[card[0]][0] = card[1]
    
    
    players = [tester, bot1, bot2]; random.shuffle(players)
    turn = 0; overallTurn = 0; emptyCount = 0; trash = [];
    
    while(emptyCount < 3 and supply['Province'][0] > 0):
        inPlay = [];
        turnCards = 0; turnActions = 1; turnBuys = 1; turnTreasure = 0;
        player = players[turn]

        while players[turn].getHand(): # process initial hand
            card = players[turn].getHand().pop();
            processCard(card, player.terminalactions, player.nontermactions, player.treasures, player.victories, player.curses)    
        
        while (turnActions > 0 and (player.nontermactions or player.terminalactions)) or turnCards > 0: # action phase
            if turnCards > 0: # check to draw cards
                players[turn].drawHand(turnCards)
                turnCards = 0
                while players[turn].getHand():
                    card = players[turn].getHand().pop()
                    processCard(card, player.terminalactions, player.nontermactions, player.treasures, player.victories, player.curses)
            if player.nontermactions or player.terminalactions:
                if player.nontermactions: # play these first
                    card = player.nontermactions.pop()
                elif player.terminalactions:
                    card = player.terminalactions.pop()
                if (card.getSpecial()):
                    play = getattr(dominionCards, card.getName())(players[turn], [players[(turn+1)%3], players[(turn+2)%3]], supply, trash)
                else:
                    play = card.playCard();
                turnCards += play[0]; turnActions += play[1];
                turnBuys += play[2]; turnTreasure += play[3];
                
                
                turnActions -= 1
                inPlay.append(card)
        
        player.terminalactions, player.nontermactions = [], []
            
        while player.treasures: # process treasures
            treasure = player.treasures.pop()
            if treasure.getName() == 'Gold':
                turnTreasure += 3;
            elif treasure.getName() == 'Silver':
                turnTreasure += 2;
            else:
                turnTreasure += 1;
            inPlay.append(treasure)
        player.treasures = []
        
        while turnBuys > 0: # buy phase
            if turnTreasure >= supply['Province'][1].getCost() and supply['Province'][0] > 0:
                players[turn].gain('Province', supply); turnTreasure -= supply['Province'][1].getCost()
                
            elif turnTreasure >= supply['Gold'][1].getCost() and supply['Gold'][0] > 0:
                players[turn].gain('Gold', supply); turnTreasure -= supply['Gold'][1].getCost()
                
            elif players[turn].strategy:
            # and turnTreasure == supply[players[turn].strategy[0][0]][1].getCost():
                for card in players[turn].strategy:
                    if supply[card[0]][0] > 0 and turnTreasure >= supply[card[0]][1].getCost():
                        players[turn].gain(card[0], supply); turnTreasure -= supply[card[0]][1].getCost()
                        card[1] -= 1;
                        if card[1] <= 0:
                            players[turn].strategy.pop(0)
                        break

            elif supply['Province'][0] <= 5 :
                if supply['Duchy'][0] > 0 and turnTreasure >= supply['Duchy'][1].getCost():
                    players[turn].gain('Duchy', supply); turnTreasure -= supply['Duchy'][1].getCost()
                elif supply['Estate'][0] > 0 and turnTreasure >= supply['Estate'][1].getCost():
                    players[turn].gain('Estate', supply); turnTreasure -= supply['Estate'][1].getCost()
                    
            elif turnTreasure >= supply['Silver'][1].getCost() and supply['Silver'][0] > 0:
                players[turn].gain('Silver', supply); turnTreasure -= supply['Silver'][1].getCost()
            turnBuys -= 1
        
        if inPlay:
            players[turn].discard.extend(inPlay)
        
        players[turn].discard.extend(player.victories + player.curses)
        player.victories, player.curses = [], []
        players[turn].drawHand(5)
        overallTurn += 1
        turn = (turn+1)%3
    
    result = []; highscore = -100; winner = ""; winnerTurns = 9999;
    for player in players:
        turnCount = overallTurn//3
        if turn > 0:
            turnCount += 1
            turn -= 1
        temp = (player.getName(), turnCount, player.totalPoints())
        result.append(temp)
        
        if temp[2] > highscore:
            highscore = temp[2];
            winnerTurns = turnCount;
            winner = [temp[0]]
        elif temp[2] == highscore:
            if turnCount < winnerTurns:
                winner = [player.getName()]
            else:
                winner.append(player.getName())
    result.append(winner)
    return result