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
    pass

    @classmethod
    @abstractmethod
    def eval(cls, stack):
        pass

    @classmethod
    @abstractmethod
    def to_string(cls) -> str:
        pass

    def __str__(self) -> str:
        return self.to_string()


@dataclass
class Node:
    function_slot: FunctionSlot
    argument_slot: ArgumentSlot

    @classmethod
    def new(cls, in_function_slot, in_argument_slot) -> Node:
        return cls(
            function_slot=FunctionSlot.new(in_function_slot),
            argument_slot=ArgumentSlot.new(in_argument_slot)
        )

    def __str__(self) -> str:
        return f"[{self.function_slot} | {self.argument_slot}]"


@dataclass
class FunctionSlot:
    slot: Union[Combinator, Node]

    @classmethod
    def new(cls, in_slot):
        return FunctionSlot(in_slot)

    def __str__(self) -> str:
        return str(self.slot)


@dataclass
class ArgumentSlot:
    slot: Union[Combinator, Node, Constant]

    @singledispatchmethod
    @classmethod
    def new(cls, in_slot):
        raise NotImplementedError(f"Cannot place {type(in_slot)} into argument slot.")

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
        return cls.new(Constant(in_slot))

    @new.register
    @classmethod
    def _(cls, in_slot: int):
        return cls.new(float(in_slot))

    def __str__(self) -> str:
        return str(self.slot)
