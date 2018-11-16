'''
Created on 9 ott 2018

@author: Utente_

This module defines the Node class
'''


class NodeSMA(object):
    '''
    classdocs
    '''
    __slots__ = ['gameBoard','children','sequence','father','F','forgottenF','inMemory','childrenGenerated','childIndex']
    
    def __init__(self, board, sequence = str(), father = None):
        '''
        Constructor
        '''
        self.gameBoard = board
        self.children = []
        self.sequence = sequence
        self.father = father
        self.F = None
        self.forgottenF = None
        self.inMemory = False
        self.childrenGenerated = False
        self.childIndex = None
    
    # This function generates the children of the node
    def makeChildren(self):
        # Gets the list of available moves from the gameBoard, in the specified order
        availMoves = self.gameBoard.getMoves()
        # For each move, it creates a new Node with the new gameBoard and its sequence of moves
        for mov in availMoves:
            tmpBoard = self.gameBoard.applyMove(mov)
            newNode = NodeSMA(tmpBoard,self.sequence+mov,self)
            self.children.append(newNode)
        #self.childrenGenerated = True    

                
    def nextChild(self):
        if self.childrenGenerated == False:
            self.makeChildren()
            self.childIndex = 0
            self.childrenGenerated = True
        if self.childIndex == len(self.children):
            self.childIndex = 0
        if self.childIndex < len(self.children):
            index = self.childIndex
            self.childIndex+=1
            return self.children[index]
     
    def completed(self):
        return self.childIndex == len(self.children)
    """ 
    def depth(self):
        return len(self.sequence)

    def resetIterator(self):
        self.childIndex = 0
    """
    # This function defines the hash value of a node, which is the hash of the sequence of numbers of the attached gameBoard
    def __hash__(self):
        return hash(self.gameBoard.idsequence)
    
    # Nodes are compared by their F value     
    def __lt__(self, other):
        return self.F < other.F
    
    # Two nodes are equal if their gameBoard is equal
    def __eq__(self, other):
        if other == None :
            return False
        return self.gameBoard.idsequence == other.gameBoard.idsequence and self.sequence == other.sequence

