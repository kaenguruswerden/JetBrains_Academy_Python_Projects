import socket
import json
import time
import random
import string


def random_password() -> str:
    """ Return a  random password of length from 6 to 10 consisting of letters and digits """
    possible_characters = string.ascii_letters + string.digits
    return ''.join(random.choice(possible_characters) for i in range(random.randint(6, 10)))


def random_login() -> str:
    """ Return a randomly chosen login name from a file """
    with open("logins.txt", "r") as logins_file:
        all_logins = logins_file.readlines()
        return random.choice(all_logins).strip()


HOST = '127.0.0.1'
PORT = 9090
LOGIN = random_login()
PASSWORD = random_password()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()
    with conn:
        while True:
            data = conn.recv(1024)
            if data:
                login_data = json.loads(data.decode())
                result = {"result": ""}
                login = login_data["login"]
                password = login_data["password"]
                if login != LOGIN:
                    result["result"] = "Wrong login!"
                    conn.send(json.dumps(result).encode())
                else:
                    if password == "":
                        result["result"] = "Wrong password!"
                        conn.send(json.dumps(result).encode())
                    elif password != PASSWORD and PASSWORD.startswith(password):
                        result["result"] = "Wrong password!"
                        time.sleep(0.1)
                        conn.send(json.dumps(result).encode())
                    elif password == PASSWORD:
                        print(password)
                        result["result"] = "Connection success!"
                        conn.send(json.dumps(result).encode())
                    else:
                        result["result"] = "Wrong password!"
                        conn.send(json.dumps(result).encode())
            elif not data:
                break
