from abc import ABC, abstractmethod
from functools import partial

from graph import Graph, GraphElement
from graph_data_types import Constant, Combinator, Node
from stack import Stack


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, graph: Graph, verbose=False) -> Graph:
        pass

    @abstractmethod
    def eval_stack(self, stack: Stack[Graph]) -> Stack[Graph]:
        pass


class VeryLazyEvaluator(Evaluator):
    def evaluate(self, graph: Graph, verbose=False) -> Graph:
        self.eval_stack(Stack[Graph](verbose=verbose).push(graph))
        return graph

    def eval_stack(self, stack: Stack[Graph]) -> Stack[Graph]:
        while len(stack) > 0:
            self.eval_component(stack, stack.peek().value)
            if stack.verbose:
                print(stack)
                print('-----')
        return stack

    def eval_component(self, stack: Stack[Graph], component: GraphElement) -> None:
        component.match(
            constant=lambda c: self.eval_constant(stack, c),
            combinator=lambda c: self.eval_combinator(stack, c),
            node=lambda n: self.eval_node(stack, n),
        )


    @staticmethod
    def eval_constant(stack: Stack[Graph], constant: Constant) -> None:
        if stack.verbose:
            print(f"encountered constant {constant.value}. Should be done.")
        stack.pop()

    @staticmethod
    def eval_combinator(stack: Stack[Graph], combinator: Combinator) -> None:
        if len(stack) < combinator.n_args + 1:
            if stack.verbose:
                print(f"{combinator.to_string()} only provided {len(stack) - 1} arguments.")
            stack.clear()
            return
        else:
            combinator.eval(stack)
            for _ in range(combinator.n_args):
                stack.pop()

    @staticmethod
    def eval_node(stack: Stack[Graph], node: Node) -> None:
        stack.push(node.function_slot)
