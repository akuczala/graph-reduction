from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Callable, Union, Type


class GraphElementValue(ABC):
    @abstractmethod
    def eval_and_update_stack(self, stack):
        pass


@dataclass(frozen=True)
class Constant(GraphElementValue):
    value: float

    def __str__(self) -> str:
        return str(self.value)

    def eval_and_update_stack(self, stack):
        if stack.verbose:
            print(f"encountered constant {self.value}. Should be done.")
        stack.pop()


class Combinator(GraphElementValue):

    @property
    @abstractmethod
    def n_args(self) -> int:
        pass

    def eval_and_update_stack(self, stack):
        if len(stack) < self.n_args + 1:
            if stack.verbose:
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


@dataclass(frozen=True)
class Node(GraphElementValue):
    function_slot: GraphElement
    argument_slot: GraphElement

    @classmethod
    def new(cls, in_function_slot, in_argument_slot) -> Node:
        return cls(
            function_slot=GraphElement.new(in_function_slot),
            argument_slot=GraphElement.new(in_argument_slot)
        )

    def eval_and_update_stack(self, stack):
        stack.push(self.function_slot)

    def __str__(self) -> str:
        return f"[{self.function_slot} | {self.argument_slot}]"


T = TypeVar('T')


@dataclass
class GraphElement:
    value: GraphElementValue

    @classmethod
    def new(cls, in_slot: Union[GraphElement, GraphElementValue, Type[Combinator], float, int]) -> GraphElement:
        """
        Convenience function. singledispatchmethod doesn't quite cut it, so here we are
        """
        match in_slot:
            case s if isinstance(s, cls):
                return in_slot
            case s if isinstance(s, GraphElementValue):
                return cls(s)
            case s if isinstance(s, type(Combinator)):
                return cls(in_slot())
            case s if isinstance(s, float):
                return cls(Constant(s))
            case s if isinstance(s, int):
                return cls(Constant(float(s)))
            case _:
                raise NotImplementedError(f"Cannot instantiate GraphElement with {in_slot} of type {type(in_slot)}.")

    @classmethod
    def new_node(cls, function_slot: GraphElement, argument_slot: GraphElement) -> GraphElement:
        return cls.new(Node.new(function_slot, argument_slot))

    def eval_and_update_stack(self, stack):
        self.value.eval_and_update_stack(stack)

    def match_value(self, on_node: Callable[[Node], T], on_combinator: Callable[[Combinator], T],
                    on_constant: Callable[[Constant], T]) -> T:
        match self.value:
            case Node() as n:
                return on_node(n)
            case Combinator() as c:
                return on_combinator(c)
            case Constant() as c:
                return on_constant(c)
            case _:
                raise ValueError(f"{self.value} of type {type(self.value)} is not a valid graph element value")

    def equals_literal(self, other: GraphElement) -> bool:
        if not isinstance(self.value, type(other.value)):
            return False
        return self.match_value(
            on_node=lambda n: (
                    n.function_slot.equals_literal(other.value.function_slot) and
                    n.argument_slot.equals_literal(other.value.argument_slot)
            ),
            on_combinator=lambda c: type(c) == type(other.value),
            on_constant=lambda c: c.value == other.value.value
        )

    def __str__(self) -> str:
        return str(self.value)
