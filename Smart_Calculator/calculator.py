import re
import stack
from calculatorErrors import *


class Calculator:
    """A simple calculator."""
    def __init__(self):
        self.stored_variables = {}
        self.supported_operators = "+-*/^()"
        self.op_priority = {"+": 1,
                            "-": 1,
                            "*": 2,
                            "/": 2,
                            "^": 3,
                            "(": -1000,
                            ")": -1000}

    def __str__(self):
        msg = ("This is a simple calculator. Supported operations:\n",
               "Addition | a + b | 1 + 3 = 3\n",
               "Subtraction | a - b | 5 - 4 = 1\n",
               "Multiplication | a * b | 3 * 4 = 12\n",
               "Division | a / b | 20 / 4 = 5\n",
               "Power | a ^ b | 2 ^ 3 = 8\n",
               "Brackets | a * (b + c) | 2 * (3 + 4) = 14\n")
        return msg

    @staticmethod
    def execute_command(user_input: str) -> None:
        """Execute the input command."""
        if user_input == "/exit":
            print("Bye!")
            exit()
        elif user_input == "/help":
            print("This is a simple calculator. Supported operations:\n",
                  "Addition | a + b | 1 + 3 = 3\n",
                  "Subtraction | a - b | 5 - 4 = 1\n",
                  "Multiplication | a * b | 3 * 4 = 12\n",
                  "Division | a / b | 20 / 4 = 5\n",
                  "Power | a ^ b | 2 ^ 3 = 8\n",
                  "Brackets | a * (b + c) | 2 * (3 + 4) = 14\n")
        else:
            print("Unknown command")

    @staticmethod
    def evaluate_postfix(expr: list) -> int:
        """Return the result of a given list representing an expression in postfix notation."""
        _stack = stack.Stack()
        for element in expr:
            if isinstance(element, int):
                _stack.append(element)
            elif element == "+":
                b = _stack.pop()
                if _stack:
                    a = _stack.pop()
                else:
                    a = 0
                _stack.append(a + b)
            elif element == "-":
                b = _stack.pop()
                if _stack:
                    a = _stack.pop()
                else:
                    a = 0
                _stack.append(a - b)
            elif element == "*":
                b = _stack.pop()
                a = _stack.pop()
                _stack.append(a * b)
            elif element == "/":
                b = _stack.pop()
                a = _stack.pop()
                r = a / b
                if r.is_integer():
                    _stack.append(int(r))
                else:
                    _stack.append(a / b)
            elif element == "^":
                b = _stack.pop()
                a = _stack.pop()
                _stack.append(pow(a, b))
        return _stack.pop()

    def assign_var(self, user_input: str) -> None:
        """Assign a variable to a number."""
        user_input = [i.strip() for i in user_input.split("=")]
        try:
            self._assign_var(user_input)
        except InvalidAssignmentError as error:
            print(error)
        except InvalidIdentifierError as error:
            print(error)
        except UnknownVariableError as error:
            print(error)

    def _assign_var(self, expr: list) -> None:
        """This function contains the logic to assign a variable to a number and should
        not be called directly. Use assign_var() instead to assign variables."""
        if len(expr) != 2:
            raise InvalidAssignmentError
        elif not re.match(r"^[a-zA-Z]+$", expr[0]):
            raise InvalidIdentifierError
        elif not re.match(r"^-?([a-zA-Z]+|[\d]+\.?[\d]*)$", expr[1]):
            raise InvalidAssignmentError
        elif re.match(r"^-?[a-zA-z]+$", expr[1]):
            if self._is_var(expr[1].strip("-")):
                if re.match(r"^-", expr[1]):
                    self.stored_variables[expr[0]] = self.stored_variables[expr[1].strip("-")] * -1
                else:
                    self.stored_variables[expr[0]] = self.stored_variables[expr[1]]
            else:
                raise UnknownVariableError
        else:
            self.stored_variables[expr[0]] = expr[1]

    def conv_infix_to_postfix(self, user_input: str) -> list:
        """Return a list representing an expression in postfix notation.

            Should not be called directly. Use conv_infix_to_postfix instead to assign variables.
            The function takes in an infix expression and converts it into
            a postfix expression, which is then returned.

            Example:
                Infix notation:
                3 + 2 * 4

                Returned postfix notation:
                3 2 4 * +

            Args:
                user_input: A list representing an expression in infix notation.

            Returns: A list representing an expression in postfix notation.

            """
        try:
            user_input = self._parse_expression(user_input.strip())
            user_input = [i.strip() for i in user_input]
            user_input = self._format_input(user_input)
        except UnknownVariableError as error:
            print(error)
        except InvalidIdentifierError as error:
            print(error)
        except InvalidExpressionError as error:
            print(error)
        else:
            return user_input

    def _parse_expression(self, user_input: str) -> list:
        """Return a list with all the operands and operators of an input string.

        Example: "1 + 2 * ( a - 4)" -> ["1", "+", "2", "*", "(", "a", "-", "4", ")"]

        Args:
            user_input: A string representing a mathematical expression

        Returns: A list representing the input expression split into its
            operands and operators (including brackets).

        """
        expr = [user_input[0]]
        for i in range(1, len(user_input)):
            if user_input[i].isdigit() and user_input[i - 1].isdigit():
                expr[-1] += user_input[i]
            elif user_input[i].isalpha() and user_input[i - 1].isalpha():
                expr[-1] += user_input[i]
            elif user_input[i] in "()":
                expr.append(user_input[i])
            elif user_input[i] in self.supported_operators and user_input[i - 1] in self.supported_operators:
                expr[-1] += user_input[i]
            elif user_input[i] and user_input[i] != "" and user_input[i] != " ":
                expr.append(user_input[i])
        return expr

    def _format_input(self, expr: list) -> list:
        """Return a list representing a formatted expression in postfix notation of a given expression
        in infix notation.

        Args:
            expr: A list representing a mathematical expression in infix notation.

        Returns:
            The formatted postfix expression.
        """
        expr = self._replace_vars(expr)
        expr = self._check_operators(expr)
        if not self._is_valid_expression(expr):
            raise InvalidExpressionError
        for i, value in enumerate(expr):
            if self._is_int(value):
                expr[i] = int(value)

        formatted_expr = self._conv_infix_to_postfix(expr)
        return formatted_expr

    def _replace_vars(self, expr: list) -> list:
        """Return a list representing the given expression after replacing the variables with their
        stored numbers.

        Example: a = 4
        ["2", "+", "a"] -> ["2", "+", "4"]"""
        for i, value in enumerate(expr):
            if self._is_var(value):
                expr[i] = self.stored_variables[value]
            elif self._is_int(value) or value in self.supported_operators:
                pass
            elif re.match(r"([a-zA-Z]+[\d]+|[\d]+[a-zA-Z]+)", value):
                raise InvalidIdentifierError
            elif not value.isalnum():
                raise InvalidExpressionError
            else:
                raise UnknownVariableError
        return expr

    def _check_operators(self, expr: list) -> list:
        """Return a list representing the given expression after formatting operators.
        Multiple "+" turn in to "+", multiple "-" into "-" or "+" accordingly."""
        formatted_expr = []
        for i, value in enumerate(expr):
            if not self._is_int(value) and not re.match(r"^([+]+|[\-]+|[/*^()])$", value):
                raise InvalidExpressionError
            elif re.match(r"^[+]+$", value):
                expr[i] = "+"
            elif re.match(r"^[\-]+$", value):
                if len(value) % 2 == 0:
                    expr[i] = "+"
                else:
                    expr[i] = "-"
        return expr

    def _is_valid_expression(self, expr: list) -> bool:
        """Return True if the given expression is valid, else False."""

        if not self._check_brackets(expr):
            return False

        bracketless_expr = [i for i in expr if i not in "()"]

        if not self._is_int(bracketless_expr[-1]):  # Expression ends on an operator
            return False
        if bracketless_expr[0] in "+-":
            for i in bracketless_expr[1::2]:
                if not self._is_int(i):
                    return False
            if len(bracketless_expr):
                for i in bracketless_expr[::2]:
                    if i not in self.supported_operators:
                        return False
        else:
            for i in bracketless_expr[::2]:
                if not self._is_int(i):
                    return False
            if len(bracketless_expr) > 1:
                for i in bracketless_expr[1::2]:
                    if i not in self.supported_operators:
                        return False
        return True

    @staticmethod
    def _check_brackets(expr: list) -> bool:
        """Returns True if bracket placement in given expression is correct, else False."""
        brackets = 0
        for value in expr:
            if value == "(":
                brackets += 1
            elif value == ")" and brackets <= 0:
                raise InvalidExpressionError
            elif value == ")":
                brackets -= 1

        if brackets:
            raise InvalidExpressionError
        else:
            return True

    def _conv_infix_to_postfix(self, expr: list) -> list:
        """This function contains the logic to convert an expression in infix notation to postfix notation.
        To convert an infix to postfix, use conv_infix_to_postfix()."""
        postfix_expr = []
        _stack = stack.Stack()

        for element in expr:
            if isinstance(element, int):
                postfix_expr.append(element)
            elif element == "(":
                _stack.append(element)
            elif element == ")":
                while not _stack.peek() == "(":
                    postfix_expr.append(_stack.pop())
                _stack.pop()
            elif not _stack.peek() or _stack.peek() == "(":
                _stack.append(element)
            elif self.op_priority[element] > self.op_priority[_stack.peek()]:
                _stack.append(element)
            elif self.op_priority[element] <= self.op_priority[_stack.peek()]:
                while _stack.peek() and self.op_priority[element] <= self.op_priority[_stack.peek()]:
                    postfix_expr.append(_stack.pop())
                _stack.append(element)

        while _stack:
            postfix_expr.append(_stack.pop())

        return postfix_expr

    def _is_var(self, x: str) -> bool:
        """Return True if a given string is an existing variable, else False."""
        return x in self.stored_variables.keys()

    @staticmethod
    def _is_int(x: str) -> bool:
        """Return True if the given string is an Integer, else False."""
        try:
            int(x)
            return True
        except ValueError:
            return False


def is_command(x: str) -> bool:
    """Return True if the given string is a command, else False."""

    return bool(re.match(r"^/", x))


def is_var_assignment(x: str) -> bool:
    """Return True if the given string expression is a variable-assignment, else False."""
    return bool(re.match(r"[\s]*[\w]+[\s]*=", x))


def main():
    calculator = Calculator()
    while True:

        user_input = input()

        # Empty user input
        if not user_input:
            continue

        # Use a command
        if is_command(user_input):
            calculator.execute_command(user_input)
            continue

        # Assign a value to a variable
        if is_var_assignment(user_input):
            calculator.assign_var(user_input)
            continue

        # Convert a mathematical expression to postfix notation, so it can be evaluated
        postfix_expr = calculator.conv_infix_to_postfix(user_input)

        # Evaluate the postfix expression
        if postfix_expr:
            print(calculator.evaluate_postfix(postfix_expr))


if __name__ == "__main__":
    main()
