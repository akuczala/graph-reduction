from abc import ABC, abstractmethod

from graph import GraphElement
from stack import SpineStack


class Evaluator(ABC):

    @abstractmethod
    def evaluate(self, graph: GraphElement, verbose=False) -> GraphElement:
        pass

    @abstractmethod
    def eval_stack(self, stack: SpineStack) -> SpineStack:
        pass


class VeryLazyEvaluator(Evaluator):
    def evaluate(self, graph: GraphElement, verbose=False) -> GraphElement:
        self.eval_stack(SpineStack(verbose=verbose).push(graph))
        return graph

    def eval_stack(self, stack: SpineStack) -> SpineStack:
        while len(stack) > 0:
            stack.peek().match_value(
                on_node=lambda n: stack.push(n.function_slot),
                on_combinator=lambda c: c.eval_and_update_stack(stack),
                on_constant=lambda c: c.eval_and_update_stack(stack)
            )
            if stack.verbose:
                print(stack)
                print('-----')
        return stack
