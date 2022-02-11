class CalculatorError(Exception):
    def __str__(self):
        return "Calculator Error"


class UnknownVariableError(CalculatorError):
    def __str__(self):
        return "Unknown Variable"


class InvalidExpressionError(CalculatorError):
    def __str__(self):
        return "Invalid expression"


class InvalidAssignmentError(CalculatorError):
    def __str__(self):
        return "Invalid assignment"


class InvalidIdentifierError(CalculatorError):
    def __str__(self):
        return "Invalid identifier"
