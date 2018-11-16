'''
Created on 9 ott 2018

@author: Utente_

This module defines the board class
'''
import copy, random
import algorithms
import heuristics
import node
import timeit
import math
def wrapper(func, args):
    def wrapped():
        return func(*args)
    return wrapped
class Board(object):
    '''
    classdocs
    '''
    order = "DURL" # The order used to explore the available moves, this default value is used in informed search 
    # These lambdas are used to determine if a move is available
    moves = {
        'L' : lambda y : y < Board.cols - 1,
        'R' : lambda y : y > 0,
        'U' : lambda x : x < Board.rows - 1,
        'D' : lambda x : x > 0
        }
    random = False # If true, we apply random neighbourood search
    rows = None 
    cols = None


    def __init__(self, values, index):
        '''
        Constructor
        '''
        self.gameBoard = values # The matrix that represents the board
        self.index = index  # The index (coordinates)  of 0
        # The board is identified but putting all its numbers in a single row
        self.idsequence = tuple([elem for row in self.gameBoard for elem in row]) 
    
    # This function applies the move dirLetter to the board
    def applyMove(self, dirLetter):
        newBoard = Board(copy.deepcopy(self.gameBoard),self.index) # We create a copy of the board
        x0,y0 = newBoard.index                                     # And save the index of 0
        # We get the new index of 0 by applying (x,y) + direction e.g. (0,2) + (0,-1) = (0,1)
        x1,y1 = tuple([index + direction for index,direction in zip(newBoard.index,Board.getDirection(dirLetter))])
        # We swap the 0 with the destination number using tuple assignment
        newBoard.gameBoard[x0][y0], newBoard.gameBoard[x1][y1] = newBoard.gameBoard[x1][y1], newBoard.gameBoard[x0][y0]
        # We manually assign the new 0 index and the new idsequence
        newBoard.index = (x1,y1)
        newBoard.idsequence = tuple([elem for row in newBoard.gameBoard for elem in row])
        return newBoard
    
    # This static function converts a letter to its corresponding direction
    @staticmethod   
    def getDirection(dirLetter):
        if dirLetter == 'L':
            return (0,1)
        elif dirLetter == 'R':
            return (0,-1)
        elif dirLetter == 'U':
            return (1,0)
        elif dirLetter == 'D':
            return (-1,0)
        else:
            raise ValueError
    
    # This function returns the possible moves that can be executed on the board    
    def getMoves(self):
        x,y = self.index
        availMoves = []
        if Board.random == True:                                # If random order is set, we shuffle the order string randomly
            Board.order = ''.join(random.sample(Board.order,4))
        for char in Board.order:                                # Available moves are evaluated according to the order string
            if char == 'L' or char == 'R':
                if Board.moves[char](y) == True:
                    availMoves.append(char)
            else :
                if Board.moves[char](x) == True:
                    availMoves.append(char)
        return availMoves
    
    # This function gives a string representation to a given board
    def __str__(self):
        rowSep = '\n' + '---'*Board.cols + '\n'
        colSep = '|'
        outputString = rowSep
        for row in self.gameBoard:
            for elem in row:
                outputString+= colSep + str(elem) + colSep
            outputString+=rowSep
           
        return outputString
    
    # This function checks if the board is in the goal state
    def isSolved(self):
        res = self.idsequence
        if res[-1]!=0:
            return False
        else:
            res = res[:-1]
            for i in range(1,len(res)+1):
                if i != res[i-1]:
                    return False
        return True
    
    # This function returns the number of inversions in the board
    def inversions(self):
        tmp = [elem for row in self.gameBoard for elem in row if elem != 0]
        inversions = 0
        for i in range(len(tmp)):
            for j in range(i+1,len(tmp)):
                if tmp[i] > tmp[j] :
                    inversions+=1
        return inversions
            
            
    # This function returns whether the board is solvable or not   
    def isSolvable(self): 
        if (Board.rows % 2 == 1 and self.inversions() % 2 == 0) or (Board.rows % 2 == 0 and ((self.index[0] % 2 == 0) == (self.inversions() % 2 == 1))) :
            return True
        else:
            return False
        
if __name__ == "__main__":
    def opp(l):
        if l == "D":
            return "U"
        if l == "U":
            return "D"        
        if l == "L":
            return "R"
        if l == "R":
            return "L" 
        if l == None:
            return None               
    types = list(range(19,70))
    #algos = [algorithms.BFS, algorithms.DFS, algorithms.IDFS,algorithms.bestFirstSearch,algorithms.aSearch]
    algos = [algorithms.bestFirstSearch,algorithms.aSearch]
    heurs = [heuristics.h2_sumManhattanDistance]
    slots = ['gameBoard','sequence','F','G']
    Board.rows = 4
    Board.cols = 4
    for t in types:
        #algorithms.memoryLimit = t+1
        prev = None
        mov = None
        board = Board([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]],(3,3))
        seq = str()
        for i in range(t):
            moves = board.getMoves()
            mov = moves[random.randint(0,len(moves)-1)]
            while mov == opp(prev):
                mov = moves[random.randint(0,len(moves)-1)]
            seq += mov
            board = board.applyMove(mov)
            prev = mov
        print(board)
        print(seq)
        for heur in heurs:
            for algo in algos:
                rootTree = node.getNodeClass(slots)(board) 
                args = (rootTree,)
                if algo == algorithms.bestFirstSearch:
                    f = heur
                    args += (f,)
                elif algo == algorithms.aSearch:
                    f = heuristics.getF(heur)
                    args += (f,)
                      
                wrapped = wrapper(algo,args)
                print(algo)
                print(t) 
                print(timeit.timeit(wrapped,number=1))