"""
# File:     nGram.py
# Author:   Zeeshan Karim
# Date:     5/27/2017
# Course:   TCSS 435 - Artificial Intelligence
# Purpose:  Implementation of nGram object for creating language model
"""

import random

class nGram():
    
    # Initializes member variables and creates successor nGram objects
    def __init__(self, level, params):
        self.element = params[0]
        self.count = 1
        self.level = level
        self.successors = []
        if len(params) > 1:
            self.successors.append(nGram(self.level + 1, params[1:]))
    
    # Recursive string representation of nGram model        
    def __str__(self):
        output = ''.join(['\t']*self.level) 
        output += self.element + ' ' + str(self.count) + '\n'
        for successor in self.successors:
            output += str(successor)
        return output
    
    # Recursively updates nGram model with a new word sequence
    def update(self, params):
        self.count += 1
        exists = False
        for successor in self.successors:
            if params[0] == successor.element:
                exists = True
                successor.update(params[1:])
                break
        if not exists and len(params) > 0:
            self.successors.append(nGram(self.level + 1, params))
    
    # Recursively generates weighted random word sequence        
    def getWords(self):
        output = []
        position = random.randint(0, self.count - 1)
        for successor in self.successors:
            position -= successor.count
            if position < 0:
                output.append(successor.element)
                output += (successor.getWords())
                break
        return output