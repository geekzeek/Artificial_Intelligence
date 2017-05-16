"""
# File:     pentago.py
# Author:   Zeeshan Karim
# Date:     5/15/2017
# Course:   TCSS 435 - Artificial Intelligence
# Purpose:  Implementation of Pentago Game
"""

# Pentago game class containing board state and game methods
class game:

    board = ['.']*36
    
    # String representation of game board
    def __str__(self):
        output = ''
        output += '+-------+-------+\n'
        for i in range(2):
            for j in range(3):
                output += '| '
                for k in range(2):
                    for l in range(3):
                        output += self.board[l + k*3 + j*6 + i*18] + ' '
                    output += '| '
                output += '\n'
            output += '+-------+-------+\n'
        return output
    
    # Overload '=' operator for comparing game states
    def __eq__(self, x):
        return self.board == x.board
    
    # Place a game piece
    def placeItem(self, player, move):
        block = int(move[0])-1
        index = int(move[2])-1
        self.board[self.position(block, index)] = player
    
    # Check if a move can be made
    def validMove(self, move):
        block = int(move[0]) - 1
        index = int(move[2]) - 1
        if self.board[self.position(block, index)] == '.': return True 
        else: return False
    
    # Rotate a game block    
    def rotateBlock(self, move):
        block = int(move[4]) - 1
        direction = move[5]
        rotated = []
        
        # Extract block elements in to 3x3 array
        for i in range(3):
            line = []
            for j in range(3):
                line.append(self.board[self.position(block, j + i*3)])
            rotated.append(line)
        
        # Rotate 3x3 matrix right or left
        if direction == 'r' or direction == 'R':
            rotated = zip(*rotated[::-1])
        else:
            rotated = list(reversed(zip(*rotated)))
        
        # Place elements back into game board
        for i in range(3):
            for j in range(3):
                self.board[self.position(block, j + i*3)] = rotated[i][j]
    
    # Check if a player has won with 5 elements in a row    
    def checkWin(self, player):
        win = False
        for i in range(6):
            for j in range(6):
                if self.board[j + i*6] == player:
                    #Check horizontal
                    if j < 2 and not win:
                        line = []
                        for k in range(5): line += self.board[j+k + i*6]
                        win = all(x == player for x in line)
                    
                    #Check vertical
                    if i < 2 and not win:
                        line = []
                        for k in range(5): line += self.board[j + (i+k)*6]
                        win = all(x == player for x in line)
                    
                    #Check left diagonal
                    if i < 2  and j < 2 and not win:  
                        line = []
                        for k in range(5): line += self.board[j+k + (i+k)*6]
                        win = all(x == player for x in line)
                    
                    #Check right diagonal
                    if i < 2 and j > 3 and not win:
                        line = []
                        for k in range(5): line += self.board[j-k + (i+k)*6]
                        win = all(x == player for x in line)
                    if win: return True
        return False
    
    # Return list of all valid moves from current game board
    def possibleMoves(self):
        moves = []
        for block in range(1, 5):
            for index in range(1, 10):
                if self.board[self.position(block-1, index-1)] == '.':
                    for rotate in range(1, 5):
                        for direction in ['l', 'r']:
                            move = str(block) + '/' + str(index) + ' ' + str(rotate) + direction
                            moves.append(move)
        return moves        
    
    # Determine utility by tearing board into strips and counting repeating elements
    def getUtility(self, maxcolor, mincolor):
        utility = 0
        
        # Horizontal strips
        lines = []
        for i in range(6):
            lines.append(self.board[i*6:(i+1)*6])
        
        utility += self.calculateUtility(lines, maxcolor, mincolor)
        
        # Vertical strips
        lines = []
        for i in range(6):
            line = []
            for j in range(6):
                line.append(self.board[j*6 + i])
            lines.append(line)
        
        utility += self.calculateUtility(lines, maxcolor, mincolor)
        
        # Left diagonal strips
        lines = []
        for i in range(1,6):
            line = []
            increment = 0
            while ((i+increment)*6 + increment) < len(self.board):
                line.append(self.board[(i+increment)*6 + increment])
                increment += 1
            lines.append(line)
            
        for i in range(6):
            line = []
            increment = 0
            while (i + increment) < 6:
                line.append(self.board[increment*6 + i+increment])
                increment += 1
            lines.append(line)
            
        utility += self.calculateUtility(lines, maxcolor, mincolor)
        
        # Right diagonal strips
        lines = []
        for i in range(1,6):
            line = []
            increment = 0
            while (((i + increment)*6 + 5 - increment)) < len(self.board):
                line.append(self.board[(i + increment)*6 + 5 - increment])
                increment += 1
            lines.append(line)

        for i in range(6):
            line = []
            increment = 0
            while i - increment >= 0:
                line.append(self.board[i + increment*6 - increment])
                increment += 1
            lines.append(line)
        
        utility += self.calculateUtility(lines, maxcolor, mincolor)
        
        # Add preference for block centers if there are no repeating elements
        if utility == 0:
            for location in [7, 10, 25, 28]:
                if self.board[location] == maxcolor:
                    utility += 2
                if self.board[location] == mincolor:
                    utility -= 2
        
        return utility
    
    # Count number of repeating elements and compute utility value
    def calculateUtility(self, lines, maxcolor, mincolor):
        #Utility scores for 1, 2, 3, 4, 5 and 6 repeating elements
        scores = [0, 1, 10, 100, 1000, 1000] 
        
        utility = 0
        for line in lines:
            if len(line) > 1:
                count = 0
                for i in range(1, len(line)):
                    if line[i-1] == line[i]:
                        count += 1
                    else:
                        if line[i-1] == maxcolor:
                            utility += scores[count]
                        elif line[i-1] == mincolor:
                            utility -= scores[count]
                        count = 0
                if count != 0:
                    if line[i-1] == maxcolor:
                        utility += scores[count]
                    elif line[i-1] == mincolor:
                        utility -= scores[count]
        return utility
    
    # Index helper converting block and index to board element
    def position(self, block, index):
        helper = [[ 0,  1,  2,  6,  7,  8, 12, 13, 14],
                  [ 3,  4,  5,  9, 10, 11, 15, 16, 17],
                  [18, 19, 20, 24, 25, 26, 30, 31, 32],
                  [21, 22, 23, 27, 28, 29, 33, 34, 35]]
        return helper[block][index]