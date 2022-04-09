from abc import abstractmethod, ABC
from dataclasses import dataclass
from functools import partial
from typing import TypeVar, Callable, Union, Type, Dict, cast, Optional

from adt import adt, Case

from box import Box

V = TypeVar('V', bound="GraphElementValue")


class GraphElementValue:
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

    def equals_literal(self, other: "Constant") -> bool:
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

    def equals_literal(self, other: "Combinator") -> bool:
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
    function_slot: Box["GraphElement"]
    argument_slot: Box["GraphElement"]

    @classmethod
    def new(cls, in_function_slot, in_argument_slot) -> "Node":
        return cls(
            function_slot=Box(GraphElement.new(in_function_slot)),
            argument_slot=Box(GraphElement.new(in_argument_slot))
        )

    def eval_and_update_stack(self, stack):
        stack.push(self.function_slot)

    def equals_literal(self, other: "Node") -> bool:
        return (
                self.function_slot.value.equals_literal(other.function_slot.value) and
                self.argument_slot.value.equals_literal(other.argument_slot.value)
        )

    def __str__(self) -> str:
        return f"[{self.function_slot} | {self.argument_slot}]"


T = TypeVar('T')


# todo: figure out how references work here. Might want to make GraphElementValue an ADT instead
# we want to be able to "swap out" different ADT instances at the same place in memory
@adt
class GraphElement:
    CONSTANT: Case[Constant]
    COMBINATOR: Case[Combinator]
    NODE: Case[Node]

    @classmethod
    def new(cls, in_slot: Union["GraphElement", GraphElementValue, Type[Combinator], float, int]) -> "GraphElement":
        """
        Convenience function. singledispatchmethod doesn't quite cut it, so here we are
        """
        match in_slot:
            case s if isinstance(s, GraphElement):
                return cast(GraphElement, in_slot)
            case s if isinstance(s, Constant):
                return cls.CONSTANT(s)
            case s if isinstance(s, Combinator):
                return cls.COMBINATOR(s)
            case s if isinstance(s, Node):
                return cls.NODE(s)
            case s if isinstance(s, type(Combinator)):
                return cls.COMBINATOR(in_slot())  # type: ignore
            case s if isinstance(s, float):
                return cls.CONSTANT(Constant(s))
            case s if isinstance(s, int):
                return cls.CONSTANT(Constant(float(s)))
        # had to take this out of case _: to make mypy happy
        raise NotImplementedError(f"Cannot instantiate GraphElement with {in_slot} of type {type(in_slot)}.")

    @classmethod
    def new_node(cls, function_slot: "GraphElement", argument_slot: "GraphElement") -> "GraphElement":
        return cls.NODE(Node.new(function_slot, argument_slot))

    def eval_and_update_stack(self, stack):
        self.value.eval_and_update_stack(stack)

    @property
    def _default_expect_value_exceptions(self) -> Dict[str, Callable[[GraphElementValue], Exception]]:
        return dict(
            node=lambda n: ValueError(f"Did not expect node {n}"),
            combinator=lambda c: ValueError(f"Did not expect combinator {c}"),
            constant=lambda c: ValueError(f"Did not expect constant {c}")
        )

    def equals_literal(self, other: "GraphElement") -> bool:
        eq = lambda s1, s2: s1.equals_literal(s2)
        eqs: Callable[[GraphElementValue], bool] = lambda s: other.match(
            constant=partial(eq)(s), combinator=partial(eq)(s), node=partial(eq)(s)
        )
        return self.match(
            constant=eqs, combinator=eqs, node=eqs
        )

    def __str__(self) -> str:
        return self.match(
            constant=str,
            combinator=str,
            node=str
        )

    def expect_value(self,
                     **kwargs: Callable[[GraphElementValue], Union[T, Exception]]) -> T:
        """
        Raises error if we match on something we don't specify a lambda for. Error messages can be customized
        by passing lambdas that return Exceptions
        """
        result: T = self.match(**dict(self._default_expect_value_exceptions, **kwargs))
        if isinstance(result, Exception):
            raise result
        else:
            return result


Graph = Box[GraphElement]
