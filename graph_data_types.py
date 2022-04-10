from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic

from stack import Stack

S = TypeVar('S', bound="EqualsLiteralMixin")


class EqualsLiteralMixin(ABC):
    @abstractmethod
    def equals_literal(self, other) -> bool:
        pass


class GraphElementValue(EqualsLiteralMixin):
    pass


ConstantType = float


@dataclass(frozen=True)
class Constant(GraphElementValue):
    value: ConstantType

    def __str__(self) -> str:
        return str(self.value)

    def equals_literal(self, other) -> bool:
        return self == other


class Combinator(GraphElementValue):

    @property
    @abstractmethod
    def n_args(self) -> int:
        pass

    def equals_literal(self, other) -> bool:
        return self == other

    @abstractmethod
    def eval(self, stack: Stack):
        pass

    @classmethod
    def to_string(cls) -> str:
        return cls.__name__

    def __str__(self) -> str:
        return self.to_string()

    def __eq__(self, other):
        return isinstance(other, Combinator) and type(self) == type(other)


@dataclass(frozen=True)
class Node(Generic[S], GraphElementValue):
    function_slot: S
    argument_slot: S

    def equals_literal(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        return (
                self.function_slot.equals_literal(other.function_slot) and
                self.argument_slot.equals_literal(other.argument_slot)
        )

    def __str__(self) -> str:
        return f"[{self.function_slot} | {self.argument_slot}]"
