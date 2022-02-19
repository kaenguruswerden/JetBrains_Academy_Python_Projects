import os
import random
import argparse
import flashcard_logger as logger


class FlashCard:
    """A class for a simple flashcard with a term and a definition, and a counter for wrong answers."""
    def __init__(self, term, definition, previous_errors=0):
        self.term = term
        self.definition = definition
        self.error_count = int(previous_errors)

    def ask_definition(self, collection: dict = None) -> None:
        """Ask the user for the definition of the card's term and check if the answer is correct.

        If a collection is passed, check if the definition belongs to another term in case of a wrong answer.

        :param collection: (optional) A dictionary with a collection of flashcards in this format:
            {definition1: term1, definition2: term2, ...}
        """
        answer = logger.get_input_and_log(f"Print the definition of \"{self.term}\":")
        if answer == self.definition:
            logger.log_and_print("Correct!")
        elif collection:
            if answer in collection.keys():
                self.error_count += 1
                logger.log_and_print(f"Wrong. The right answer is \"{self.definition}\", "
                                     f"but your definition is correct for \"{collection[answer]}\".")
            else:
                self.error_count += 1
                logger.log_and_print(f"Wrong. The right answer is \"{self.definition}\".")
        else:
            self.error_count += 1
            logger.log_and_print(f"Wrong. The right answer is \"{self.definition}\".")
    
    def reset_errors(self) -> None:
        """Reset error count."""
        self.error_count = 0


class FlashCardCollection:
    """A class for a collection of flashcards.
    
    Supported actions: 
    - adding and removing cards
    - importing and exporting collections of cards
    - asking the user for definitions of a term of a random flashcard from the collection"
    - showing the card with the highest number of errors
    - resetting all cards error count"""

    def __init__(self):
        self.collection = {}
        self.terms_and_defs = {}

    def add_flashcard(self) -> None:
        """Ask the user for a term and a definition and create a new flashcard of it. Flashcards can NOT have the
        same term or definition."""
        term = logger.get_input_and_log("The card:")
        while True:
            if term in self.collection.keys():
                term = logger.get_input_and_log(f"The card \"{term}\" already exists. Try again:")
            else:
                break
        definition = logger.get_input_and_log("The definition of the card:")
        while True:
            if definition in self.terms_and_defs.keys():
                definition = logger.get_input_and_log(f"The definition \"{definition}\" already exists. Try again:")
            else:
                break
        self.collection[term] = FlashCard(term, definition)
        self.terms_and_defs[definition] = term
        logger.log_and_print(f"The pair (\"{term}\":\"{definition}\") has been added.")

    def remove_flashcard(self) -> None:
        """Remove a flashcard from the collection."""
        card = logger.get_input_and_log("Which card?")
        if card in self.collection.keys():
            definition = self.collection[card].definition
            del self.terms_and_defs[definition]
            del self.collection[card]
            logger.log_and_print("The card has been removed.")
        else:
            logger.log_and_print(f"Can't remove \"{card}\": there is no such card.")

    def import_flashcards(self, path: str = None) -> None:
        """
        Import all the cards from a file to the collection. The file name can either be passed in the function or
        through user input. If a card with the same name (term) already exists in the collection, it gets replaced.

        :param path: (optional) Name of a file.
        """
        if not path:
            path = logger.get_input_and_log("File name:")
        cwd = os.path.dirname(__file__)
        filename = os.path.join(cwd, path)  # doesn't work for the hyperskill tests...
        if not os.path.exists(path):
            logger.log_and_print("File not found.")
        else:
            with open(path, "r") as file:
                line_count = 0
                for line in file:
                    line_count += 1
                    term, definition, error_count = line.strip("\n").split("; ")
                    if term in self.collection.keys():
                        old_def = self.collection[term].definition
                        del self.terms_and_defs[old_def]
                    self.collection[term] = FlashCard(term, definition, error_count)
                    self.terms_and_defs[definition] = term
            logger.log_and_print(f"{line_count} cards have been loaded.")

    def export_flashcards(self, path: str = None) -> None:
        """
        Export all the cards in the collection to a file.
        The file name can either be passed in the function or through user input.

        :param path: (optional) Name of a file.
        """
        if not path:
            path = logger.get_input_and_log("File name:")
        cwd = os.path.dirname(__file__)
        filename = os.path.join(cwd, path)  # doesn't work for the hyperskill tests...
        with open(path, "w") as file:
            for card in self.collection:
                line = f"{card}; {self.collection[card].definition}; {self.collection[card].error_count}\n"
                file.write(line)
        logger.log_and_print(f"{len(self.terms_and_defs)} cards have been saved.")

    def ask_definitions(self) -> None:
        """Ask the user for a definition to a term and checks if it is correct. Repeat n times; n input by user."""
        n = int(logger.get_input_and_log("How many times to ask?"))
        for _ in range(n):
            card = random.choice(list(self.collection.keys()))
            self.collection[card].ask_definition(self.terms_and_defs)

    def hardest_card(self) -> None:
        """Print the card(s) that got answered wrong the most times their number of errors."""
        hardest_cards = []
        max_error_count = 0
        for card in self.collection:
            if self.collection[card].error_count > max_error_count:
                max_error_count = self.collection[card].error_count
                hardest_cards = [card]
            elif self.collection[card].error_count == max_error_count and max_error_count > 0:
                hardest_cards.append(card)
        if max_error_count == 0:
            logger.log_and_print("There are no cards with errors.")
        elif len(hardest_cards) == 1:
            logger.log_and_print(f"The hardest card is \"{hardest_cards[0]}\". "
                                 f"You have {max_error_count} errors answering it.")
        elif len(hardest_cards) > 1:
            hardest_cards = [f"\"{card}\"" for card in hardest_cards]
            card_names = ", ".join(hardest_cards)
            logger.log_and_print(f"The hardest cards are {card_names}. "
                                 f"You have {max_error_count} errors answering them.")
    
    def reset_stats(self) -> None:
        """Reset the error count of all card in collection to 0."""
        for card in self.collection:
            self.collection[card].reset_errors()
        logger.log_and_print("Card statistics have been reset.")


def input_loop(flashcard_collection: FlashCardCollection, export_file_name: str = None) -> None:
    """
    Main loop for the flashcard program.

    :param flashcard_collection: A collection of flashcards to work with.
    :param export_file_name: (optional) Name of a file to automatically export the collection to before
        exiting the program.
    """
    while True:
        user_input = logger.get_input_and_log(("Input the action (add, remove, import, export, ask, exit, "
                                               "log, hardest card, reset stats):"))
        if user_input == "add":
            flashcard_collection.add_flashcard()
        elif user_input == "remove":
            flashcard_collection.remove_flashcard()
        elif user_input == "import":
            flashcard_collection.import_flashcards()
        elif user_input == "export":
            flashcard_collection.export_flashcards()
        elif user_input == "ask":
            flashcard_collection.ask_definitions()
        elif user_input == "log":
            log()
        elif user_input == "hardest card":
            flashcard_collection.hardest_card()
        elif user_input == "reset stats":
            flashcard_collection.reset_stats()
        elif user_input == "exit":
            logger.log_and_print("Bye bye!")
            if export_file_name:
                flashcard_collection.export_flashcards(export_file_name)
            exit()
        else:
            logger.log_and_print("This is not known command!")
        logger.log_and_print("")


def log() -> None:
    """Save the log to a file specified by user input."""
    file_name = logger.get_input_and_log("File name:")
    logger.save_log_to_file(file_name)
    logger.log_and_print("The log has been saved.")


def parse_arguments() -> argparse.Namespace:
    """Return parsed arguments."""
    parser = argparse.ArgumentParser(description="This program uses the flashcard principal to test your knowledge. "
                                                 "It also support adding and removing flashcards, "
                                                 "importing and exporting sets of flashcards, "
                                                 "as well as error tracking.")
    parser.add_argument("-i", "--import_from", help="name of a file with saved flashcards to import flashcards from "
                                                    "automatically at the beginning")
    parser.add_argument("-e", "--export_to", help="name of a file to export the flashcards to automatically "
                                                  "before exiting the program")
    return parser.parse_args()


def main():
    flashcard_collection = FlashCardCollection()
    args = parse_arguments()
    if args.import_from:
        flashcard_collection.import_flashcards(args.import_from)
    if args.export_to:
        export_file_name = args.export_to
    else:
        export_file_name = None
    input_loop(flashcard_collection, export_file_name)


if __name__ == "__main__":
    main()
