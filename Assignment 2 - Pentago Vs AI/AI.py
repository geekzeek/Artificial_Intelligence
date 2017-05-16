"""
# File:     AI.py
# Author:   Zeeshan Karim
# Date:     5/15/2017
# Course:   TCSS 435 - Artificial Intelligence
# Purpose:  Implementation of Search Tree, and Minimax / Alpha-Beta Algorithms
"""

import random
from copy import deepcopy

import pentago

# Depth limit of search tree
maxDepth = 3

# Search method to use, 'AlphaBeta' or 'MiniMax'
searchMethod = 'AlphaBeta'

# Game node class used to create tree
class gameNode:
    state = None
    lastMove = None
    depth = 0
    value = 0
    children = []
    
    # Populates list of children from current game state
    def getChildren(self, color):
        # Get list of possible moves
        moves = self.state.possibleMoves()
        
        # Create a child for each move and add it to the list
        for move in moves:
            child = gameNode()
            child.state = pentago.game()
            child.state.board = deepcopy(self.state.board)
            child.state.placeItem(color, move)
            child.state.rotateBlock(move)
            child.lastMove = move
            child.depth = self.depth + 1
            child.children = []
            
            # Check if the new board state already exists
            exists = False
            for existing in self.children:
                if child.state == existing.state:
                    exists = True
                    break
                
            # Add the new state if it does not exist yet
            if not exists:
                self.children.append(child)


# AI player class containing MiniMax and AlphaBeta search algorithms
class player:
    
    gameTree = None
    currentNode = None
    maxcolor = ''
    mincolor = ''
    depthLimit = -1
    
    # Testing Variables
    nExpanded = 0

    # Get a random valid move for testing
    def getTestMove(self, current):
        valid = False
        while not valid:
            move = ''
            move += str(random.randint(1, 4))
            move += '/'
            move += str(random.randint(1, 9))
            move += ' '
            move += str(random.randint(1, 4))
            move += ['r', 'l'][random.randint(0,1)]
            valid = current.validMove(move)
        return move
    
    # Get an intelligent move using game tree search
    def getMove(self, current):
        # Create the tree or update current node if it already exists
        if self.gameTree == None:
            self.gameTree = gameNode()
            self.gameTree.state = current
            self.gameTree.depth = 0
            self.gameTree.lastMove = ''
            self.currentNode = self.gameTree
        else:
            for child in self.currentNode.children:
                if child.state == current:
                    self.currentNode = child
                    break
                
        # Update depth limit for this search
        self.depthLimit = self.currentNode.depth + maxDepth
        
        # Find optimal state
        if searchMethod == 'AlphaBeta':
            nextNode = self.alphaBetaSearch(self.currentNode)
        else:
            nextNode = self.miniMaxSearch(self.currentNode)
        
        # Display and reset nExpanded for testing
        # print self.nExpanded
        self.nExpanded = 0
        
        # Update current node to the optimal state
        self.currentNode = nextNode
        
        # Return the move used to get to optimal state
        return nextNode.lastMove
        
    def alphaBetaSearch(self, node):
        #If there are no children yet, get them
        if(len(node.children) == 0):
            node.getChildren(self.maxcolor)
            self.nExpanded += 1
        
        # Start a new AlphaBeta search from the current state
        beta = float('inf')
        alpha = -float('inf')
        bestChild = node.children[0]
        
        # Find the maximum value child
        for child in node.children:
            # Determine value by minimizing next depth level
            child.value = self.AB_minimize(child, alpha, beta)
            if child.value > alpha:
                alpha = child.value
                bestChild = child
        return bestChild


    def AB_maximize(self, node, alpha, beta):
        # If we haven't hit depth limit and children don't exist yet, get them
        if node.depth < self.depthLimit:
            if len(node.children) == 0:
                node.getChildren(self.maxcolor)
                self.nExpanded += 1
        
        # If node is terminal, return its utility    
        if len(node.children) == 0:
            return node.state.getUtility(self.maxcolor, self.mincolor)
        
        # Find the maximum value child
        value = -float('inf')
        for child in node.children:
            # Determine value by minimizing next depth level
            child.value = self.AB_minimize(child, alpha, beta)
            value = max(value, child.value)
            if value >= beta:
                # Prune nodes and return current value
                return value
            alpha = max(alpha, value) 
        return value
        
    def AB_minimize(self, node, alpha, beta):
        # If we haven't hit depth limit and children don't exist yet, get them
        if node.depth < self.depthLimit:
            if len(node.children) == 0:
                node.getChildren(self.mincolor)
                self.nExpanded += 1

        # If node is terminal, return its utility 
        if len(node.children) == 0:
            return node.state.getUtility(self.maxcolor, self.mincolor)
        
        # Find the minimum value child
        value = float('inf')
        for child in node.children:
            # Determine value by maximizing next depth level
            child.value = self.AB_maximize(child, alpha, beta)
            value = min(value, child.value)
            if value <= alpha:
                # Prune nodes and return current value
                return value
            beta = min(beta, value)
        return value
    
    
    def miniMaxSearch(self, node):
        # If there are no children yet, get them
        if(len(node.children) == 0):
            node.getChildren(self.maxcolor)
            self.nExpanded += 1
        
        # Start a new MiniMax search from the current state
        bestValue = self.MM_maximize(node)
        bestChild = node.children[0]
        
        # Find the child with optimal value and return it
        for child in node.children:
            if child.value == bestValue:
                bestChild = child
                break
        return bestChild
    
    def MM_maximize(self, node):
        # If we haven't hit depth limit and children don't exist yet, get them
        if node.depth < self.depthLimit:
            if len(node.children) == 0:
                node.getChildren(self.maxcolor)
                self.nExpanded += 1
        
        # If node is terminal, return its utility 
        if len(node.children) == 0:
            return node.state.getUtility(self.maxcolor, self.mincolor)
        
        # Find the maximum value child    
        maxValue = -float('inf')
        for child in node.children:
            # Determine value by minimizing next depth level
            child.value = self.MM_minimize(child)
            maxValue = max(maxValue, child.value)
        return maxValue
    
    def MM_minimize(self, node):
        # If we haven't hit depth limit and children don't exist yet, get them
        if node.depth < self.depthLimit:
            if len(node.children) == 0:
                node.getChildren(self.mincolor)
                self.nExpanded += 1
        
        # If node is terminal, return its utility 
        if len(node.children) == 0:
            return node.state.getUtility(self.maxcolor, self.mincolor)
        
        # Find the minimum value child    
        minValue = float('inf')
        for child in node.children:
            # Determine value by maximizing next depth level
            child.value = self.MM_maximize(child)
            minValue = min(minValue, child.value)
        return minValue
        
    

