line = "---------"
grid = [[" " for i in range(3)] for j in range(3)]
empty_cells = 9
game_over = False
current_player = "X"


def check_user_input(coords: list) -> bool:
    if coords[0] > 3 or coords[1] > 3 or coords[0] < 1 or coords[1] < 1:
        print("Coordinates should be from 1 to 3!")
        return False
    elif type(coords[0]) != int or type(coords[1]) != int:
        print("You should enter numbers!")
        return False
    elif grid[coords[0] - 1][coords[1] - 1] != " ":
        print("This cell is occupied! Choose another one!")
        return False
    else:
        return True


def print_grid() -> None:
    print(line)
    for row in grid:
        print("| ", end="")
        for symbol in row:
            print(symbol + " ", end="")
        print("|")
    print(line)


def analyze_game_state() -> None:
    global game_over
    winner = ""
    # check rows
    for row in range(len(grid)):
        if grid[row][0] == grid[row][1] == grid[row][2]:
            winner = grid[row][0]
    # check columns
    for column in range(len(grid[0])):
        if grid[0][column] == grid[1][column] == grid[2][column]:
            winner = grid[0][column]
    # check diagonals
    if grid[0][0] == grid[1][1] == grid[2][2]:
        winner = grid[0][0]
    if grid[2][0] == grid[1][1] == grid[0][2]:
        winner = grid[2][0]

    if winner == "X" or winner == "O":
        print(f"{winner} wins")
        game_over = True
    elif winner == "" and empty_cells == 0:
        print("Draw")
        game_over = True


print_grid()

while not game_over:
    coordinates = input("Enter the coordinates").split()
    coordinates = [int(coordinates[0]), int(coordinates[1])]
    input_is_valid = check_user_input(coordinates)
    if input_is_valid:
        grid[coordinates[0] - 1][coordinates[1] - 1] = current_player
        print_grid()
        empty_cells -= 1
        analyze_game_state()
        if current_player == "X":
            current_player == "O"
        else:
            current_player == "X"
