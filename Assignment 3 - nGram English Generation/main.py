"""
# File:     main.py
# Author:   Zeeshan Karim
# Date:     5/27/2017
# Course:   TCSS 435 - Artificial Intelligence
# Purpose:  Implementation of nGram English Language Generator
"""

import nGram
import random

# Depth of nGram structure
N_GRAM = 5

# Number of words to generate
LEN_OUTPUT = 1000

# Example file directory and filenames
directory = 'ExampleText/'
fileList = []
fileList.append('alice-27.txt') 
fileList.append('doyle-27.txt')
fileList.append('doyle-case-27.txt')
fileList.append('london-call-27.txt')
fileList.append('melville-billy-27.txt')
fileList.append('twain-adventures-27.txt')

if __name__ == '__main__':
    model = []
    wordSequence = []
    nWords = 0
    
    # Iterate through files and add nGrams to model
    for fileName in fileList:
        print 'Reading ' + fileName + ' ...'
        with open(directory + fileName, 'r') as openFile:
            for line in openFile:
                for word in line.split():
                    nWords += 1
                    wordSequence.append(word.lower())
                    if len(wordSequence) == N_GRAM:
                        exists = False
                        for gram in model:
                            if gram.element == wordSequence[0]:
                                exists = True
                                gram.update(wordSequence[1:])
                                break
                        if not exists:
                            model.append(nGram.nGram(0, wordSequence))      
                        wordSequence.remove(wordSequence[0])

    '''
    # Write string representation of model to model.txt
    with open('model.txt', 'w') as outFile:
        for gram in model:
            outFile.write(str(gram) + '\n')
    '''        
    
    # Select weighted random first word from model
    output = []
    position =  random.randint(0, nWords -1)
    print 'Generating text ...'
    for gram in model:
        position -= gram.count
        if position < 0:
            output.append(gram.element)
            break
    
    # Loop word selection based off first word till output length
    while len(output) < LEN_OUTPUT:
        for gram in model:
            if gram.element == output[-1]:
                output += gram.getWords()
                break
    
    # Write generated text to output.txt
    with open('output.txt', 'w') as outFile:
        for word in output[0:LEN_OUTPUT - 1]:
            outFile.write(word + ' ')
    print 'Text written to output.txt'