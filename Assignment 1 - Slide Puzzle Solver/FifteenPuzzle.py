"""
# File:     FifteenPuzzle.py
# Author:   Zeeshan Karim
# Date:     4/16/2017
# Course:   TCSS 435 - Artificial Intelligence
# Purpose:  15 slide puzzle solver, using 6 different search methods
#           Reports statistics when a solution is found
# Usage:    Program accepts command line arguments in format:
#               "[initialstate]" [searchmethod] [options]
# Output:   Prints statistics when solution found in format:
#               [depth], [numCreated], [numExpanded], [maxFringe]
"""

import sys
from copy import deepcopy

solution = ['1', '2', '3', '4', 
            '5', '6', '7', '8', 
            '9', 'A', 'B', 'C', 
            'D', 'E', 'F', ' ']

expandOrder = ['RIGHT', 'DOWN', 'LEFT', 'UP']

# Statistics variables
class Statistics:
    depth = -1
    nCreated = 0
    nExpanded = 0
    maxFringe = 0
    
    def __str__(self):
        return '%d, %d, %d, %d' % (self.depth, 
                                   self.nCreated, 
                                   self.nExpanded, 
                                   self.maxFringe)
        
# Priority queue for GBFS and AStar
class pQueue:
    nodeQueue = []
    weightQueue = []
    def __len__(self):
        return len(self.nodeQueue)
    
    def __str__(self):
        out = ''
        out += '--------------------\n'
        for i in range(len(self.nodeQueue)):
            out += str(self.weightQueue[i]) + '\n' + str(self.nodeQueue[i])
        out += '--------------------\n'
        return out
        
    def pop(self):
        if self.nodeQueue:
            self.weightQueue.pop(0)
            return self.nodeQueue.pop(0)
    
    def put(self, weight, node):
        for i in range(len(self.nodeQueue)):
            if weight < self.weightQueue[i]:
                self.weightQueue.insert(i, weight)
                self.nodeQueue.insert(i, node)
                return
        self.weightQueue.append(weight)
        self.nodeQueue.append(node)
# Puzzle board class
class Puzzle:

    state = []
    blankIndex = None
    depth = None
    
    def __init__(self, initial):
        self.state = list(initial)
        self.depth = 0
        self.blankIndex = self.state.index(' ')
        
    def __eq__(self, x):
        return self.state == x.state
    
    def __str__(self):
        out = ''
        for i in range(4):
            out += str(self.state[(i*4):((i+1)*4)])
            out += "\n"
        return out
        
    def isSolved(self):
        # Determines if a solution has been reached
        # Ignores elements 13 and 14 to accommodate unsolvable puzzles
        s1 = self.state[0:12] == solution[0:12]
        s2 = self.state[15] == solution[15]
        return s1 and s2
    
    def getSuccessors(self):
        # Returns any possible successor states in a list
        successors = []
        for direction in expandOrder:
            successor = None
            if direction == 'RIGHT' and self.blankIndex % 4 < 3:
                successor = deepcopy(self)
                target = self.blankIndex + 1
                    
            if direction == 'DOWN' and self.blankIndex < 12:
                successor = deepcopy(self)
                target = self.blankIndex + 4
                
            if direction == 'LEFT' and self.blankIndex % 4 > 0:
                successor = deepcopy(self)
                target = self.blankIndex - 1

            if direction == 'UP' and self.blankIndex > 3:
                successor = deepcopy(self)
                target = self.blankIndex - 4
            
            if successor:
                successor.depth += 1        
                successor.state[successor.blankIndex] = successor.state[target]
                successor.state[target] = ' '
                successor.blankIndex = target
                successors.append(successor)
        return successors

    def nIncorrect(self):
        # Heuristic for number of incorrect tiles
        n = 0
        for index, tile in enumerate(self.state):
            if tile != solution[index]: n += 1
        return n
    
    def manhattanSum(self):
        # Heuristic for sum of Manhattan distance to solution
        mSum = 0
        for tileIndex, tile in enumerate(self.state):
            solIndex = solution.index(tile);
            vDistance = abs(solIndex/4 - tileIndex/4)
            hDistance = abs(solIndex%4 - tileIndex%4)
            mSum += vDistance + hDistance
        return mSum
                
def solveBFS(start):
    #Nodes to be expanded are queued FIFO
    stats = Statistics()
    queue = []
    done = []
    queue.append(start)

    while queue:
        current = queue.pop(0)
        if current.isSolved():
            stats.depth = current.depth
            return stats
        stats.nExpanded += 1
        done.append(current)
        successors = current.getSuccessors()
        for successor in successors:
            if successor not in done:
                stats.nCreated += 1
                queue.append(successor)
                if len(queue) > stats.maxFringe:
                    stats.maxFringe = len(queue)
    return Statistics() # No Solution, return default statistics
                    
def solveDFS(start):
    # Identical to BFS except nodes to be expanded are queued LIFO
    stats = Statistics()
    stack = []
    done = []
    stack.append(start)

    while stack:
        current = stack.pop()
        if current.isSolved():
            stats.depth = current.depth
            return stats
        stats.nExpanded += 1
        done.append(current)
        successors = current.getSuccessors()
        for successor in successors:
            if successor not in done:
                stats.nCreated += 1
                stack.append(successor)
                if len(stack) > stats.maxFringe:
                    stats.maxFringe = len(stack)
    return Statistics() # No Solution, return default statistics
    
def solveDLS(start, maxDepth):
    # Identical to DFS except nodes are limited to max depth set by user
    stats = Statistics()
    stack = []
    done = []
    stack.append(start)

    while stack:
        current = stack.pop()
        if current.isSolved():
            stats.depth = current.depth
            return stats
        stats.nExpanded += 1
        done.append(current)
        successors = current.getSuccessors()
        for successor in successors:
            if successor not in done and successor.depth <= int(maxDepth):
                stats.nCreated += 1
                stack.append(successor)
                if len(stack) > stats.maxFringe:
                    stats.maxFringe = len(stack)
    return Statistics() # No Solution, return default statistics
    
def solveID(start):
    # Identical to DFS with iterative deepening implemented
    # Depth limited to 100 in case solution cannot be found
    stats = Statistics()
    stack = []
    done = []
    stack.append(start)
    maxDepth = 0
    while maxDepth < 100:
        while stack:
            current = stack.pop()
            if current.isSolved():
                stats.depth = current.depth
                return stats
            stats.nExpanded += 1
            done.append(current)
            successors = current.getSuccessors()
            for successor in successors:
                if successor not in done and successor.depth <= maxDepth:
                    stats.nCreated += 1
                    stack.append(successor)
                    if len(stack) > stats.maxFringe:
                        stats.maxFringe = len(stack)
        maxDepth += 1
        stack.append(start)
        done = []
    return Statistics() # No Solution, return default statistics

def solveGBFS(start, heuristic):
    # Nodes are queued by priority determined by user selected heuristic
    stats = Statistics()
    queue = pQueue()
    done = []
    priority = None

    if heuristic == 'h1':
        priority = start.nIncorrect()
    elif heuristic == 'h2':
        priority = start.manhattanSum()
    
    queue.put(priority, start)

    while queue:
        current = queue.pop()
        if current.isSolved():
            stats.depth = current.depth
            return stats
        stats.nExpanded += 1
        done.append(current)
        successors = current.getSuccessors()
        for successor in successors:
            if successor not in done:
                stats.nCreated += 1
                if heuristic == 'h1':
                    priority = successor.nIncorrect()
                elif heuristic == 'h2':
                    priority = successor.manhattanSum()
                queue.put(priority, successor)
                if len(queue) > stats.maxFringe:
                    stats.maxFringe = len(queue)
    return Statistics() # No Solution, return default statistics

def solveAStar(start, heuristic):
    # Nodes are queued by priority determined by depth and user selected heuristic
    stats = Statistics()
    queue = pQueue()
    done = []
    priority = None

    if heuristic == 'h1':
        priority = start.nIncorrect()
    elif heuristic == 'h2':
        priority = start.manhattanSum()
    queue.put(priority + start.depth, start)

    while queue:
        current = queue.pop()
        if current.isSolved():
            stats.depth = current.depth
            return stats
        done.append(current)
        stats.nExpanded += 1
        successors = current.getSuccessors()
        for successor in successors:
            if heuristic == 'h1':
                priority = successor.nIncorrect()
            elif heuristic == 'h2':
                priority = successor.manhattanSum()
            if successor not in done:
                stats.nCreated += 1
                queue.put(priority + successor.depth, successor)
                if len(queue) > stats.maxFringe:
                    stats.maxFringe = len(queue)
            elif done[done.index(successor)].depth > successor.depth:
                done[done.index(successor)].depth = successor.depth
                queue.put(priority + successor.depth, successor)
                
    return Statistics() # No Solution, return default statistics  

if __name__ == '__main__':
    
    start = None
    solveWith = None
    heuristic = None
    stats = None
    
    if len(sys.argv) in range(3, 5):
        start = Puzzle(sys.argv[1])
        solveWith = sys.argv[2]
        if len(sys.argv) == 4:
            heuristic = sys.argv[3]
    else:
        print "Invalid input"
        sys.exit(-1)

    if sorted(start.state) != sorted(solution):
        print 'Invalid puzzle'
        sys.exit(-1)
    
    if solveWith == 'DLS' and not int(heuristic):
        print 'Invalid depth, DLS requires an int depth'
        sys.exit(-1)
        
    elif solveWith == 'GBFS' or solveWith == 'AStar':
        if heuristic != 'h1' and heuristic != 'h2':
            print 'Invalid heuristic, GBFS and AStar only accept heuristics h1 and h2'
            sys.exit(-1)

    if solveWith == 'BFS':
        stats = solveBFS(start)
        
    elif solveWith == 'DFS':
        stats = solveDFS(start)
        
    elif solveWith == 'DLS':
        stats = solveDLS(start, heuristic)
        
    elif solveWith == 'ID':
        stats = solveID(start)
    
    elif solveWith == 'GBFS':
        stats = solveGBFS(start, heuristic)
        
    elif solveWith == 'AStar':
        stats = solveAStar(start, heuristic)
        
    else:
        print 'Invalid search method'
        sys.exit(-1)
    
    print stats
    
    