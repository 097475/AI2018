'''
Created on 9 ott 2018

@author: Utente_

This module defines the Node class
'''

def getNodeClass(slots):

    class Node(object):
        '''
        classdocs
        '''
        #__slots__ = ['gameBoard','sequence','F','G']
        __slots__ = slots
        def __init__(self, board, sequence = str()):
            '''
            Constructor
            '''
            self.gameBoard = board
            self.sequence = sequence
        
        # This function generates the children of the node
        def makeChildren(self):
            children = []
            # Gets the list of available moves from the gameBoard, in the specified order
            availMoves = self.gameBoard.getMoves()
            # For each move, it creates a new Node with the new gameBoard and its sequence of moves
            for mov in availMoves:
                tmpBoard = self.gameBoard.applyMove(mov)
                newNode = Node(tmpBoard,self.sequence+mov)
                children.append(newNode)
            return children   
    
            
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
            return self.gameBoard.idsequence == other.gameBoard.idsequence 
        
    return Node