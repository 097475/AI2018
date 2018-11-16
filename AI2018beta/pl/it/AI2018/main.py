'''
Created on 9 ott 2018

@author: Utente_
'''
from board import Board
from node import getNodeClass
from nodeSMA import NodeSMA
import algorithms
import heuristics
import sys,getopt
import timeit

helpstr = """
usage:

-b/--bfs order    Breadth-first search

-d/--dfs order   Depth-first search

-i/--idfs order  Iterative deepenening DFS

-h/--bf id_of_heurisic    Best-first strategy

-a/--astar id_of_heurisic    A* strategy

-s/--sma id_of_heurisic   SMA* strategy

available heuristics:

    h0    :    0
    h1    :    Number of misplaced tiles
    h2    :    Manhattan distance
    h3    :    Number of inversions

valid orders:

LDUR,RULD,ULDR,etc.

"""

memoryLimit = 5000
depthLimit = 500

# This dictionary stores the algorithm function references
algos = {
    '-b' : algorithms.BFS,
    '--bfs': algorithms.BFS,
    '-d' : algorithms.DFS,
    '--dfs': algorithms.DFS,
    '-i' : algorithms.IDFS,
    '--idfs': algorithms.IDFS,
    '-h' : algorithms.bestFirstSearch,
    '--bf': algorithms.bestFirstSearch,
    '-a' : algorithms.aSearch,
    '--astar': algorithms.aSearch,
    '-s' : algorithms.SMA,
    '--sma': algorithms.SMA
    }
# This dictionary stores the heuristic function references
heurs = {
    'h0' : heuristics.h0,
    'h1' : heuristics.h1_nMisplacedTiles,
    'h2' : heuristics.h2_sumManhattanDistance,
    'h3' : heuristics.h3_sumInversions
    }

nodeAttributes = ['gameBoard','sequence']
additionalAttributes = {
    algorithms.BFS : [],
    algorithms.DFS : [],
    algorithms.IDFS : [],
    algorithms.bestFirstSearch : ['F'],
    algorithms.aSearch : ['F','G']   
    }

# This function reads the input from stdin : the number of rows and columns, and the initial board
# User input is being controlled and the program exit in case of irregularities
def readInput():
    Board.rows, Board.cols = tuple(map(int,input("Insert number of rows and columns ").split()))
    values = list()
    index = tuple()

    for i in range(Board.rows):
        row = list(map(int,input("Insert row %d of values " % i).split()))

        if len(row) != Board.cols:
            print("Error: Too many values in single row")
            sys.exit(1)

        zeroes = [(i,j) for j,x in enumerate(row) if x == 0]
        
        if len(zeroes) > 1 or (len(zeroes) == 1 and index != () ):
            print("Error: Too many white spaces or white space already set")
            sys.exit(1)
        elif len(zeroes) == 1 and index == ():
            index = zeroes.pop()  
                     
        values.append(row)
               
    check =  [elem for row in values for elem in row] 
    if not all(n in range(Board.rows * Board.cols) for n in check):
        print("Error: White space or tile missing")
        sys.exit(1)
        
    return (values,index)


# This is the entry point for the software
if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hb:d:i:h:a:s:m:",["bfs=","dfs=","idfs=","bf=","astar=","sma=","mem="])
        command = opts[0]
        if len(opts) == 2:
            algorithms.memoryLimit = int(opts[1][1])
    except Exception:
        print (helpstr)
        sys.exit(1)
        
    if command[0] == "-h":
        print(helpstr)
    else:
        val = readInput()
        initBoard = Board(*val)
        
        if initBoard.isSolvable() == False:
            print("-1")
            sys.exit(0)
         
        selectedAlgorithm = algos[command[0]]
        if selectedAlgorithm != algorithms.SMA:   
            rootTree = getNodeClass(nodeAttributes + additionalAttributes[selectedAlgorithm])(initBoard)
        else:
            rootTree = NodeSMA(initBoard)
        arguments = (rootTree,)
        
        if selectedAlgorithm == algorithms.BFS or selectedAlgorithm == algorithms.DFS or selectedAlgorithm == algorithms.IDFS:
            order = command[1]
            if not all(c in "LRUD" for c in order) or len(set(order)) != 4 or len(order) != 4:
                print(helpstr)
                print("Error : Order not valid")
                sys.exit(1)
            Board.order = order
            if order[0] == 'R':
                Board.random = True
        else:
            func = heurs.get(command[1])
            if func == None:
                print(helpstr)
                print("Error : Selected heuristic doesn't exist")
                sys.exit(1) 
                
            if selectedAlgorithm != algorithms.bestFirstSearch:
                func = heuristics.getF(func)
                
                
            arguments += (func,)  
        selectedAlgorithm(*arguments)   