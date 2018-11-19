'''
Created on 9 ott 2018

@author: Utente_

This module defines the Node class for SMA* algorithm
'''


class NodeSMA(object):
    '''
    classdocs
    '''
    __slots__ = ['gameBoard','children','sequence','father','F','G','forgottenF','inMemory','childrenGenerated','childIndex','ID']
    
    def __init__(self, board, sequence = str(), father = None):
        '''
        Constructor
        '''
        self.gameBoard = board # The board object
        self.children = []  # The list of children
        self.sequence = sequence # The full sequence of moves from start to here
        self.father = father # The father of the node
        self.F = None   # F-value
        self.forgottenF = None # The F-value of the best forgotten child
        self.inMemory = False # Whether the node is in the set of nodes to visit
        self.childrenGenerated = False # Whether its children have been generated or not
        self.childIndex = None # The index of the next child to return
        self.ID = None  # An identification number to distinguish whether a node is newer or older
    
    # This function generates the children of the node
    def makeChildren(self):
        # Gets the list of available moves from the gameBoard, in the specified order
        availMoves = self.gameBoard.getMoves()
        # For each move, it creates a new Node with the new gameBoard and its sequence of moves
        for mov in availMoves:
            tmpBoard = self.gameBoard.applyMove(mov)
            newNode = NodeSMA(tmpBoard,self.sequence+mov,self)
            self.children.append(newNode)  

    # Returns the next child, if children are finished, it restarts from the first one         
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
     
    # Returns whether the node has generated all of its children
    def completed(self):
        return self.childIndex == len(self.children)

    # This function defines the hash value of a node, which is the hash of the sequence of numbers of the attached gameBoard
    def __hash__(self):
        return hash(self.gameBoard.gameBoard)
    
    # Nodes are compared by their F value     
    def __lt__(self, other):
        return self.F < other.F
    
    # Two nodes are equal if their gameBoard is equal
    def __eq__(self, other):
        if other == None :
            return False
        return self.gameBoard.gameBoard == other.gameBoard.gameBoard #and self.sequence == other.sequence

