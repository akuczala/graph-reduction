from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatchmethod
from typing import Union, Type

from adt import adt, Case


@dataclass
class Constant:
    value: float

    def __str__(self) -> str:
        return str(self.value)


class Combinator(ABC):

    @property
    def n_args(cls):
        pass

    def count_args_and_eval(self, stack):
        if len(stack) < self.n_args + 1:
            print(f"{self.to_string()} only provided {len(stack) - 1} arguments.")
            stack.clear()
            return
        else:
            self.eval(stack)

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
        if isinstance(in_slot, cls):
            return in_slot
        else:
            raise NotImplementedError(f"{type(in_slot)} is not a valid graph element value.")

    # @new.register
    # @classmethod
    # def _(cls, in_slot: GraphElement):
    #     return in_slot

    @new.register
    @classmethod
    def _(cls, in_slot: Combinator):
        return cls(in_slot)

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

    def __str__(self) -> str:
        return str(self.value)
