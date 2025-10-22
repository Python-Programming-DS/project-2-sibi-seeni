# File : SS_Project2_PartA.py
# Date : 10/26/2025
#   A program to play a two-player Tic-Tac-Toe game implementation
#   (Rewritten into OOP structure)
#
#   by : Sibi Seenivasan 

class Board:
    """
    Manages the state and display of the Tic-Tac-Toe board.
    """
    def __init__(self):
        # Initializes a new, empty board
        self.board_state = [[" " for _ in range(3)] for _ in range(3)]

    def printBoard(self):
        # Displays the current game board with formatting
        print("-----------------")
        print("R\\C | 0 | 1 | 2 |")
        print("-----------------")
        for idx, row in enumerate(self.board_state):
            # Join with '|' and surround with '|'
            print(f"{idx}   | {' | '.join(cell if cell != ' ' else ' ' for cell in row)} |")
            print("-----------------")
        print() # Add a newline after the board
        
    def reset(self):
        # Resets the board to an empty state
        self.board_state = [[" " for _ in range(3)] for _ in range(3)]

class Game:
    """
    Manages the game logic, player turns, and game state.
    """
    def __init__(self):
        # Initializes the game with a board and sets the first player 
        self.board = Board()
        self.turn = 'X'

    def switchPlayer(self):
        # Switches the current player from 'X' to 'O' or 'O' to 'X'
        self.turn = "O" if self.turn == "X" else "X"

    def validateEntry(self, row, col):
        # Checks if a given cell is empty (available)
        return self.board.board_state[row][col] == " "

    def checkFull(self):
        # Checks if the board is full
        for row in self.board.board_state:
            if " " in row:
                return False
        return True

    def checkWin(self):
        # Checks if the current player (self.turn) has won
        board = self.board.board_state
        turn = self.turn
        # Checks for 3-in-a-row horizontally, vertically, or diagonally
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
        # Checks if the game is over (either by a win or a draw)
        # Game is over if there is a winner OR the board is full
        return self.checkWin() or self.checkFull()

    def playGame(self):
        """
        Contains the main loop for playing the Tic-Tac-Toe game.
        """
        playing = True
        while playing:
            self.board.reset()
            self.turn = "X"  # X always goes first in a new game
            print("New Game: X goes first.")
            self.board.printBoard()
            
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
                
                self.board.board_state[row][col] = self.turn
                self.board.printBoard()

                # 6. Check for game end (Win or Draw)
                if self.checkWin():
                    print(f"{self.turn} IS THE WINNER!!!")
                    break
                
                if self.checkFull():
                    print("DRAW! NOBODY WINS!")
                    break
                
                # 7. Switch turn
                self.switchPlayer()

            # Ask to play again
            print("Another game? Enter Y or y for yes.")
            response = input().strip()
            if response.lower() != "y":
                playing = False
                print("Thank you for playing!")

def main():
    game = Game()
    game.playGame()

if __name__ == "__main__":
    main()