from graph import GraphElement
from ski import K, I, S
from utils import left_associate


def graph_example_1():
    ge0 = GraphElement.new_node(K(), K())
    ge1 = GraphElement.new_node(ge0, I())
    ge2 = GraphElement.new_node(I(), ge1)
    return ge2


def graph_example_2():
    return left_associate(S, K, K, 5)


def graph_example_3():
    n = GraphElement.new_node
    return n(n(n(n(S, K), n(K, I)), S), K)  # = SK


def graph_example_4():
    # S (S K K I) K I
    la = left_associate
    return la(S, la(S, K, K, I), K, I)  # = KI