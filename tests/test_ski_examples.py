from graph import Graph
from evaluator import VeryLazyEvaluator
from ski import S, K, I
from ski_examples import graph_example_2, graph_example_3, graph_example_4, graph_example_5
from utils import left_associate as la

EvaluatorClass = VeryLazyEvaluator

s = Graph.new(S)
k = Graph.new(K)
i = Graph.new(I)


def eval_equals_result(graph: Graph, expected_result: Graph) -> bool:
    return EvaluatorClass().evaluate(graph, verbose=True).equals_literal(expected_result)


def test_example_2():
    assert eval_equals_result(graph_example_2(), Graph.new(5))


def test_example_3():
    assert eval_equals_result(graph_example_3(), Graph.new_node(s, k))


def test_example_4():
    assert eval_equals_result(graph_example_4(), Graph.new_node(k, i))


# This test fails with VeryLazyEvaluator
# def test_example_5():
#     assert eval_equals_result(graph_example_5(), la(s, i, k))
