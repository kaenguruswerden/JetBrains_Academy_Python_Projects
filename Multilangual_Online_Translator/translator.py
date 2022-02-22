import requests
import os
import argparse
from bs4 import BeautifulSoup

# The available languages
LANGUAGES = ["Arabic", "German", "English", "Spanish", "French", "Hebrew",
             "Japanese", "Dutch", "Polish", "Portuguese", "Romanian", "Russian", "Turkish"]


def send_request(url: str, word: str) -> requests.models.Response:
    """Send a get request to the website with passed URL and return the response if the connection was successful.
    Print an error and exit the program if something goes wrong.

    :param url: The URL to the site with the translation for a word.
    :param word: The word to translate.
    :return: The HTML content of the page.
    """
    # print(url)
    headers = {'User-Agent': 'Mozilla/5.0'}
    page = requests.get(url, headers=headers)
    if page:
        return page
    if page.status_code == 404:
        print(f"Sorry, unable to find {word}")
        exit()
    else:
        # print(page.status_code, "Connection failed!")
        print("Something wrong with your internet connection")
        exit()


def get_translations(page_content: BeautifulSoup) -> list:
    """Return a list with all the translations of a word.

    :param page_content: The parsed content of an HTML page.
    :return: A list with all the translations of the word.
    """
    translations = page_content.find("div", {"id": "translations-content"}).find_all("a")
    translations_list = []
    for tr in translations:
        translations_list.append(tr.text.strip())
    return translations_list


def get_examples(page_content: BeautifulSoup) -> list:
    """Return a list with all the example sentences.

    :param page_content: The parsed content of an HTML page.
    :return: A list with all the example sentences, alternating between the original and the translated version.
    """
    sentences = page_content.find("section", {"id": "examples-content"}).find_all("span", {"class": "text"})
    sentences_list = []
    for s in sentences:
        sentences_list.append(s.text.strip())
    return sentences_list


def print_translations_and_save_to_file(language_to: str, word: str, *translations, sep="") -> None:
    """Print and save the translations of a word to a text file with the word's name.

    :param language_to: The language to translate to.
    :param word: The word to translate.
    :param translations: A list with all the translations for the word.
    :param sep: (Optional) The seperator between the words in the output.
    """
    with open(f"{word}.txt", "a", encoding="UTF-8") as file:
        print(f"\n{language_to} Translations:", sep=sep, file=file)
        print(*translations, sep=sep, file=file)


def print_examples_and_save_to_file(language_to: str, word: str, *sentences: list[str], sep="") -> None:
    """Print and save the example sentences to a text file with the word's name.

    :param language_to: The language to translate to.
    :param word: The word to translate.
    :param sentences: A list with all the example sentences, alternating between the language to translate from
        and the language to translate to.
    :param sep: (Optional) The seperator between the sentences in the output.
    """
    with open(f"{word}.txt", "a", encoding="UTF-8") as file:
        print(f"\n{language_to} Examples:", sep=sep, file=file)
        for i, sentence in enumerate(sentences, start=1):
            print(sentence, end=sep, file=file)
            if i % 2 == 0:
                print(file=file)


def translate(language_from: str, language_to: str, word: str, n: int = 5) -> None:
    """Translate the passed word into chosen language, print the result and save it to a file.

    :param language_from: The language to translate from.
    :param language_to: The language to translate to.
    :param word: the word to translate.
    :param n: the max number of results in the output.
    """
    url = f"https://context.reverso.net/translation/{language_from.lower()}-{language_to.lower()}/{word}"

    page = send_request(url, word)
    page_content = BeautifulSoup(page.content, "html.parser")

    translations = get_translations(page_content)
    sentences = get_examples(page_content)

    print_translations_and_save_to_file(language_to, word, *translations[0:n], sep="\n")
    print_examples_and_save_to_file(language_to, word, *sentences[0:n*2], sep="\n")


def parse_arguments() -> argparse.Namespace:
    """Return parsed arguments."""
    parser = argparse.ArgumentParser(description="This program translates a word from one language into one or all"
                                                 "available languages and gives an example on how to use the word"
                                                 "in each language.")
    parser.add_argument("language_from", help="the language you want to translate from")
    parser.add_argument("language_to", help="the language you want to translate to (or all available languages)")
    parser.add_argument("word", help="the word you want to get translated")
    return parser.parse_args()


def main():
    n = 1  # max number of translations per language
    args = parse_arguments()
    language_from, language_to, word = args.language_from.title(), args.language_to.title(), args.word

    for language in [language_to, language_from]:
        if language not in LANGUAGES and language != "All":
            print(f"Sorry, the program doesn't support {language.lower()}")
            break
    else:
        # If a file with the name already exists, delete it's content.
        if os.path.exists(f"{word}.txt"):
            with open(f"{word}.txt", "w") as file:
                file.close()

        if language_to == "All":
            for language in LANGUAGES:
                if language != language_from:
                    translate(language_from, language, word, n)
        else:
            translate(language_from, language_to, word, n)

        # Strip the newlines at the beginning and end of file. Probably not the most elegant way of doing it...
        with open(f"{word}.txt", "r", encoding="UTF-8") as file:
            file_content = "".join(file.readlines()).strip("\n")

        with open(f"{word}.txt", "w+", encoding="UTF-8") as file:
            file.writelines(file_content)
            file.seek(0)
            print(file.read())


if __name__ == "__main__":
    main()
