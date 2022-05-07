from typing import List, Dict, Tuple
from tqdm import tqdm

from maximum_matching.algorithms.vazirani import Vaz
from maximum_matching.algorithms.Rand import Rand
from maximum_matching.algorithms.MinDegree import MinDeg
import maximum_matching.algorithms as alg
from maximum_matching.algorithms.feldmanTSM import FeldmanTSM
import maximum_matching.graphs as graphs
import maximum_matching.utility as util
from maximum_matching.utility.result_printer import write_results

# For testing
PRINT_OUTPUT = False

# List the algorithms you would like the program to run
_algorithms = [
    Vaz(),  # Vazirani (Online)
    Rand(),
    MinDeg(),
    alg.Oblivious(),
    alg.FeldmanTSM(),
    alg.MaxFlow()
]


def run_on_graph(graph: graphs.GraphBase, hist_graph: graphs.GraphBase, algorithms) -> List[Dict]:
    """
    Runts tests with a list on algorithms on a given graph

    :param graph: the populated graph to test on
    :param hist_graph: historic graph for FTSM algorithm
    :param algorithms: list on algorithms to run
    :return: a list of dictionary with the results of each algorithm
    """

    results = []
    kwarg = {"historic_graph": hist_graph}

    for algr in tqdm(algorithms, desc="Algorithms", position=1, ncols=80, ascii=True, leave=False):

        matching_size, trend = None, None

        matching_size, trend = algr.run(graph=graph, **kwarg)

        if PRINT_OUTPUT:
            print(matching_size)

        results.append({
            "name": type(algr).__name__,
            "matching_size": matching_size,
            "trend": trend,
        })

    return results


if __name__ == "__main__":

    tests = util.parser.load_tests_csv()
    result = []

    for idx, t in tqdm(tests.iterrows(), total=tests.shape[0], desc="Tests", position=0, ncols=80, ascii=True):
        actual_g, hist_g = t["generator"].generate(graph_class=graphs.FullMatrixGraph, **t.to_dict())

        result.append(run_on_graph(actual_g, hist_g, _algorithms))

        pass

    write_results(result=result)
