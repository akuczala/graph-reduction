from functools import partial
from typing import TypeVar, Callable, Union, Type, Dict

from adt import adt, Case

from box import Box
from graph_data_types import EqualsLiteralMixin, GraphElementValue, ConstantType, Constant, Combinator, Node
from stack import Stack

V = TypeVar('V', bound="GraphElementValue")
T = TypeVar('T')


@adt
class GraphElement(EqualsLiteralMixin):
    CONSTANT: Case[Constant]
    COMBINATOR: Case[Combinator]
    NODE: Case[Node["Graph"]]

    def eval_and_update_stack(self, stack: Stack["Graph"]) -> None:
        self.apply_to_any(lambda gv: gv.eval_and_update_stack(stack))

    def equals_literal(self, other: "GraphElement") -> bool:
        eq = lambda s1, s2: s1.equals_literal(s2)
        return self.apply_to_any(lambda s: other.apply_to_any(partial(eq, s)))

    def apply_to_any(self, f: Callable[[GraphElementValue], T]) -> T:
        return self.match(
            constant=f, combinator=f, node=f
        )

    @property
    def _default_expect_value_exceptions(self) -> Dict[str, Callable[[GraphElementValue], Exception]]:
        return dict(
            node=lambda n: ValueError(f"Did not expect node {n}"),
            combinator=lambda c: ValueError(f"Did not expect combinator {c}"),
            constant=lambda c: ValueError(f"Did not expect constant {c}")
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

    def __str__(self) -> str:
        return self.apply_to_any(str)


class Graph(Box[GraphElement], EqualsLiteralMixin):

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
