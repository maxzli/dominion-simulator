#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 01:55:40 2020

@author: maxzli
"""
from IPython import get_ipython
get_ipython().magic('reset -sf')

from dominionInit import Card

# Card('Name', cost, kind, specialAction, Effect)
# Card.Effect: [description, +cards, +actions, +buy, +treasure]

# initialize basic setup cards
ACTION_CARDS = [Card('Smithy', 4, 'A', False, ["+3 Cards", 3, 0, 0, 0]), 
                Card('Village', 3, 'A', False, ["+1 Card, +2 Actions", 1, 2, 0, 0]), 
                 Card('Gardens', 4, 'V', False, ["1 VP for every 10 cards (rounded down)", 0, 0, 0, 0]), # special
                 Card('Militia', 4, 'A', True, ["+2 Treasure, other players discard 2", 0, 0, 0, 2]), # special
                 Card('Moat', 2, 'A', True, ["+2 Cards, Other players' attacks have no effect", 2, 0, 0, 0]), # special
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