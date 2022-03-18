from graph import Combinator, ArgumentSlot, FunctionSlot
from stack import SpineStack
from utils import raise_exception


class I(Combinator):
    pass

    @classmethod
    def eval(cls, stack: SpineStack):
        if len(stack) == 1:  # we are done!
            stack.pop()
            return
        parent, node = stack.peek_at_last(2)
        parent.function_slot = node.argument_slot.match(
            combinator=lambda c: FunctionSlot.COMBINATOR(c),
            subtree=lambda t: FunctionSlot.SUBTREE(t),
            constant=lambda c: parent.function_slot
        )
        stack.pop()

    @classmethod
    def to_string(cls) -> str:
        return "I"


class K(Combinator):

    @classmethod
    def eval(cls, stack: SpineStack):
        parent, node = stack.peek_at_last(2)
        x = parent.argument_slot  # gets thrown away
        c = node.argument_slot

        parent.function_slot = FunctionSlot.COMBINATOR(I)
        parent.argument_slot = c.match(
            combinator=lambda c: ArgumentSlot.COMBINATOR(c),
            subtree=lambda t: ArgumentSlot.SUBTREE(t),
            constant=lambda c: ArgumentSlot.CONSTANT(c)
        )
        stack.pop()

    @classmethod
    def to_string(cls) -> str:
        return "K"


class S(Combinator):
    pass
