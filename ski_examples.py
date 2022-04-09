from box import Box
from graph import GraphElement, Node
from ski import K, I, S
from utils import left_associate as la


def graph_example_1():
    ge0 = Box(GraphElement.new_node(K(), K()))
    ge1 = Box(GraphElement.new_node(ge0, I()))
    ge2 = Box(GraphElement.new_node(I(), ge1))
    return ge2


def graph_example_1_spelled_out():
    ge0 = Box(GraphElement.NODE(Node(
        Box(GraphElement.COMBINATOR(K())),
        Box(GraphElement.COMBINATOR(K()))
    )))
    ge1 = Box(GraphElement.NODE(
        Node(ge0, Box(GraphElement.COMBINATOR(I())))
    ))
    ge2 = Box(GraphElement.NODE(Node(
            Box(GraphElement.COMBINATOR(I())),
            ge1
    )))
    return ge2


def graph_example_2():
    return la(S, K, K, 5)


def graph_example_3():
    #n = GraphElement.new_node
    n = lambda g1, g2: Box(GraphElement.NODE(Node(g1, g2)))
    s = Box(GraphElement.COMBINATOR(S()))
    k = Box(GraphElement.COMBINATOR(K()))
    i = Box(GraphElement.COMBINATOR(I()))
    return n(n(n(n(s, k), n(k, i)), s), k)  # = SK


def graph_example_4():
    # S (S K K I) K I = KI
    return la(S, la(S, K, K, I), K, I)


def graph_example_5():
    # same as 4 but S doesn't have all its arguments. Can be simplified regardless
    # S (S K K I) K = SIK
    return la(S, la(S, K, K, I), K)
