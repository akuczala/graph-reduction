from __future__ import annotations
from typing import List

from graph import Node

StackValue = Node


class SpineStack:
    def __init__(self):
        self.stack: List[StackValue] = []

    def push(self, value: StackValue) -> SpineStack:
        self.stack.append(value)
        return self

    def pop(self) -> StackValue:
        return self.stack.pop()

    def peek(self) -> StackValue:
        return self.stack[-1]

    def peek_at_last(self, n: int) -> List[StackValue]:
        return self.stack[-n:]

    def __len__(self):
        return len(self.stack)

    def __str__(self):
        return str(self.stack)