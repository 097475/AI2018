'''
Created on 10 ott 2018

@author: Utente_
'''
#from node import Tree
#from board import Board
#import main

from heuristics import g
from sortedcontainers import SortedSet
import heapq, math
memoryLimit = 9999

# This functions implements Breadth-First Search
# The specified search order is already respected by queueing each child in the given order
def BFS(root):
    toVisit = [root]
    visited = set()
    while toVisit != []:
        curr = toVisit.pop(0)
        visited.add(curr)
        if curr.gameBoard.isSolved():
            print(len(curr.sequence))
            print(curr.sequence)
            break
        else :
            children = curr.makeChildren()
            for child in children:
                if child not in visited:
                    toVisit.append(child) 

# This function implements Depth-First Search
# The search order is respected by stacking each child in reversed order
def DFS(root):
    toVisit = [root]
    visited = dict()
    while toVisit != []:
        curr = toVisit.pop()
        visited[curr] = len(curr.sequence)
        if len(curr.sequence) > memoryLimit:
            continue
        if curr.gameBoard.isSolved():
            print(len(curr.sequence))
            print(curr.sequence)
            break
        else :
            children = curr.makeChildren()
            for child in reversed(children):
                lastDepth = visited.get(child)
                if lastDepth == None or lastDepth > len(child.sequence):
                    toVisit.append(child) 

# This function implements Iterative Deepening Depth-First Search
# The search order is respected by stacking each child in reversed order
def IDFS(root):
    for level in range(memoryLimit+1):
        toVisit = [root]
        visited = dict()
        while toVisit != []:
            curr = toVisit.pop()
            visited[curr] = len(curr.sequence)
            if len(curr.sequence) > level:
                continue
            if curr.gameBoard.isSolved():
                print(len(curr.sequence))
                print(curr.sequence)
                break
            else :
                children = curr.makeChildren()
                for child in reversed(children):
                    lastDepth = visited.get(child)
                    if lastDepth == None or lastDepth > len(child.sequence):
                        toVisit.append(child)
        else:
            continue
        break


# This function implements Greedy Best-First Search
# The F value of a node is given by the chosen heuristic
def bestFirstSearch(root, h):
    i = 0
    visited = set()
    minHeap = []
    heapq.heappush(minHeap,(h(root),i,root))
    while minHeap != []:
        curr = heapq.heappop(minHeap)[2]
        visited.add(curr)
        if curr.gameBoard.isSolved():
            print(len(curr.sequence))
            print(curr.sequence)
            break
        else :
            children = curr.makeChildren()
            for child in children:
                if child not in visited:
                    i+=1
                    heapq.heappush(minHeap,(h(child),i,child))
                
# This function implements A* search
# The F value is given by g(n) + h(n)
# If a node is found but already in the open list, it is swapped if the g(n) value is lower                    
def aSearch(root,f):
    minHeap = []
    closedNodes = set()
    openNodes = dict()
    root.F = f(root)
    root.G = 0
    heapq.heappush(minHeap,root)
    openNodes[hash(root)] = root;
    while minHeap != []:
        curr = heapq.heappop(minHeap)
        del openNodes[hash(curr)]
        closedNodes.add(curr)   
        if curr.gameBoard.isSolved():
            print(len(curr.sequence))
            print(curr.sequence)
            break
        else :
            children = curr.makeChildren()
            for child in children:
                child.G = g(child)
                child.F = f(child)
                if child in closedNodes:
                    continue
                if hash(child) not in openNodes:                     
                    openNodes[hash(child)] = child
                    heapq.heappush(minHeap,child)
                else:
                    othernode = openNodes[hash(child)]
                    if child.G < othernode.G:
                        openNodes[hash(child)] = child
                       
def SMA(root,f):
    def getTop(frontier):
        best = frontier[0].F
        tmp = [elem for elem in frontier if elem.F == best]
        shallowest = tmp[0]
        for elem in tmp[1:]:
            if len(elem.sequence) < len(shallowest.sequence):
                shallowest = elem
        return shallowest
            
    def removeLeaf(frontier):
        i = 1
        while i < len(frontier) + 1:
            worst  = frontier[-i]
            if worst.sequence == "" or worst == getTop(frontier):
                i+=1
                continue
            for child in worst.children:
                if child.inMemory == True:
                    break
            else:
                worst.inMemory = False
                frontier.remove(worst)
                return worst       
            i+=1
            
    def forget():
        deleted = removeLeaf(frontier)
        deleted.inMemory = False
        #deleted.father.resetIterator()
        if deleted.father.forgottenF == None or deleted.father.forgottenF > deleted.F:
            deleted.father.forgottenF = deleted.F 
        if deleted.father not in frontier and deleted.father != child:
            frontier.add(deleted.father)
            deleted.father.inMemory = True
    

    visited = set()
    frontier = SortedSet(key=lambda value: value.F)
    root.F = f(root)
    root.inMemory = True
    frontier.add(root)
    while len(frontier) > 0 :
        curr = getTop(frontier)
        visited.add(curr)
        print(len(frontier))
        print(len(curr.sequence))
        if curr.gameBoard.isSolved():
            print(len(curr.sequence))
            print(curr.sequence)
            break
        else:
            child = curr.nextChild()
            #print(curr.sequence +"->"+child.sequence)
            if child != None and child.F == None:
                if not child.gameBoard.isSolved() and len(child.sequence)+1 == memoryLimit:
                    child.F = math.inf
                else :
                    child.F = max(curr.F,f(child))
            ###backup###
            if curr.completed():
                frontier.remove(curr)
                curr.F = min([node.F for node in curr.children if node.F != None])  
                frontier.add(curr)
                currF = curr.F
                tmp = curr.father                  
                while tmp != None and tmp in frontier: 
                    if tmp.forgottenF != None:
                        frontier.remove(tmp)
                        tmp.F = min(currF,tmp.forgottenF)
                        frontier.add(tmp)
                        currF = tmp.F
                        tmp = tmp.father
                    else:
                        break
                    
            ###delete full node###
            full = True
            for elem in curr.children:
                if elem.F != None and elem.F == math.inf:
                    continue
                if elem != child and elem not in frontier:
                    full = False
            if full:
                #curr.finished = True
                frontier.remove(curr)
                curr.inMemory = False
             
             
            if child != None and child not in frontier:   
                ### add child ####  
                if child.F < math.inf:
                    child.inMemory = True
                    frontier.add(child)
                ###forget a node for memory full###
                while len(frontier) >= memoryLimit:
                    forget()
                        
    


#if __name__ == '__main__':
    #val = main.readInput()
    #initBoard = Board(*val)
    #rootTree = Tree(initBoard)
    #SMA(rootTree,heuristics.getF(heuristics.h2_sumManhattanDistance))