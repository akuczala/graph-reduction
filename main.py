from evaluator import VeryLazyEvaluator
from ski_examples import graph_example_4, graph_example_3


def init_test():
    top = graph_example_3()
    print(top)
    VeryLazyEvaluator().evaluate(top, verbose=True)
    print(top)


init_test()
