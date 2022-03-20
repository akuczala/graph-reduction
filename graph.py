from __future__ import annotations
from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Callable, Union, Type, Dict, cast

from adt import ADT, ValueType

V = TypeVar('V', bound="GraphElementValue")


class GraphElementValue(ValueType):
    @abstractmethod
    def eval_and_update_stack(self, stack):
        pass

    @abstractmethod
    def equals_literal(self: V, other: V) -> bool:
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

    def equals_literal(self, other: Constant) -> bool:
        return self.value == other.value


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

    def equals_literal(self, other: Combinator) -> bool:
        return type(self) == type(other)

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

    def equals_literal(self, other: Node) -> bool:
        return (
                self.function_slot.equals_literal(other.function_slot) and
                self.argument_slot.equals_literal(other.argument_slot)
        )

    def __str__(self) -> str:
        return f"[{self.function_slot} | {self.argument_slot}]"


T = TypeVar('T')


@dataclass
class GraphElement(ADT):
    value: GraphElementValue

    @classmethod
    def new(cls, in_slot: Union[GraphElement, GraphElementValue, Type[Combinator], float, int]) -> GraphElement:
        """
        Convenience function. singledispatchmethod doesn't quite cut it, so here we are
        """
        match in_slot:
            case s if isinstance(s, GraphElement):
                return cast(GraphElement, in_slot)
            case s if isinstance(s, GraphElementValue):
                return cls(s)
            case s if isinstance(s, type(Combinator)):
                return cls(in_slot())  # type: ignore
            case s if isinstance(s, float):
                return cls(Constant(s))
            case s if isinstance(s, int):
                return cls(Constant(float(s)))
        # had to take this out of case _: to make mypy happy
        raise NotImplementedError(f"Cannot instantiate GraphElement with {in_slot} of type {type(in_slot)}.")

    @classmethod
    def new_node(cls, function_slot: GraphElement, argument_slot: GraphElement) -> GraphElement:
        return cls.new(Node.new(function_slot, argument_slot))

    def eval_and_update_stack(self, stack):
        self.value.eval_and_update_stack(stack)

    @property
    def match_kwargs(self) -> Dict[Type[V], str]:
        return {
            Node: 'on_node',
            Combinator: 'on_combinator',
            Constant: 'on_constant'
        }

    @property
    def _default_expect_value_exceptions(self) -> Dict[str, Callable[[ValueType], Exception]]:
        return dict(
            on_node=lambda n: ValueError(f"Did not expect node {n}"),
            on_combinator=lambda c: ValueError(f"Did not expect combinator {c}"),
            on_constant=lambda c: ValueError(f"Did not expect constant {c}")
        )

    def equals_literal(self, other: GraphElement) -> bool:
        if not isinstance(self.value, type(other.value)):
            return False
        return self.value.equals_literal(other.value)

    def __str__(self) -> str:
        return str(self.value)
