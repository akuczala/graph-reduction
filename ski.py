from graph import GraphElement, Graph
from graph_data_types import Combinator, Node
from stack import Stack


class I(Combinator):

    @property
    def n_args(self) -> int:
        return 1

    def eval(self, stack: Stack[Graph]):
        ge, _self_ge = stack.peek_at_last(2)
        ge.value = ge.value.expect_value(node=lambda n: n.argument_slot.value)


class K(Combinator):

    @property
    def n_args(self) -> int:
        return 2

    def eval(self, stack: Stack[Graph]):
        parent, current, _self_ge = stack.peek_at_last(3)
        # we assume that parent + current are nodes

        parent_node = parent.value.expect_value(node=lambda node: node)
        current_node = current.value.expect_value(node=lambda node: node)
        parent_node.function_slot.value = GraphElement.COMBINATOR(I())
        parent_node.argument_slot.value = current_node.argument_slot.value


class S(Combinator):

    @property
    def n_args(self) -> int:
        return 3

    def eval(self, stack: Stack[Graph]):
        # S x y z
        ge_z, ge_y, ge_x, _self_ge = stack.peek_at_last(4)
        z, y, x = [ge.value.expect_value(node=lambda node: node).argument_slot for ge in [ge_z, ge_y, ge_x]]
        new_ge_1 = Graph.new_node(x, z)
        new_ge_2 = Graph.new_node(y, z)
        ge_z.value = GraphElement.NODE(Node(new_ge_1, new_ge_2))
