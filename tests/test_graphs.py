from graph import GraphElement, Graph, Constant
from ski import I, K


def test_ge_equality():
    i1 = I()
    i2 = I()
    k = K()
    assert i1 == i2
    assert i1 != k

    assert Constant(5) == Constant(5)
    assert Constant(5) != Constant(6)

    assert Constant(5) != I()

    assert GraphElement.COMBINATOR(i1) == GraphElement.COMBINATOR(i2)
    assert GraphElement.COMBINATOR(i1) != GraphElement.COMBINATOR(k)


def test_graph_equality():
    g1, g2, g3 = Graph.new(5), Graph.new(5), Graph.new(10)
    assert g1.equals_literal(g2) and not g1.equals_literal(g3)

    g1, g2, g3 = Graph.new(I), Graph.new(I), Graph.new(K)
    assert g1.equals_literal(g2) and not g1.equals_literal(g3)

    g1 = Graph.new_node(Graph.new(K), Graph.new(5))
    g2 = Graph.new_node(Graph.new(K), Graph.new(5))
    g3 = Graph.new_node(Graph.new(K), Graph.new(1))

    assert g1.equals_literal(g2) and not g1.equals_literal(g3)

    g1 = Graph.new(10);
    g2 = Graph.new(I);
    g3 = Graph.new(I)

    assert Graph.new_node(g1, g2).equals_literal(Graph.new_node(g1, g2))
    assert Graph.new_node(g1, g2).equals_literal(Graph.new_node(g1, g3))
    assert not Graph.new_node(g1, g2).equals_literal(Graph.new_node(g3, g1))
