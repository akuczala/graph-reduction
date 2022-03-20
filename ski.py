from graph import Combinator, GraphElement, Node
from stack import SpineStack


class I(Combinator):

    @property
    def n_args(self) -> int:
        return 1

    def eval(self, stack: SpineStack):
        ge, _self_ge = stack.peek_at_last(2)
        ge.value = ge.value.argument_slot.value

    @classmethod
    def to_string(cls) -> str:
        return "I"


class K(Combinator):

    @property
    def n_args(self) -> int:
        return 2

    def eval(self, stack: SpineStack):
        parent, current, _self_ge = stack.peek_at_last(3)
        # we assume that parent + current are nodes
        parent_node, current_node = parent.value, current.value
        parent_node.function_slot.value = I()
        parent_node.argument_slot.value = current_node.argument_slot.value

    @classmethod
    def to_string(cls) -> str:
        return "K"


class S(Combinator):

    @property
    def n_args(self) -> int:
        return 3

    def eval(self, stack):
        # S x y z
        ge_z, ge_y, ge_x, _self_ge = stack.peek_at_last(4)
        z, y, x = [ge.value.argument_slot for ge in [ge_z, ge_y, ge_x]]
        new_ge_1 = GraphElement.new_node(x, z)
        new_ge_2 = GraphElement.new_node(y, z)
        ge_z.value = Node.new(new_ge_1, new_ge_2)

    @classmethod
    def to_string(cls) -> str:
        return "S"
