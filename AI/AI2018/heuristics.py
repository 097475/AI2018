'''
Created on 11 ott 2018

@author: Utente_

This module defines the heuristics used in informed search algorithms
'''

# This function, given a heuristic, returns the F function, that is g(n) + h(n)
def getF(func):
    def f(node):
        return g(node) + func(node)
    return f

# This function defines the g function, i.e. the distance from source to the given node
# This is simply defined as the length of the sequence of moves of the given node
def g(node):
    return len(node.sequence)

# This heuristic always returns 0, the argument is for compatibility purposes
def h0(node):
    return 0

# This heuristic returns the number of misplaced non zero tiles in the board of the given node
def h1_nMisplacedTiles(node):
    boardSequence = node.gameBoard.idsequence 
    count = 0
    for i in range(1,len(boardSequence)): 
        if i != boardSequence[i-1]:
            count+=1
    return count

# This heuristic returns the sum of the Manhattan distances of each non zero tile compared to their expected position  
def h2_sumManhattanDistance(node):
    rows = node.gameBoard.rows
    cols = node.gameBoard.cols
    matrix = node.gameBoard.gameBoard
    count = 0
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] != 0 :
                count += abs(i - ((matrix[i][j]-1)//rows)) + abs(j - ((matrix[i][j]-1)%cols))
    return count

# This heuristic returns the number of inversions in the board of the given node
def h3_sumInversions(node):
    return node.gameBoard.inversions()
