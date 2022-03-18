from graph import Node, FunctionSlot, Constant, ArgumentSlot, Combinator
from ski import I, K
from stack import SpineStack


def init_test():
    node0 = Node.new(K(), I())
    node1 = Node.new(node0, I())
    node2 = Node.new(I(), node1)
    top_node = node2
    print(top_node)
    #stack = SpineStack().push(node0)
    #eval_stack(stack)
    evaluate(top_node)
    print(top_node)


# todo figure out how this is actually supposed to work
def eval_stack(stack: SpineStack):
    node = stack.peek()
    # todo: do imperatively rather than recursively
    while len(stack) > 0:
        match node.function_slot.slot:
            case Combinator() as c:
                c.eval(stack)
            case Node(function_slot=f, argument_slot=a) as n:
                eval_stack(stack.push(n))
            case _:
                raise Exception(f"No match on {node.function_slot.slot}!")

    print(stack)

def evaluate(top_node: Node):
    stack = SpineStack().push(top_node)
    while len(stack) > 0:
        node = stack.peek()
        match node.function_slot.slot:
            case Combinator() as c:
                c.eval(stack)
            case Node(function_slot=f, argument_slot=a) as n:
                stack.push(n)
            case _:
                raise Exception(f"No match on {node.function_slot.slot}!")
    return top_node

init_test()
