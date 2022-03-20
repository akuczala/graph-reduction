from graph import Node, Combinator, GraphElement, Constant
from ski import I, K, S
from stack import SpineStack


def graph_example_1():
    ge0 = GraphElement.new_node(K(), K())
    ge1 = GraphElement.new_node(ge0, I())
    ge2 = GraphElement.new_node(I(), ge1)
    return ge2


def graph_example_2():
    ge0 = GraphElement.new_node(S(), K())
    ge1 = GraphElement.new_node(ge0, K())
    ge2 = GraphElement.new_node(ge1, 5)
    return ge2


def graph_example_3():
    n = GraphElement.new_node
    return n(n(n(n(S(), K()), n(K(), I())), S()), K())


def init_test():
    top = graph_example_3()
    print(top)
    stack = SpineStack().push(top)
    eval_stack(stack)
    # evaluate(top)
    print(top)


def eval_stack(stack: SpineStack):
    while len(stack) > 0:
        ge = stack.peek()
        match ge.value:
            case Node(function_slot=f, argument_slot=a):
                stack.push(f)
            case Combinator() as c:
                c.count_args_and_eval(stack)
            case Constant(val):
                print(f"encountered constant {val}. Should be done.")
                return
            case _:
                raise ValueError(f"{ge.value} of type {type(ge.value)} is not a valid graph element value")
        print(stack)
        print('-----')
    print(stack)


init_test()
