from typing import TypeVar, Generic

T = TypeVar('T')


class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f"Box({self.value})"