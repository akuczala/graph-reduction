from __future__ import annotations
from typing import List, TypeVar, Generic

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self, verbose=False):
        self.stack: List[T] = []
        self.verbose = verbose

    def push(self, value: T) -> Stack[T]:
        self.stack.append(value)
        return self

    def pop(self) -> T:
        return self.stack.pop()

    def peek(self) -> T:
        return self.stack[-1]

    def peek_at_last(self, n: int) -> List[T]:
        return self.stack[-n:]

    def clear(self):
        self.stack = []

    def __len__(self):
        return len(self.stack)

    def __str__(self):
        return str([str(s) for s in self.stack])
