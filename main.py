from graph import Node, FunctionSlot, Constant, ArgumentSlot, Combinator
from ski import I, K
from stack import SpineStack


def init_test():
    #node = Node(function_slot=FunctionSlot.COMBINATOR(I), argument_slot=ArgumentSlot.CONSTANT(Constant(5)))
    node1 = Node(function_slot=FunctionSlot.COMBINATOR(K), argument_slot=ArgumentSlot.CONSTANT(5))
    node0 = Node(function_slot=FunctionSlot.SUBTREE(node1), argument_slot=ArgumentSlot.COMBINATOR(K))
    print(str(node0))
    stack = SpineStack().push(node0)
    eval_stack(stack)
    print(str(node0))

def eval_stack(stack: SpineStack):
    node = stack.peek()
    # todo: do imperatively rather than recursively
    node.function_slot.match(
        combinator=lambda c: c.eval(stack),
        subtree=lambda n: eval_stack(stack.push(n))
    )

init_test()