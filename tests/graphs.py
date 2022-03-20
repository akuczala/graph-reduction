from graph import GraphElement, Node
from ski import I, K


def test_graph_equality():
    g1, g2, g3 = GraphElement.new(5), GraphElement.new(5), GraphElement.new(10)
    assert g1.equals_literal(g2) and not g1.equals_literal(g3)

    g1, g2, g3 = GraphElement.new(I), GraphElement.new(I), GraphElement.new(K)
    assert g1.equals_literal(g2) and not g1.equals_literal(g3)

    g1 = GraphElement.new_node(GraphElement.new(K), GraphElement.new(5))
    g2 = GraphElement.new_node(GraphElement.new(K), GraphElement.new(5))
    g3 = GraphElement.new_node(GraphElement.new(K), GraphElement.new(1))

    assert g1.equals_literal(g2) and not g1.equals_literal(g3)
