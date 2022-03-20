from graph import Node, Combinator, Constant, GraphElement
from stack import SpineStack
from ski_examples import graph_example_4


def init_test():
    top = graph_example_4()
    print(top)
    stack = SpineStack().push(top)
    eval_stack(stack, verbose=True)
    # evaluate(top)
    print(top)


def eval_stack(stack: SpineStack, verbose=False):
    while len(stack) > 0:
        stack.peek().match_value(
            on_node=lambda n: stack.push(n.function_slot),
            on_combinator=lambda c: c.eval_and_update_stack(stack, verbose=verbose),
            on_constant=lambda c: c.eval_and_update_stack(stack, verbose=verbose)
        )
        if verbose:
            print(stack)
            print('-----')


def evaluate(graph: GraphElement, verbose=False) -> GraphElement:
    eval_stack(SpineStack().push(graph), verbose=verbose)
    return graph


init_test()
