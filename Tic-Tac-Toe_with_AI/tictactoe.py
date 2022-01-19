import random


class BoardManager:
    def __init__(self):
        self.grid = [[" " for _ in range(3)] for _ in range(3)]
        self.symbol_counter = {"X": 0, "O": 0}
        self.game_over = False

    def __repr__(self):
        return f"BoardManager(grid={self.grid}, symbol_counter={self.symbol_counter}, game_over={self.game_over})"

    def get_empty_cells(self) -> list:
        """ Return a list of all empty cells. """
        empty_cells = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == " ":
                    empty_cells.append([i, j])
        return empty_cells

    def check_user_input(self, coords: list, symbol: str) -> None:
        """ Check if the user input is valid. If it is, confirm the input, otherwise print a message. """
        # check if input format is correct
        if len(coords) != 2 or not (coords[0].isdigit() and coords[1].isdigit()):
            print("You should enter numbers!")
            return
        else:
            coords = [int(coords[0]), int(coords[1])]

        # check if input coordinates are correct
        if coords[0] > 3 or coords[1] > 3 or coords[0] < 1 or coords[1] < 1:
            print("Coordinates should be from 1 to 3!")
            return
        elif self.grid[coords[0] - 1][coords[1] - 1] != " ":
            print("This cell is occupied! Choose another one!")
            return
        else:
            self.confirm_input(symbol, coords)

    def check_computer_input(self, coords: list, symbol: str, difficulty: str) -> None:
        """ Check if the computer input is valid. If it is, confirm the input. """
        if not(self.grid[coords[0] - 1][coords[1] - 1] != " "):
            print(f"Making move level \"{difficulty}\"")
            self.confirm_input(symbol, coords)
    
    def check_for_winning_move(self, symbol) -> list:
        """ Return the coordinate of a cell if the symbol's player is one move away from winning.
         Return [-1, -1] if there is no winning move. """
        # check rows
        for row in range(len(self.grid)):
            line = []
            for j in range(len(self.grid)):
                line.append(self.grid[row][j])
            if line.count(symbol) == 2 and line.count(" ") == 1:
                j = line.index(" ")
                return [row + 1, j + 1]
        # check columns
        for column in range(len(self.grid[0])):
            line = []
            for i in range(len(self.grid)):
                line.append(self.grid[i][column])
            if line.count(symbol) == 2 and line.count(" ") == 1:
                i = line.index(" ")
                return [i + 1, column + 1]
        # check diagonals
        diagonal = []
        empty_coords = []
        for i in range(len(self.grid[0])):
            j = i
            diagonal.append(self.grid[i][j])
            if self.grid[i][j] == " ":
                empty_coords = [i + 1, j + 1]
        if diagonal.count(symbol) == 2 and diagonal.count(" ") == 1:
            return empty_coords
        diagonal2 = []
        for i in range(len(self.grid[0])):
            j = 2 - i
            diagonal2.append(self.grid[i][j])
            if self.grid[i][j] == " ":
                empty_coords = [i + 1, j + 1]
        if diagonal2.count(symbol) == 2 and diagonal2.count(" ") == 1:
            return empty_coords
        return [-1, -1]

    def grid_from_string(self, state: str) -> None:
        """ Translates the string to the grid. The string must contain exactly 9 characters. """
        if len(state) == 9:
            for i in range(len(state)):
                self.grid[i // 3][i % 3] = state[i]
                if state[i] == "X" or state[i] == "O":
                    self.symbol_counter[state[i]] += 1

    def make_random_move(self) -> list:
        """ Return the coordinates of a random empty cell on the board. """
        empty_cells = self.get_empty_cells()
        cell = random.choice(empty_cells)
        print(cell)
        return [cell[0] + 1, cell[1] + 1]
        
    def confirm_input(self, symbol: str, coords: list) -> None:
        """ Fill the cell on given coordinate with the symbol. """
        self.grid[coords[0] - 1][coords[1] - 1] = symbol
        self.print_grid()
        self.symbol_counter[symbol] += 1

    def print_grid(self) -> None:
        """ Print the board in it's current state in a specific format. """
        line = "---------"
        print(line)
        for row in self.grid:
            print("| ", end="")
            for symbol in row:
                print(symbol + " ", end="")
            print("|")
        print(line)

    def analyze_game_state(self) -> str:
        """ Return the winner's symbol if there is a winner on the board.
        Return "Draw" in case of a draw and empty string otherwise"""
        winner = ""
        # check rows
        for row in range(len(self.grid)):
            if self.grid[row][0] == self.grid[row][1] == self.grid[row][2] and self.grid[row][0] != " ":
                winner = self.grid[row][0]
        # check columns
        for column in range(len(self.grid[0])):
            if self.grid[0][column] == self.grid[1][column] == self.grid[2][column] and self.grid[0][column] != " ":
                winner = self.grid[0][column]
        # check diagonals
        if self.grid[0][0] == self.grid[1][1] == self.grid[2][2] and self.grid[1][1] != " ":
            winner = self.grid[0][0]
        if self.grid[2][0] == self.grid[1][1] == self.grid[0][2] and self.grid[1][1] != " ":
            winner = self.grid[2][0]

        if winner == "X" or winner == "O":
            return winner
        elif winner == "" and self.get_empty_cells() == []:
            return "Draw"
        else:
            return ""


class GameManager:
    def __init__(self):
        self.initial_state = "         "
        self.difficulties = ["easy", "medium", "hard"]
        self.player1 = ""
        self.player2 = ""
        self.board = BoardManager()
        self.function_calls = 0

    def who_plays_next(self) -> tuple:
        """ Return the player and his symbol whose turn it is. """
        if self.board.symbol_counter["X"] == self.board.symbol_counter["O"]:
            return self.player1, "X"
        else:
            return self.player2, "O"

    def easy_move(self, symbol: str) -> None:
        """ Make a move with the "easy" AI.
        This is a random move."""
        coordinates = self.board.make_random_move()
        self.board.check_computer_input(coordinates, symbol, "easy")

    def medium_move(self, symbol: str) -> None:
        """ Make a move with the "medium" AI.
        It looks one move ahead. If it finds a winning move, it makes the move.
        Else if it finds that the opponent is one move away from winning, it blocks it.
        Else it makes a random move. """
        coordinates = self.board.check_for_winning_move(symbol)
        if coordinates == [-1, -1]:
            enemy_symbol = "X" if symbol == "O" else "O"
            coordinates = self.board.check_for_winning_move(enemy_symbol)
            if coordinates == [-1, -1]:
                coordinates = self.board.make_random_move()
        self.board.check_computer_input(coordinates, symbol, "medium")

    def hard_move(self, symbol: str) -> None:
        """ Make a move with the "hard" AI.
        Determines and makes the best possible move using the minimax algorithm. (Will never lose) """
        self.function_calls = 0
        new_board = BoardManager()
        new_board.grid = self.board.grid
        best_move = self.minimax(new_board, symbol, symbol)
        # Take the coordinates of the return move, discard the score as it doesn't interest us anymore.
        i, j = best_move["coordinates"]
        self.board.check_computer_input([i + 1, j + 1], symbol, "hard")
        # print(self.function_calls)  # uncomment to print the number of function calls on minimax()

    def minimax(self, new_board: BoardManager, symbol: str, own_symbol: str) -> dict:
        """ Return the best possible move using the minimax algorithm. Takes a board, a player symbol and the symbol
        of the player, that want's to calculate the move.

        This is a copy of the tutorial (https://www.freecodecamp.org/news/how-to-make-your-tic-tac-toe-game-unbeatable-by-using-the-minimax-algorithm-9d690bad4b37/),
        translated to python and slightly modified to work with the rest of this script. Most notably, his allows the
        game to run two AIs with this algorithm against each other. """

        # Just to track the number of function calls.
        self.function_calls += 1
        # A list of all remaining empty cells on the board
        available_cells = new_board.get_empty_cells()
        # Determines the symbol of the enemy player, so that two AIs can run the algorithm against each other.
        enemy_symbol = "X" if own_symbol == "O" else "O"
        # Checks for the terminal states win, lose and draw and returns a value accordingly.
        state = new_board.analyze_game_state()
        if state == own_symbol:
            return {"coordinates": [], "score": 10}
        elif state == enemy_symbol:
            return {"coordinates": [], "score": -10}
        elif len(available_cells) == 0:
            return {"coordinates": [], "score": 0}

        # A list to store all the moves
        moves = []

        # Loop through empty cells
        for i in range(len(available_cells)):
            # Create a move dict, that contains the coordinates and the score of the move.
            move = {}
            coords = available_cells[i]
            # Assign the coordinates to the move
            move["coordinates"] = coords
            # Set the empty cell to the current players symbol
            new_board.grid[coords[0]][coords[1]] = symbol

            # Collect the score resulting from calling minimax on the opponent of the current player.
            if symbol == own_symbol:
                result = self.minimax(new_board, enemy_symbol, own_symbol)
                move["score"] = result["score"]
            else:
                result = self.minimax(new_board, own_symbol, own_symbol)
                move["score"] = result["score"]

            # Reset the cell to be empty
            new_board.grid[coords[0]][coords[1]] = " "
            # Put the move to the end of the list.
            moves.append(move)

        # If it is the player's turn, who originally called the function, loop through the moves and choose the
        # move with the highest score
        best_move = []
        if symbol == own_symbol:
            best_score = -10000
            for move in moves:
                if move["score"] > best_score:
                    best_score = move["score"]
                    best_move = move
        # Else loop through the moves and choose the move with the lowest score
        else:
            best_score = 10000
            for move in moves:
                if move["score"] < best_score:
                    best_score = move["score"]
                    best_move = move

        # Return chosen best move from the moves array.
        # Remember, a move is a dict that contains the coordinates and score associated with it.
        return best_move

    def menu_loop(self) -> None:
        """ Menu loop, loop until valid parameters are entered by the user.
        Start the game with specified players/AIs or exit the script. """
        print("Accepted command: start/exit user/difficulty user/difficulty (difficulty = easy/medium/hard)")
        valid_params = False
        while not valid_params:
            params = input("Input command: ").split()
            if params[0] == "exit":
                exit()
            if len(params) == 3 and params[0] == "start" \
                    and (params[1] == "user" or params[1] in self.difficulties) \
                    and (params[2] == "user" or params[2] in self.difficulties):
                self.player1 = params[1]
                self.player2 = params[2]
                valid_params = True
            else:
                print("Bad parameters!")
        # start the game if all parameters are valid
        self.start_game()

    def start_game(self) -> None:
        """ Create a new board. If the board is supposed to have an initial not empty state,
        change the self.initial_state string in the __init__ method.
        Start the main game loop. """
        self.board.__init__()
        self.board.grid_from_string(self.initial_state)
        self.board.print_grid()
        self.game_loop()

    def end_game(self, end_state) -> None:
        """ Print the result of game and declare the game as over. """
        if end_state == "Draw":
            print("Draw")
        else:
            print(f"{end_state} wins")
        self.board.game_over = True

    def game_loop(self) -> None:
        """ Main game loop, run until the game is over.
        Go back to the menu after. """
        while not self.board.game_over:
            current_player, symbol = self.who_plays_next()
            if current_player == "user":
                coordinates = input("Enter the coordinates: ").split()
                self.board.check_user_input(coordinates, symbol)
            elif current_player == "easy":
                self.easy_move(symbol)
            elif current_player == "medium":
                self.medium_move(symbol)
            elif current_player == "hard":
                self.hard_move(symbol)

            # Check if game is over
            state = self.board.analyze_game_state()
            if state == symbol or state == "Draw":
                self.end_game(state)

        # Go back to menu after game is over
        self.menu_loop()


def main():
    random.seed()
    game = GameManager()
    game.menu_loop()


if __name__ == "__main__":
    main()
