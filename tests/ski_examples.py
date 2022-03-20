from graph import GraphElement
from main import evaluate
from ski import S, K, I
from ski_examples import graph_example_2, graph_example_3, graph_example_4


def eval_equals_result(graph: GraphElement, expected_result: GraphElement) -> bool:
    return evaluate(graph).equals_literal(expected_result)


def test_example_2():
    assert eval_equals_result(graph_example_2(), GraphElement.new(5))


def test_example_3():
    assert eval_equals_result(graph_example_3(), GraphElement.new_node(S, K))


def test_example_4():
    assert eval_equals_result(graph_example_4(), GraphElement.new_node(K, I))
