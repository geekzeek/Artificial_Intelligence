"""
# File:     main.py
# Author:   Zeeshan Karim
# Date:     5/15/2017
# Course:   TCSS 435 - Artificial Intelligence
# Purpose:  Command Line Game of Pentago vs MiniMax and Alpha-Beta Pruning AI
"""

import random
import re

import pentago
import AI

if __name__ == '__main__':
    
    player = ''
    computer = ''
    nextTurn = ''
    move = ''
    pwin = False
    cwin = False
    
    game = pentago.game()
    opponent = AI.player()
    
    outfile = open('Output.txt', 'w')
    
    # Determine player and computer game piece colors
    while player not in ['w', 'b']:
        player = raw_input('Choose Player Color (w or b): ')
    if player == 'w': computer = 'b'
    else: computer = 'w'
    
    # Assign colors to minimize and maximize
    opponent.mincolor = player
    opponent.maxcolor = computer
    
    # Randomly select which player goes first
    nextTurn = [player, computer][random.randint(0,1)]
    if nextTurn is player: print 'Player Goes First!'
    else: print 'Computer Goes First'
    print game
    
    # Write game information to file
    outfile.write('Player color: ' + player + '\n')
    outfile.write('Computer color: ' + computer + '\n')
    outfile.write('Player to move first: ' + nextTurn + '\n')
    outfile.write(str(game))
    
    try:
        # Game loop
        while(True):
            
            if nextTurn is player:
                # Get command line input of player move
                valid = False
                while not valid:
                    move = raw_input('Enter Move (%s): ' %player)
                    valid = re.match('^[1-4]\/[1-9] [1-4][RrLl]', move)
                    if valid: valid = game.validMove(move)
                    if not valid:
                        print 'Invalid move, try again'
    
                
            else:
                # Get move from AI with current game state
                print "Computer's Turn..."
                move = opponent.getMove(game)
            
            # Place the piece from the move and check win conditions
            game.placeItem(nextTurn, move)
            pwin = game.checkWin(player)
            cwin = game.checkWin(computer)
            if pwin or cwin: break
            
            # Rotate the block from the move and check win conditions
            game.rotateBlock(move)
            pwin = game.checkWin(player)
            cwin = game.checkWin(computer)
            if pwin or cwin: break
            
            # Check for full board tie
            if all(x != '.' for x in game.board):
                pwin = cwin = True
                break
            
            # Print move and game board to console and file
            print move
            print game
            outfile.write(move + '\n')
            outfile.write(str(game) + '\n')
            
            # Swap who's turn it is
            if nextTurn is player: nextTurn = computer
            else: nextTurn = player
        
        # Print final move and board to console and file
        print move
        print game
        outfile.write(move + '\n')
        outfile.write(str(game))
        
        if pwin and not cwin: print 'Player Wins!'
        elif cwin and not pwin: print 'Computer Wins!'
        else: print 'Tie Game!'
    finally:
        outfile.close()
    

            
                

        