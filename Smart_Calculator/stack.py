from collections import deque


class Stack(deque):
    """A class for a stack."""
    def __init__(self):
        super().__init__()

    def peek(self):
        """Return the element, that currently is on top of the stack without removing it."""
        if self:
            return self[-1]
        else:
            return None
