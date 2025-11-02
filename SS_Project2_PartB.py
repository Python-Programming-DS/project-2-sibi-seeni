# File : SS_TicTacToe.py
# Date : 10/31/2025
#   A program to play a two-player Tic-Tac-Toe game implementation
#   (With Minimax)
#
#   by : Sibi Seenivasan

# Defining players for clarity in Minimax
COMPUTER_PLAYER = 'O'
HUMAN_PLAYER = 'X'

def _get_available_moves(board_state):
    # Return a list of (row, col) tuples for all empty cells
    moves = []
    for r in range(3):
        for c in range(3):
            if board_state[r][c] == ' ':
                moves.append((r, c))
    return moves

def _check_win_utility(board_state, player):
    # Check if a specific player has won on a given board_state

    # Horizontal check
    for i in range(3):
        if all(board_state[i][j] == player for j in range(3)):
            return True
    # Vertical check
    for i in range(3):
        if all(board_state[j][i] == player for j in range(3)):
            return True
    # Diagonal check
    if (all(board_state[i][i] == player for i in range(3)) or
        all(board_state[i][2 - i] == player for i in range(3))):
        return True
    return False

def _check_full_utility(board_state):
    # Checking if a given board_state is full
    for row in board_state:
        if " " in row:
            return False
    return True

def _minimax(board_state, depth, is_maximizing):
    
    # Minimax recursive helper function

    if _check_win_utility(board_state, COMPUTER_PLAYER):
        return 10  # Computer wins
    if _check_win_utility(board_state, HUMAN_PLAYER):
        return -10 # User wins
    if _check_full_utility(board_state):
        return 0   # Draw
    
    if is_maximizing: # Computer's turn (O)
        best_score = -float('inf')
        for (r, c) in _get_available_moves(board_state):
            board_state[r][c] = COMPUTER_PLAYER
            score = _minimax(board_state, depth + 1, False) # Next is minimizer
            board_state[r][c] = ' ' # Undo move
            best_score = max(score, best_score)
        return best_score
    
    else: # Minimizing player's turn (Human, X)
        best_score = float('inf')
        for (r, c) in _get_available_moves(board_state):
            board_state[r][c] = HUMAN_PLAYER
            score = _minimax(board_state, depth + 1, True) # Next is maximizer
            board_state[r][c] = ' ' # Undo move
            best_score = min(score, best_score)
        return best_score

def findBestMove(board_state):
    
    # Finds the best move for the Computer (O) by iterating all possible moves and evaluating them with the minimax algorithm.

    best_score = -float('inf')
    best_move = None
    
    for (r, c) in _get_available_moves(board_state):
        board_state[r][c] = COMPUTER_PLAYER  
        # We call minimax with 'False' because after the COMPUTER makes a move, it's the minimizing player's (Human's) turn.

        move_score = _minimax(board_state, 0, False)
        board_state[r][c] = ' '             # Undo the move

        if move_score > best_score:
            best_score = move_score
            best_move = (r, c)
            
    return best_move

# --- Game Classes ---

class Board:
    """Manages the state and display of the Tic-Tac-Toe board."""

    def __init__(self):
        # Initializes a new, empty board
        self.board_state = [[" " for _ in range(3)] for _ in range(3)]

    def printBoard(self):
        # Displays the current game board with formatting
        print("-----------------")
        print("R\\C | 0 | 1 | 2 |")
        print("-----------------")
        for idx, row in enumerate(self.board_state):
            print(f"{idx}   | {' | '.join(cell if cell != ' ' else ' ' for cell in row)} |")
            print("-----------------")
        print() 

    def reset(self):
        # Resets the board to an empty state
        self.board_state = [[" " for _ in range(3)] for _ in range(3)]

class Game:
    """Manages the game logic, player turns, and game state."""

    def __init__(self, game_mode):
        # Initializes the game with a board and sets the first player
        self.board = Board()
        self.turn = 'X' # Human (X) always goes first
        self.game_mode = game_mode # 'pvp' or 'pvc'

    def switchPlayer(self):
        # Switches the current player from 'X' to 'O' or 'O' to 'X'
        self.turn = "O" if self.turn == "X" else "X"

    def validateEntry(self, row, col):
        # Checks if a given cell is empty (available)
        return self.board.board_state[row][col] == " "

    def checkFull(self):
        # Checks if the board is full
        return _check_full_utility(self.board.board_state)

    def checkWin(self):
        # Checks if the current player (self.turn) has won
        return _check_win_utility(self.board.board_state, self.turn)

    def checkEnd(self):
        # Checks if the game is over (either by a win or a draw)
        return self.checkWin() or self.checkFull()

    def get_human_move(self):
        # Handles all input and validation for a human player

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
            return row, col # Return the valid move

    def playGame(self):
        """
        Contains the main loop for playing the Tic-Tac-Toe game.
        """
        playing = True
        while playing:
            self.board.reset()
            self.turn = "X"  # X always goes first
            print("New Game: X goes first.")
            self.board.printBoard()
            
            while True:
                # Decide whose turn it is
                is_ai_turn = (self.game_mode == 'pvc' and self.turn == COMPUTER_PLAYER)

                if is_ai_turn:
                    print(f"{self.turn}'s turn (Computer)")
                    row, col = findBestMove(self.board.board_state)
                    print(f"Computer chose row #{row} and column #{col}")
                else:
                    # Get move from human player (Player 1 or Player 2)
                    row, col = self.get_human_move()

                # Apply the move to the board
                self.board.board_state[row][col] = self.turn
                self.board.printBoard()

                # Check for game end (Win or Draw)
                if self.checkWin():
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
    """
    Main function to start the game.
    Asking the user for the game mode.
    """
    print("Welcome to Tic-Tac-Toe!")
    game_mode = ''
    while game_mode not in ('1', '2'):
        print("Select game mode:")
        print(" (1) Player vs Player")
        print(" (2) Player vs Computer")
        choice = input().strip()
        
        if choice == '1':
            game_mode = 'pvp'
            break
        elif choice == '2':
            game_mode = 'pvc'
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

    game = Game(game_mode)
    game.playGame()

if __name__ == "__main__":
    main()
