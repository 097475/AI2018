'''
Created on 10 ott 2018

@author: Utente_

This module implements the algorithms and the function to rebuild the solution string
'''



from sortedcontainers import SortedSet
from collections import deque
import heapq, math
memoryLimit = 31

# This function given the final node and the hashmap of visited nodes is able to rebuild the solution string
def pathBuilder(visited,node):
    def opp(l):
        if l == "D":
            return "U"
        if l == "U":
            return "D"        
        if l == "L":
            return "R"
        if l == "R":
            return "L"  
    seq = ""
    curr = node.gameBoard
    while visited[curr]["mov"] != "":
        seq += visited[curr]["mov"]
        tmp = curr.applyMove(opp(visited[curr]["mov"])) ##board opposta
        curr = tmp
    return "".join(reversed(seq)) 

# This functions implements Breadth-First Search
# The specified search order is already respected by queueing each child in the given order
def BFS(root):
    toVisit = deque([root])
    visited = dict()
    visited[root.gameBoard] = {"mov" :root.sequence}
    while toVisit != []:
        curr = toVisit.popleft()
        if curr.gameBoard.isSolved():
            seq = pathBuilder(visited,curr)
            print(len(seq))
            print(seq)
            break
        else :
            children = curr.makeChildren()
            for child in children:
                if child.gameBoard not in visited:
                    toVisit.append(child)
                    visited[child.gameBoard] = {"mov" :child.sequence} 

# This function implements Depth-First Search
# The search order is respected by stacking each child in reversed order
def DFS(root):
    root.depth = 0
    toVisit = [root]
    visited = dict()
    visited[root.gameBoard] = {"mov" :root.sequence, "depth" : root.depth}
    while toVisit != []:
        curr = toVisit.pop()
        if curr.depth > memoryLimit:
            continue
        if curr.gameBoard.isSolved():
            seq = pathBuilder(visited,curr)
            print(len(seq))
            print(seq)
            break
        else :
            children = curr.makeChildren()
            for child in reversed(children):
                child.depth = curr.depth + 1
                lastDepth = visited.get(child.gameBoard)
                if lastDepth == None or lastDepth["depth"] > child.depth:
                    toVisit.append(child) 
                    visited[child.gameBoard] = {"mov" :child.sequence, "depth" : child.depth}

# This function implements Iterative Deepening Depth-First Search
# The search order is respected by stacking each child in reversed order
def IDFS(root):
    for level in range(memoryLimit+1):
        root.depth = 0
        toVisit = [root]
        visited = dict()
        visited[root.gameBoard] = {"mov" :root.sequence, "depth" : root.depth}
        while toVisit != []:
            curr = toVisit.pop()
            if curr.depth > level:
                continue
            if curr.gameBoard.isSolved():
                seq = pathBuilder(visited,curr)
                print(len(seq))
                print(seq)
                break
            else :
                children = curr.makeChildren()
                for child in reversed(children):
                    child.depth = curr.depth + 1
                    lastDepth = visited.get(child.gameBoard)
                    if lastDepth == None or lastDepth["depth"] > child.depth:
                        toVisit.append(child)
                        visited[child.gameBoard] = {"mov" :child.sequence, "depth" : child.depth}
        else:
            continue
        break


# This function implements Greedy Best-First Search
# The F value of a node is given by the chosen heuristic
def bestFirstSearch(root, h):
    minHeap = []
    visited = dict()
    root.F = h(root)
    heapq.heappush(minHeap,root)
    visited[root.gameBoard] = {"mov" :root.sequence}
    while minHeap != []:
        curr = heapq.heappop(minHeap)
        if curr.gameBoard.isSolved():
            seq = pathBuilder(visited,curr)
            print(len(seq))
            print(seq)
            break
        else :
            children = curr.makeChildren()
            for child in children:
                child.F = h(child)
                if child.gameBoard not in visited:
                    heapq.heappush(minHeap,child)
                    visited[child.gameBoard] = {"mov" :child.sequence}
                
# This function implements A* Search
# The F value is given by g(n) + h(n)                    
def aSearch(root,h):
    minHeap = []
    visited = dict()
    root.G = 0
    root.F = root.G + h(root)
    heapq.heappush(minHeap,root)
    while minHeap != []:
        curr = heapq.heappop(minHeap)
        if curr.gameBoard in visited:
            continue
        visited[curr.gameBoard] = {"mov" :curr.sequence}  
        if curr.gameBoard.isSolved():
            seq = pathBuilder(visited,curr)
            print(len(seq))
            print(seq)
            break
        else :
            children = curr.makeChildren()
            for child in children:
                child.G = curr.G+1
                child.F = child.G + h(child)
                if child.gameBoard not in visited:
                    heapq.heappush(minHeap,child)                   

# This function implements SMA* Search 
def SMA (root,h):
    # Get the deepest, newest, least-F node
    def getTop(frontier):
        best = frontier[0].F
        tmp = [elem for elem in frontier if elem.F == best]
        deepest = tmp[0]
        for elem in tmp[1:]:
            if len(elem.sequence) < len(deepest.sequence) and elem.ID > deepest.ID:
                deepest = elem
        return deepest
    # Back up of F values
    def backup(node):
        if curr.completed() and curr.father != None and curr.father.inMemory:
            prev = curr.F
            frontier.remove(curr)
            curr.F = min([node.F for node in curr.children if node.F != None])
            if curr.forgottenF != None:
                curr.F = min(curr.F,curr.forgottenF)  
            frontier.add(curr)
            if prev != curr.F:
                backup(curr.father)
    # Get the shallowest, oldest, worst-F leaf           
    def removeLeaf(frontier):
        worst  = frontier[-1].F
        tmp = [elem for elem in frontier if elem.F == worst]
        shallowest = tmp[0]
        for elem in tmp[1:]:
            if len(elem.sequence) > len(shallowest.sequence) and elem != getTop(frontier) and elem.ID < shallowest.ID:
                shallowest = elem
        shallowest.inMemory = False
        frontier.remove(shallowest)
        return shallowest    
    # Forget a node and add his father back if necessary                       
    def forget():
        deleted = removeLeaf(frontier)
        if deleted.father.forgottenF == None or deleted.father.forgottenF > deleted.F:
            deleted.father.forgottenF = deleted.F 
        if deleted.father not in frontier and deleted.father != child:
            frontier.add(deleted.father)
            deleted.father.inMemory = True
        
    frontier = SortedSet(key=lambda value: value.F)
    root.G = 0
    root.F = root.G + h(root)
    ID = 0
    root.ID = ID
    root.inMemory = True
    frontier.add(root)
    while len(frontier) > 0:
        curr = getTop(frontier)
        if curr.gameBoard.isSolved():
            print(curr.sequence)
            print(len(curr.sequence))
            break
        else :
            # Get the next child
            child = curr.nextChild()
            # Set its ID
            if child.ID == None:
                child.ID = ID + 1
                ID += 1
            child.G = curr.G + 1
            # Set its F value
            if not child.gameBoard.isSolved() and len(child.sequence)+1 == memoryLimit:
                child.F = math.inf
            elif child.F == None :
                child.F = max(curr.F,child.G + h(child))
                
            # If all children are generated, backup the F values    
            if curr.completed():
                backup(curr)
            # If all the children are in memory, delete the current node    
            full = True
            for elem in curr.children:
                if elem.F != None and elem.F == math.inf:
                    continue
                if elem != child and elem not in frontier:
                    full = False
            if full:
                frontier.remove(curr)
                curr.inMemory = False
              
            # If child is not in memory and it can lead to goal              
            if child not in frontier and child.F < math.inf:
                # Make room for it if necessary
                while len(frontier) + 1 > memoryLimit:
                    forget()
                # Add the node to memory
                frontier.add(child)