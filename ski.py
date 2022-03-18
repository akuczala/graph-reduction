from graph import Combinator, ArgumentSlot, FunctionSlot, Constant
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
        match node.argument_slot:
            case Constant():
                pass
            case _ as c:
                parent.function_slot = c
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

        parent.function_slot = FunctionSlot.new(I())
        parent.argument_slot = c
        stack.pop()

    @classmethod
    def to_string(cls) -> str:
        return "K"


class S(Combinator):
    pass
