'''
Created on 11 ott 2018

@author: Utente_

This script verifies a previously found solution step by step
'''
from board import Board
import main 
import sys

helpstr = '''
commands :
step  - move ahead by 1
jump n - move ahead by n
exec - executes all moves
help - show this help dialog
exit - close the program
'''
# Executes the given sequence on the gameBoard, exit if unallowed move is submitted
def verify(gameBoard,sequence):
    for mov in sequence:
        availMoves = gameBoard.getMoves() # List of allowed moves
        if mov in availMoves:
            gameBoard = gameBoard.applyMove(mov) # If mov is in list, execute it
        else:
            print("Unallowed move submitted: "+mov) # Exit otherwise
            print("Exiting...\n")
            sys.exit(1)    
    print(gameBoard)
    
    if gameBoard.isSolved():
        print("The solution is correct!")
        
    return gameBoard



if __name__ == '__main__':
    # Reads the board and the solution to verify
    print("Inserting the board\n")
    board = Board(*main.readInput())
    solution = input("Insert the solution to test\n")

    # The program is now listening for commands, as specified in helpstr
    print(helpstr)
    while True:
        command = input(">>>(Type 'exit' to terminate) ").split()
        if command[0] == "exec":
            verify(board,solution) # Executes the whole solution string
        elif command[0] == "step":
            board=verify(board,solution[:1]) # Executes only the next move in solution
            solution = solution[1:]          # The solution string moves ahead by one
        elif command[0] == "jump":
            jump = int(command[1])              
            board=verify(board,solution[:jump]) # Executes the next "jump" moves
            solution = solution[jump:]          # The solution string moves ahead by "jump"
        elif command[0] == "help":
            print(helpstr)
        elif command[0] == "exit":
            print("Program terminated.")
            break
        else:
            print("Unrecognized command")

            
