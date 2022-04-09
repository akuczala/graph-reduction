from box import Box
from graph import GraphElement, Graph
from evaluator import VeryLazyEvaluator
from ski import S, K, I
from ski_examples import graph_example_2, graph_example_3, graph_example_4, graph_example_5
from utils import left_associate as la

EvaluatorClass = VeryLazyEvaluator


def eval_equals_result(graph: Graph, expected_result: Graph) -> bool:
    return EvaluatorClass().evaluate(graph, verbose=True).value.equals_literal(expected_result.value)


def test_example_2():
    assert eval_equals_result(graph_example_2(), Box(GraphElement.new(5)))


def test_example_3():
    assert eval_equals_result(graph_example_3(), Box(GraphElement.new_node(S, K)))


def test_example_4():
    assert eval_equals_result(graph_example_4(), Box(GraphElement.new_node(K, I)))


def test_example_5():
    assert eval_equals_result(graph_example_5(), la(S, I, K))
