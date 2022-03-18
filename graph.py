from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import singledispatchmethod

from adt import adt, Case


@dataclass
class Constant:
    value: float

    def __str__(self) -> str:
        return str(self.value)

    # def __repr__(self) -> str:
    #     return str(self)


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

    # def __repr__(self) -> str:
    #     return self.to_string()


@adt
class FunctionSlot:
    COMBINATOR: Case[Combinator]
    SUBTREE: Case[Node]

    # @singledispatchmethod
    # @staticmethod
    # def new(in_slot):
    #     raise NotImplementedError(f"Cannot place {type(in_slot)} into function slot.")
    #
    # @new.register
    # def _(in_slot: Combinator):
    #     return FunctionSlot.COMBINATOR(in_slot)
    #
    # @new.register
    # def _(in_slot: Node):
    #     return FunctionSlot.SUBTREE(in_slot)

    def __str__(self) -> str:
        return self.match(
            combinator=lambda c: c.to_string(),
            subtree=lambda t: str(t)
        )

    # def __repr__(self) -> str:
    #     return str(self)


@adt
class ArgumentSlot:
    COMBINATOR: Case[Combinator]
    SUBTREE: Case[Node]
    CONSTANT: Case[Constant]

    # @singledispatchmethod
    # @staticmethod
    # def new(in_slot) -> ArgumentSlot:
    #     raise NotImplementedError(f"Cannot place {type(in_slot)} into argument slot.")
    #
    # @new.register
    # def _(in_slot: Combinator) -> ArgumentSlot:
    #     return ArgumentSlot.COMBINATOR(in_slot)
    #
    # @new.register
    # def _(in_slot: Node) -> ArgumentSlot:
    #     return ArgumentSlot.SUBTREE(in_slot)
    #
    # @new.register
    # def _(in_slot: Constant) -> ArgumentSlot:
    #     return ArgumentSlot.CONSTANT(in_slot)
    #
    # @new.register
    # def _(in_slot: float) -> ArgumentSlot:
    #     return ArgumentSlot.CONSTANT(Constant(in_slot))

    def __str__(self) -> str:
        return self.match(
            combinator=lambda c: c.to_string(),
            subtree=lambda t: str(t),
            constant=lambda c: str(c)
        )

    # def __repr__(self) -> str:
    #     return str(self)


@dataclass
class Node:
    function_slot: FunctionSlot
    argument_slot: ArgumentSlot

    def new(self, in_function_slot, in_argument_slot) -> Node:
        return Node(
            function_slot=FunctionSlot.new(in_function_slot),
            argument_slot=ArgumentSlot.new(in_argument_slot)
        )

    def __str__(self) -> str:
        return f"[{self.function_slot} | {self.argument_slot}]"

    # def __repr__(self) -> str:
    #     return str(self)