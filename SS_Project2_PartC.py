# File : SS_Project2_PartC.py
# Date : 11/01/2025
#   A program to play a two-player Tic-Tac-Toe game implementation,
#   now with an AI opponent powered by a Random Forest model.
#
#   by : Sibi Seenivasan

import pandas as pd
import numpy as np
import random
import time
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

def train_and_get_model():
    """
    Loads the dataset, trains the Random Forest model using GridSearchCV,
    and returns the best-trained model.
    """
    print("Loading game ...")
    
    try:
        # Loading the dataset
        df = pd.read_csv("tictac_single.txt", sep=" ", header=None)
        
        # Separating features (X) and target (y)
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]
        
        # Defining the parameter grid for Random Forest
        param_grid_rf = {'n_estimators': [50, 100, 200], # Number of trees
                         'max_depth': [5, 10, 15, 20, None],     # Max depth of trees
                         'min_samples_leaf': [1, 2, 4, 6, 8]}

        # Initializing GridSearchCV
        rf_grid = GridSearchCV(estimator=RandomForestClassifier(random_state=26),
                                    param_grid=param_grid_rf,
                                     scoring='f1_weighted',
                                     cv=5,
                                     verbose=0,  # Set to 0 for cleaner game output
                                     n_jobs=-1)
        
        # Fitting the model
        model = rf_grid.fit(X, y)
        print("Let's start to play!")
        print("---------------------------------------")
        return model

    except FileNotFoundError:
        print("Please make sure the dataset file is in the same directory.")
        return None
    except Exception as e:
        print(f"An error occurred during AI training: {e}")
        return None

class MLPlayer:
    """
    Manages the AI's logic and move prediction.
    """
    def __init__(self, model):
        # Storing the trained model object
        self.model = model

    def _board_to_model_input(self, board_state):
        # Converting the 2D game board to a 1D flat list for the model
        model_input = []
        for row in board_state:
            for cell in row:
                if cell == 'X':
                    model_input.append(1)
                elif cell == 'O':
                    model_input.append(-1)
                else: # ' '
                    model_input.append(0)
        return model_input

    def _index_to_row_col(self, index):
        # Convert 0-8 index to a (row, col) tuple
        row = index // 3
        col = index % 3
        return (row, col)

    def predict_move(self, board_state):
        # Predicts the best move for 'O' (player -1) given the current board

        # 1. Converting board to model-readable format
        model_input = self._board_to_model_input(board_state)
        
        # 2. Getting prediction
        predicted_index = self.model.predict([model_input])[0]
        
        # 3. Convert index (0-8) to (row, col)
        row, col = self._index_to_row_col(predicted_index)

        if board_state[row][col] == " ":
            return (row, col)
        else:
            # If the model predicts an occupied square
            print("AI model predicted an invalid move. Picking a random valid move.")
            empty_cells = []
            for r in range(3):
                for c in range(3):
                    if board_state[r][c] == " ":
                        empty_cells.append((r, c))
            
            if empty_cells:
                return random.choice(empty_cells)
            else:
                # No empty cells left
                return None 

class Board:
    """
    Manages the state and display of the Tic-Tac-Toe board.
    """
    def __init__(self):
        # Initialize a new, empty board
        self.board_state = [[" " for _ in range(3)] for _ in range(3)]

    def printBoard(self):
        # Displaying the current game board with formatting
        print("-----------------")
        print("R\\C | 0 | 1 | 2 |")
        print("-----------------")
        for idx, row in enumerate(self.board_state):
            # Join with '|' and surround with '|'
            print(f"{idx}   | {' | '.join(cell if cell != ' ' else ' ' for cell in row)} |")
            print("-----------------")
        print() # Add a newline after the board
        
    def reset(self):
        # Reset board to an empty state
        self.board_state = [[" " for _ in range(3)] for _ in range(3)]

class Game:
    """
    Manages the game logic, player turns, and game state.
    """
    def __init__(self, model):
        # Initialize game with board and sets the first player 
        self.board = Board()
        self.turn = 'X'
        self.ml_player = MLPlayer(model) if model else None
        self.game_mode = None # Will be 'hvh' (Human vs Human) or 'hva' (Human vs AI)

    def switchPlayer(self):
        # Switch current player from 'X' to 'O' or 'O' to 'X'
        self.turn = "O" if self.turn == "X" else "X"

    def validateEntry(self, row, col):
        # Checking if a given cell is empty (available)
        return self.board.board_state[row][col] == " "

    def checkFull(self):
        # Checking if the board is full
        for row in self.board.board_state:
            if " " in row:
                return False
        return True

    def checkWin(self):
        # Checking if current player has won
        board = self.board.board_state
        turn = self.turn
        # Check for 3-in-a-row
        for i in range(3):
            # Horizontal check
            if all(board[i][j] == turn for j in range(3)):
                return True
            # Vertical check
            if all(board[j][i] == turn for j in range(3)):
                return True
        # Diagonals check
        if all(board[i][i] == turn for i in range(3)) or all(board[i][2 - i] == turn for i in range(3)):
            return True
        return False

    def checkEnd(self):
        # Checking if the game is over (either by win or draw)
        return self.checkWin() or self.checkFull()

    def get_human_move(self):
        # Get and validate move input from a human player

        while True:
            # 1. Get input
            print(f"{self.turn}'s turn")
            print(f"Where do you want your {self.turn} placed?")
            print("Please enter row number and column number separated by a comma")
            move = input().strip()

            # 2. Input parsing and basic format validation
            try:
                parts = move.split(",")
                row_str = parts[0].strip() if len(parts) > 0 else ""
                col_str = parts[1].strip() if len(parts) > 1 else ""
                
                row, col = int(row_str), int(col_str)
                valid_format = True

            except (ValueError, IndexError):
                valid_format = False
                row_str, col_str = move.split(",") if ',' in move else (move, "")
                row_str = row_str.strip()
                col_str = col_str.strip()
                print(f"You have entered row #{row_str}")
                print("\t\t\tand column #", col_str)
            
            # 3. Validation for out-of-range (0, 1, or 2)
            if valid_format and not (0 <= row <= 2 and 0 <= col <= 2):
                print(f"You have entered row #{row}")
                print(f"\t\t\tand column #", col)
                print() 
                print("Invalid entry: try again.")
                print("Row & column numbers must be either 0, 1, or 2.")
                continue
                
            # 4. Validation for non-numeric or malformed input
            if not valid_format:
                print("Invalid entry: try again.")
                print("Row & column numbers must be either 0, 1, or 2.")
                continue

            # 5. Validation for cell already taken (uses self.validateEntry)
            if not self.validateEntry(row, col):
                print(f"You have entered row #{row}")
                print(f"and column #{col}")
                print("That cell is already taken.")
                print("Please make another selection.")
                continue

            # Valid move
            print(f"You have entered row #{row}")
            print(f"\t  and column #{col}")
            print("Thank you for your selection.")
            return row, col

    def playGame(self):
        # Contains the main loop for playing the Tic-Tac-Toe game

        # Select game mode
        while self.game_mode not in ['hvh', 'hva']:
            print("Select game mode:")
            print("1: Human vs. Human")
            print("2: Human vs. AI")
            mode_choice = input("Enter 1 or 2: ").strip()
            if mode_choice == '1':
                self.game_mode = 'hvh'
            elif mode_choice == '2':
                if self.ml_player:
                    self.game_mode = 'hva'
                else:
                    print("AI model not available. Please check file paths and restart.")
                    return # Exit if model failed to load
            else:
                print("Invalid choice. Please enter 1 or 2.")

        playing = True
        while playing:
            self.board.reset()
            self.turn = "X"  # X always goes first in a new game
            print("New Game: X goes first.")
            self.board.printBoard()
            
            while True:
                
                # Check if it's a human's turn
                if self.turn == 'X' or self.game_mode == 'hvh':
                    row, col = self.get_human_move()
                    self.board.board_state[row][col] = self.turn
                
                # Otherwise, it's the AI's turn
                else:
                    print(f"{self.turn}'s turn (AI is thinking...)")
                    time.sleep(1) # Add a small delay for effect
                    
                    row, col = self.ml_player.predict_move(self.board.board_state)
                    
                    print(f"AI has placed 'O' at row #{row}, column #{col}")
                    self.board.board_state[row][col] = self.turn

                # Post-move actions (common to both human and AI)
                self.board.printBoard()

                # Check for game end (Win or Draw)
                if self.checkWin():
                    if self.game_mode == 'hva' and self.turn == 'O':
                        print("THE AI IS THE WINNER!!!")
                    else:
                        print(f"{self.turn} IS THE WINNER!!!")
                    break
                
                if self.checkFull():
                    print("DRAW! NOBODY WINS!")
                    break
                
                # Switch turn
                self.switchPlayer()

            # Ask to play again
            print("Another game? Enter Y or y for yes.")
            response = input().strip()
            if response.lower() != "y":
                playing = False
                print("Thank you for playing!")

def main():
    # Train the model once when the script starts
    model = train_and_get_model()
    
    # Start the game, passing the trained model to the Game class
    if model:
        game = Game(model)
        game.playGame()

if __name__ == "__main__":
    main()