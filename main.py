from evaluator import VeryLazyEvaluator
from ski_examples import graph_example_4


def init_test():
    top = graph_example_4()
    print(top)
    VeryLazyEvaluator().evaluate(top, verbose=True)
    print(top)

init_test()
