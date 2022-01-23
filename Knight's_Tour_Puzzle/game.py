import copy


class Chessboard:
    """ A class representing a chessboard for the knight's tour puzzle.
    An example for a chessboard should look like in this task:
     ---------------------
    5| __ __ __ __ __ __ |      A board with the dimensions 6*5.
    4| __ __ __ __ __ __ |      x = columns, y = rows
    3| __ __ __ __ __ __ |      e.g. the coordinates of the knight here is (4,2)
    2| __ __ __  X __ __ |
    1| __ __ __ __ __ __ |
     ---------------------
        1  2  3  4  5  6
    """

    def __init__(self, dimensions: list, start_position: list):
        self.cols, self.rows = dimensions
        self.cell_size = len(str(self.rows * self.cols))
        self.border_length = self.cols * (self.cell_size + 1) + 3
        self.knight_position = start_position  # in coordinates
        self.board = [[("_" * self.cell_size) for _ in range(self.cols)] for _ in range(self.rows)]
        self.previous_board = copy.deepcopy(self.board)

    def __str__(self):
        msg = (f"A Chessboard for the knight's tour puzzle with {self.rows} rows and {self.cols} columns.\n"
               f"The knight's current position is ({self.knight_position[0]}, {self.knight_position[1]}).\n"
               f"To print the current board state, use the classes print_board() method. ")
        return msg

    def print_board(self):
        """ Print the chess board with borders and numbered columns and rows. """
        border = " " + "-" * self.border_length
        col_nums = ""
        print(border)
        for row in range(self.rows):
            row_string = str(self.rows - row) + "| "
            for col in range(self.cols):
                row_string += self.board[row][col] + " "
            row_string += "|"
            print(row_string)
        print(border)
        for col in range(self.cols):
            col_nums += " " * self.cell_size + str(col + 1)
        print("  " + "".join([" " * self.cell_size + str(col + 1) for col in range(self.cols)]))

    def coords_to_index(self, coords: list) -> list:
        """ Return indices for a matrix converted from coordinates. coords (x,y) -> board[i][j]
        Example:     ---------------------
                    5| __ __ __ __ __ __ |      coordinates (4,2) -> board[3, 3]
                    4| __ __ __ __ __ __ |
                    3| __ __ __ __ __ __ |
                    2| __ __ __  X __ __ |
                    1| __ __ __ __ __ __ |
                     ---------------------
                        1  2  3  4  5  6
        """
        return [self.rows - coords[1], coords[0] - 1]

    def index_to_coords(self, coords: list) -> list:
        """ Return coordinates converted from indices for a matrix. board[i][j] -> coordinates (4,2)
        (reverse of coord_to_index()) """
        return [coords[1] + 1, self.rows - coords[0]]

    def set_knight_position(self, coords: list):
        """ Set the knights position to given coordinates with an "X".
        His old position is set to "*" """
        if self.knight_position:
            old_position = self.coords_to_index(self.knight_position)
            self.board[old_position[0]][old_position[1]] = " " * (self.cell_size - 1) + "*"
        i, j = self.coords_to_index(coords)
        self.board[i][j] = " " * (self.cell_size - 1) + "X"
        self.knight_position = coords

    def possible_moves(self, coords: list) -> list:
        """ Return a list of the coordinates of all the possible next knight moves from a given position."""
        moves = []
        position = self.coords_to_index(coords)
        for x in [-2, 2]:
            for y in [-1, 1]:
                i, j = position[0] + x, position[1] + y
                if 0 <= i < self.rows and 0 <= j < self.cols:
                    if self.board[i][j] == ("_" * self.cell_size):
                        moves.append([i, j])
        for x in [-1, 1]:
            for y in [-2, 2]:
                i, j = position[0] + x, position[1] + y
                if 0 <= i < self.rows and 0 <= j < self.cols:
                    if self.board[i][j] == ("_" * self.cell_size):
                        moves.append([i, j])
        return [self.index_to_coords(move) for move in moves]

    def count_visited_cells(self) -> int:
        """ Return the number of cells that were visited by the knight. """
        counter = 0
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != "_" * self.cell_size:
                    counter += 1
        return counter

    def save_board(self) -> None:
        """ Save a copy of the current board. """
        self.previous_board = copy.deepcopy(self.board)

    def restore_board(self) -> None:
        """ Restore the previous board."""
        self.board = copy.deepcopy(self.previous_board)

    def mark_landing_positions(self, moves: list) -> None:
        """ Mark the landing positions on the board with the number of possible next moves from that new position. """
        self.save_board()
        for move in moves:
            number_of_next_moves = len(self.possible_moves(move))
            self.board[self.rows - move[1]][move[0] - 1] = " " * (self.cell_size - 1) + str(number_of_next_moves)

    def make_move(self, coords: list) -> None:
        """ Make the move to the given coordinate and print the board. """
        self.set_knight_position(coords)
        self.save_board()
        self.mark_landing_positions(self.possible_moves(self.knight_position))
        self.print_board()
        self.restore_board()


def input_board_dimensions_loop() -> list:
    """ Return board dimensions from user input. The input must look like this:
    <int int> and the dimensions must be >= 0, otherwise an error gets printed. Repeat until
    an input is valid. """
    valid_input = False
    while not valid_input:
        dimensions = input("Enter you board dimensions: ").split()
        if len(dimensions) == 2:
            if dimensions[0].isdigit() is True and dimensions[1].isdigit() is True:
                dimensions = [int(dimensions[0]), int(dimensions[1])]
                if not (dimensions[0] < 1 or dimensions[1] < 1):
                    return dimensions
        print("Invalid dimensions!")


def input_start_position_loop(dimensions: list) -> list:
    """ Return coordinates from user input. The input must look like this:
    <int int> and the coordinates must be within the board dimensions the function takes in, otherwise an error gets
    printed. Repeat until an input is valid. """
    valid_input = False
    while not valid_input:
        coordinates = input("Enter the knight's starting position: ").split()
        if len(coordinates) == 2:
            if coordinates[0].isdigit() is True and coordinates[1].isdigit() is True:
                coordinates = [int(coordinates[0]), int(coordinates[1])]
                if 1 <= coordinates[0] <= dimensions[0] and 1 <= coordinates[1] <= dimensions[1]:
                    return coordinates
        print("Invalid position!")


def select_mode_loop() -> str:
    """ Return if the user wants to solve the puzzle or see the solution (y/n). Repeat until an input is valid. """
    while True:
        mode = input("Do you want to try the puzzle? (y/n): ")
        if mode in ("y", "n"):
            return mode
        else:
            print("Invalid input!")


def input_next_move_loop(possible_moves: list) -> list:
    """ Return coordinates from user input. Take in a list of possible moves. The input must look like this:
        <int int> and the coordinates represent a possible move from the list, otherwise an error gets
        printed. Repeat until an input is valid. """
    valid_input = False
    while not valid_input:
        coordinates = input("Enter your next move: ").split()
        if len(coordinates) == 2:
            if coordinates[0].isdigit() is True and coordinates[1].isdigit() is True:
                coordinates = [int(coordinates[0]), int(coordinates[1])]
                if coordinates in possible_moves:
                    return coordinates
        print("Invalid move! ", end="")


def player_loop(board: Chessboard) -> None:
    """ Move the knight and loop until there are no more possible moves. """
    while board.possible_moves(board.knight_position):
        coords = input_next_move_loop(board.possible_moves(board.knight_position))
        board.make_move(coords)
    # Print the results
    visited_cells = board.count_visited_cells()
    if visited_cells == board.rows * board.cols:
        print("\nWhat a great tour! Congratulations!")
    else:
        print(f"\nNo more possible moves!\nYour knight visited {visited_cells} squares!")


def show_solution(board: Chessboard) -> None:
    """ Print the solution of the puzzle. """
    print("\nHere's the solution!")
    board.print_board()


def warnsdorff(board: Chessboard, call: int) -> tuple[Chessboard, bool]:
    """ Return the solved board based on Warnsdorff's rule. If the board is not solvable, return the board solved
     up to a dead end. """
    solved = False
    # Number of the current move
    current_move = call
    # Indices of the knight's current position
    i, j = board.coords_to_index(board.knight_position)
    # List of all the possible moves from the knight's current position
    possible_moves = board.possible_moves(board.knight_position)

    # If there are no more moves, return the board and a bool signaling if the puzzle was solved or not
    if not possible_moves:
        board.board[i][j] = " " * (board.cell_size - len(str(current_move))) + str(current_move)
        # Board solved
        if board.count_visited_cells() == board.rows * board.cols:
            return board, True
        # Dead end
        else:
            board.board[i][j] = "_" * board.cell_size
            return board, False

    while not solved and possible_moves:
        # Find the next move based on Warnsdorff's rule. (next move is the move with the least possible next moves)
        next_move = []
        minimum = None
        for move in possible_moves:
            if minimum:
                if minimum > len(board.possible_moves(move)):
                    minimum = len(board.possible_moves(move))
                    next_move = move
            else:
                minimum = len(board.possible_moves(move))
                next_move = move

        # Set the current cell to the number of the current move and move the knight to that position
        board.board[i][j] = " " * (board.cell_size - len(str(current_move))) + str(current_move)
        board.knight_position = next_move

        # Recursive call for the next move
        board, solved = warnsdorff(board, current_move + 1)

        # If a dead end was reached, reset the board to what it was before the move
        if not solved:
            possible_moves.pop(possible_moves.index(next_move))
            board.board[i][j] = "_" * board.cell_size
            board.knight_position = board.index_to_coords([i, j])

    return board, solved


def main():
    # Set up the board and the knight's starting point
    dimensions = input_board_dimensions_loop()
    start_position = input_start_position_loop(dimensions)
    board = Chessboard(dimensions, start_position)

    # Ask the user if he wants to play or just see the solution
    mode = select_mode_loop()

    # Try to solve the board on a copy of the set-up board
    solved_board, solved = warnsdorff(copy.deepcopy(board), 1)

    # Check if the puzzle has a solution
    if solved:
        # It there is a solution, enter the user's chosen mode
        if mode == "y":
            board.make_move(start_position)
            player_loop(board)
        elif mode == "n":
            show_solution(solved_board)
    else:
        print("No solution exists!")


if __name__ == "__main__":
    main()
