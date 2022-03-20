from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatchmethod
from typing import Union


@dataclass
class Constant:
    value: float

    def __str__(self) -> str:
        return str(self.value)


class Combinator(ABC):

    @property
    def n_args(cls) -> int:
        pass

    def eval_and_update_stack(self, stack, verbose=False):
        if len(stack) < self.n_args + 1:
            if verbose:
                print(f"{self.to_string()} only provided {len(stack) - 1} arguments.")
            stack.clear()
            return
        else:
            self.eval(stack)
            for _ in range(self.n_args):
                stack.pop()

    @abstractmethod
    def eval(self, stack):
        pass

    @classmethod
    @abstractmethod
    def to_string(cls) -> str:
        pass

    def __str__(self) -> str:
        return self.to_string()


@dataclass
class Node:
    function_slot: GraphElement
    argument_slot: GraphElement

    @classmethod
    def new(cls, in_function_slot, in_argument_slot) -> Node:
        return cls(
            function_slot=GraphElement.new(in_function_slot),
            argument_slot=GraphElement.new(in_argument_slot)
        )

    def __str__(self) -> str:
        return f"[{self.function_slot} | {self.argument_slot}]"


@dataclass
class GraphElement:
    value: Union[Combinator, Node, Constant]

    @singledispatchmethod
    @classmethod
    def new(cls, in_slot):
        # singledispatchmethod doesn't seem to support matching on own type
        if isinstance(in_slot, cls):
            return in_slot
        else:
            raise NotImplementedError(f"{in_slot} of type {type(in_slot)} is not a valid graph element value.")

    @new.register
    @classmethod
    def _(cls, in_slot: Combinator):
        return cls(in_slot)

    @new.register
    @classmethod
    def _(cls, in_slot: type(Combinator)):
        return cls(in_slot())

    @new.register
    @classmethod
    def _(cls, in_slot: Node):
        return cls(in_slot)

    @new.register
    @classmethod
    def _(cls, in_slot: Constant):
        return cls(in_slot)

    @new.register
    @classmethod
    def _(cls, in_slot: float):
        return cls(Constant(in_slot))

    @new.register
    @classmethod
    def _(cls, in_slot: int):
        return cls.new(float(in_slot))

    @classmethod
    def new_node(cls, function_slot, argument_slot):
        return cls.new(Node.new(function_slot, argument_slot))

    def equals_literal(self, other: GraphElement) -> bool:
        if not isinstance(self.value, type(other.value)):
            return False
        match self.value:
            case Node():
                return (
                        self.value.function_slot.equals_literal(other.value.function_slot) and
                        self.value.argument_slot.equals_literal(other.value.argument_slot)
                )
            case Combinator():
                return type(self.value) == type(other.value)
            case Constant():
                return self.value.value == other.value.value

    def __str__(self) -> str:
        return str(self.value)
