from abc import abstractmethod
from dataclasses import dataclass
from functools import partial
from typing import TypeVar, Callable, Union, Type, Dict, cast

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


ConstantType = float


@dataclass(frozen=True)
class Constant(GraphElementValue):
    value: ConstantType

    def __str__(self) -> str:
        return str(self.value)

    def eval_and_update_stack(self, stack):
        if stack.verbose:
            print(f"encountered constant {self.value}. Should be done.")
        stack.pop()

    def equals_literal(self, other) -> bool:
        return self == other


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

    def equals_literal(self, other) -> bool:
        return self == other

    @abstractmethod
    def eval(self, stack):
        pass

    @classmethod
    @abstractmethod
    def to_string(cls) -> str:
        pass

    def __str__(self) -> str:
        return self.to_string()

    def __eq__(self, other):
        return isinstance(other, Combinator) and type(self) == type(other)


@dataclass(frozen=True)
class Node(GraphElementValue):
    function_slot: "Graph"
    argument_slot: "Graph"

    def eval_and_update_stack(self, stack):
        stack.push(self.function_slot)

    def equals_literal(self, other) -> bool:
        if not isinstance(other, Node):
            return False
        return (
                self.function_slot.equals_literal(other.function_slot) and
                self.argument_slot.equals_literal(other.argument_slot)
        )

    def __str__(self) -> str:
        return f"[{self.function_slot} | {self.argument_slot}]"


T = TypeVar('T')


@adt
class GraphElement:
    CONSTANT: Case[Constant]
    COMBINATOR: Case[Combinator]
    NODE: Case[Node]

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
            constant=partial(eq, s), combinator=partial(eq, s), node=partial(eq, s)
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


class Graph(Box[GraphElement]):

    def __init__(self, value: GraphElement):
        super().__init__(value)

    @classmethod
    def new(cls, arg: Union["Graph", GraphElement, GraphElementValue, Type[Combinator], ConstantType, int]):
        match arg:
            case GraphElement() as ge:
                return cls(ge)
            case Constant() as c:
                return cls.new_constant(c)
            case Combinator() as c:
                return cls.new_combinator(c)
            case s if isinstance(s, type(Combinator)):
                return cls.new_combinator(s())  # type: ignore
            case s if isinstance(s, ConstantType) or isinstance(s, int):
                return cls.new_constant(s)
            # had to take this out of case _: to make mypy happy
        raise NotImplementedError(f"Cannot instantiate GraphElement with {arg} of type {type(arg)}.")

    @classmethod
    def new_node(cls, function_slot: "Graph", argument_slot: "Graph"):
        return cls(GraphElement.NODE(Node(function_slot, argument_slot)))

    @classmethod
    def new_combinator(cls, combinator: "Combinator"):
        return cls(GraphElement.COMBINATOR(combinator))

    @classmethod
    def new_constant(cls, constant: Union[Constant, ConstantType]):
        match constant:
            case Constant(_) as c:
                return cls(GraphElement.CONSTANT(c))
            case c if isinstance(c, ConstantType) or isinstance(c, int):
                return cls(GraphElement.CONSTANT(Constant(c)))
            case c:
                raise TypeError(f"Cannot build constant graph from type {type(c)}")

    def equals_literal(self, other: "Graph") -> bool:
        return self.value.equals_literal(other.value)

    def __str__(self):
        return str(self.value)
