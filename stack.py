from __future__ import annotations
from typing import List

from graph import GraphElement

StackValue = GraphElement


class SpineStack:
    def __init__(self, verbose=False):
        self.stack: List[StackValue] = []
        self.verbose = verbose

    def push(self, value: StackValue) -> SpineStack:
        self.stack.append(value)
        return self

    def pop(self) -> StackValue:
        return self.stack.pop()

    def peek(self) -> StackValue:
        return self.stack[-1]

    def peek_at_last(self, n: int) -> List[StackValue]:
        return self.stack[-n:]

    def clear(self):
        self.stack =[]

    def __len__(self):
        return len(self.stack)

    def __str__(self):
        return str([str(s) for s in self.stack])
