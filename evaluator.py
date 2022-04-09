from abc import ABC, abstractmethod

from graph import Graph
from stack import Stack


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, graph: Graph, verbose=False) -> Graph:
        pass

    @abstractmethod
    def eval_stack(self, stack: Stack) -> Stack:
        pass


class VeryLazyEvaluator(Evaluator):
    def evaluate(self, graph: Graph, verbose=False) -> Graph:
        self.eval_stack(Stack[Graph](verbose=verbose).push(graph))
        return graph

    def eval_stack(self, stack: Stack) -> Stack:
        while len(stack) > 0:
            stack.peek().value.eval_and_update_stack(stack)
            if stack.verbose:
                print(stack)
                print('-----')
        return stack
