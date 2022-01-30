import random
from nltk.tokenize import regexp_tokenize


class Trigram:
    """
    A class representing a trigram.
    """

    def __init__(self, head: str, tail: str):
        self.head = head
        self.tail = tail

    def __repr__(self):
        return f"Trigram(head={self.head}, tail={self.tail}"

    def __str__(self):
        return f"Head: {self.head} Tail: {self.tail}"


class MarkovChain:
    """
    A class representing a Markov chain.

    A Markov chain is a statistical model in which the probability of each event depends on the previous event.
    It can be described as a set of states and transitions between them. Each transition has a probability that is
    determined by some kind of statistical data. In this project, a state corresponds to a token, and each transition
    represents going from one word of a sentence to another. The probability of transitions is calculated from the
    trigrams collected. The basic idea of this project is that from a dictionary we can create a model that will
    consider all the possible transitions from one word to another and choose the most probable one based on the
    previous word. - (https://hyperskill.org/projects/134/stages/716/implement)
    """

    def __init__(self, path: str):
        self.path = path
        self.tokens = self.generate_tokens()
        self.trigrams = self.break_into_trigrams()
        self.chain = self.create_markov_chain()

    def generate_tokens(self) -> list:
        """
        Return the tokens of a text corpus taken from a text file.

        :return: A list with the tokens separated by whitespace characters such as space, tab, newline characters
        """
        with open(self.path, "r", encoding="UTF-(") as corpus_file:
            text = corpus_file.read()
            corpus_tokens = regexp_tokenize(text, r"[^\s]+")
            corpus_file.close()
            return corpus_tokens

    def break_into_trigrams(self) -> list:
        """
        Return a list of trigrams generated from a list of tokens.

        :return: A list of generated trigrams
        """
        tokens = self.tokens
        trigrams = []
        for i, token in enumerate(tokens):
            if i < len(tokens) - 2:
                trigrams.append(Trigram(f"{token} {tokens[i + 1]}", tokens[i + 2]))
        return trigrams

    def create_markov_chain(self) -> dict[str, dict]:
        """
        Return a generated chain model with the Markov Model

        :return: A dictionary which contains dictionaries for each key following, the rules of the Markov Model.
        """
        trigrams = self.trigrams
        markov_chain = {}
        for trigram in trigrams:
            markov_chain.setdefault(trigram.head, {})
            markov_chain[trigram.head].setdefault(trigram.tail, 0)
            markov_chain[trigram.head][trigram.tail] += 1
        return markov_chain

    def generate_sentence(self, start: str, min_length: int) -> str:
        """
        Generate and print a sentence with at least min_length words from a chain with a specified start token.

        :param start: The first token of the sentence
        :param min_length: The minimal number of words in a sentence
        :return A string with the sentence. A sentence always ends with a sentence-ending punctuation mark (., !, ?).
        """
        sentence = start.split()
        while len(sentence) < min_length or sentence[-1][-1] not in [".", "!", "?"]:
            sentence.append(self.find_next_word(sentence[-2] + " " + sentence[-1]))
        return " ".join(sentence)

    def find_first_words(self) -> str:
        """
        Return the first (two) random words of a sentence.

        :return: A string with the first (two) words for a sentence. The first word can not end with a sentence-ending \
                 punctuation mark (., !, ?).
        """
        first_words = random.choice(list(self.chain.keys()))
        first_word, second_word = [word.strip("[\"']") for word in first_words.split()]
        if first_words[0].isupper() and first_word[-1] not in [".", "!", "?"]:
            return f"{first_word} {second_word}"
        else:
            return self.find_first_words()

    def find_next_word(self, words: str) -> str:
        """
        Return the next words following the rules of the Markov Model.

        :param words: A String with the previous (two) words of the sentence
        :return: A String with the next word of the sentence.
        """
        next_words = list(self.chain[words].keys())
        counts = list(self.chain[words].values())
        next_word = random.choices(next_words, counts)
        return str(next_word).strip("[\"']")


def main():
    random.seed()
    # Let the user input the path to the file
    path = input()
    # Because I'm too lazy to type the path everytime I test the program
    if path == "":
        path = "corpus.txt"

    chain = MarkovChain(path)

    # Generate and print n sentences
    for _ in range(10):
        first_word = chain.find_first_words()
        sentence = chain.generate_sentence(first_word, 5)
        print(sentence)


if __name__ == "__main__":
    main()
