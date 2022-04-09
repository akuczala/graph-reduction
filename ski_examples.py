from graph import Graph
from ski import K, I, S
from utils import left_associate as la

s = Graph.new(S)
k = Graph.new(K)
i = Graph.new(I)

def graph_example_1():
    ge0 = Graph.new_node(k, k)
    ge1 = Graph.new_node(ge0, i)
    ge2 = Graph.new_node(i, ge1)
    return ge2


def graph_example_2():
    return la(S, K, K, 5)


def graph_example_3():
    n = lambda g1, g2: Graph.new_node(g1, g2)
    return n(n(n(n(s, k), n(k, i)), s), k)  # = SK


def graph_example_4():
    # S (S K K I) K I = KI
    return la(s, la(s, k, k, i), k, i)


def graph_example_5():
    # same as 4 but S doesn't have all its arguments. Can be simplified regardless
    # S (S K K I) K = SIK
    return la(s, la(s, k, k, i), k)
