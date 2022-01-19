import random


words = ['python', 'java', 'kotlin', 'javascript']
attempts = 8


def menu() -> None:
    action = ""
    while action != "play" and action != "exit":
        action = input('Type "play" to play the game, "exit" to quit:')
    if action == "play":
        play()
    else:
        exit()


def play() -> None:

    global attempts
    win = False
    solution = random.choice(words)
    solution_set = set(solution)
    hint = "-" * len(solution)
    guessed_letters = set()

    while attempts > 0 and not win:
        print("\n" + hint)
        guess = input("Input a letter: ")
        if len(guess) != 1:
            print("You should input a single letter")
        elif not guess.isalpha() or not guess.islower():
            print("Please enter a lowercase English letter")
        elif guess in guessed_letters:
            print("You've already guessed this letter")
        elif guess in solution_set:
            new_hint = ""
            for i in range(len(solution)):
                if solution[i] == guess:
                    new_hint += guess
                else:
                    new_hint += hint[i]
            hint = new_hint
            if hint == solution:
                win = True
                print(solution)
        else:
            print("That letter doesn't appear in the word")
            attempts -= 1
        guessed_letters.add(guess)

    if win:
        print("You guessed the word!\nYou survived!")
    else:
        print("You lost!")
    menu()


print("H A N G M A N")
menu()
