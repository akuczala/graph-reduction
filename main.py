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
        ge = stack.peek()
        match ge.value:
            case Node(function_slot=f, argument_slot=a):
                stack.push(f)
            case Combinator() as c:
                c.eval_and_update_stack(stack, verbose=verbose)
            case Constant(val):
                if verbose:
                    print(f"encountered constant {val}. Should be done.")
                return
            case _:
                raise ValueError(f"{ge.value} of type {type(ge.value)} is not a valid graph element value")
        if verbose:
            print(stack)
            print('-----')


def evaluate(graph: GraphElement) -> GraphElement:
    eval_stack(SpineStack().push(graph))
    return graph


init_test()
