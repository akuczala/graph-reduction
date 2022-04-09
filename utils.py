from functools import reduce

from graph import Graph


def raise_exception(e: Exception):
    raise e


def left_associate(*s):
    return reduce(lambda x0, x1: Graph.new_node(x0, x1), s)
