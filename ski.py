from typing import List

from graph import GraphElement, Graph
from graph_data_types import Combinator, Node


class I(Combinator):

    @property
    def n_args(self) -> int:
        return 1

    def eval(self, args: List[Graph]):
        g = args[0]
        g.value = g.value.expect_match(node=lambda n: n.argument_slot.value)


class K(Combinator):

    @property
    def n_args(self) -> int:
        return 2

    def eval(self, args: List[Graph]):
        parent, current = args

        parent_node = parent.value.expect_match(node=lambda node: node)
        current_node = current.value.expect_match(node=lambda node: node)
        parent_node.function_slot.value = GraphElement.COMBINATOR(I())
        parent_node.argument_slot.value = current_node.argument_slot.value


class S(Combinator):

    @property
    def n_args(self) -> int:
        return 3

    def eval(self, args: List[Graph]):
        # S x y z
        g_z, g_y, g_x = args
        z, y, x = [ge.value.expect_match(node=lambda node: node).argument_slot for ge in [g_z, g_y, g_x]]
        new_1 = Graph.new_node(x, z)
        new_2 = Graph.new_node(y, z)
        g_z.value = GraphElement.NODE(Node(new_1, new_2))
