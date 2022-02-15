print('What\'s your name?') # reading an input
name = input();
print(f'Hello, {name}');  # here is an obvious comment: this prints a greeting with a name


very_big_number = 11_000_000_000_000_000_000_000_000_000_000_000_000_000_000_000
print(very_big_number)



def some_fun():
    print('NO TODO HERE;;')
    pass; # Todo something


class  Person:
    pass

class user:

    def __init__(self, login: str, password: str):
        self.login = login
        self.password = password

    def fun1(S=5, test=[], d={}, s=()):  # default argument value is mutable
        VARIABLE = 10
        string = 'string'
        print(VARIABLE)

    @staticmethod
    def _print1():
        print('q')

    @staticmethod
    def Print2():
        print('q')

    def __bad_Name__(self):
        pass


CONSTANT = 10
names = ['John', 'Lora', 'Paul']


def fun1(S=5, test=[], d={}, s=()):  # default argument value is mutable
    VARIABLE = 10
    string = 'string'
    print(VARIABLE)