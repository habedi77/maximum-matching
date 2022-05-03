from typing import List, Dict
from tqdm import tqdm

from maximum_matching.algorithms import *
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
    Oblivious(),
    FeldmanTSM(),
    MaxFlow()
]


def run_on_graph(graph: graphs.GraphBase, hist_graph: graphs.GraphBase, algorithms, seed) -> List[Dict]:
    """
    Runts tests with a list on algorithms on a given graph

    :param graph: the populated graph to test on
    :param hist_graph: historic graph for FTSM algorithm
    :param algorithms: list on algorithms to run
    :param seed: seed to note in results
    :return: a list of dictionary with the results of each algorithm
    """

    results = []
    tqdm_inst = tqdm(algorithms, desc="Algorithms", position=2, ncols=80, ascii=True, leave=False)
    kwarg = {"historic_graph": hist_graph}

    for alg in tqdm_inst:
        tqdm_inst.set_postfix_str(type(alg).__name__)

        matching_size, trend = alg.run(graph=graph, **kwarg)

        if PRINT_OUTPUT:
            print(matching_size)

        results.append({
            "name": type(alg).__name__,
            "matching_size": matching_size,
            "trend": trend,
            "seed": seed,
        })

    return results


if __name__ == "__main__":

    tests = util.parser.load_tests_csv(file="agg_tests.csv")
    result = []

    for idx, t in tqdm(tests.iterrows(), total=tests.shape[0], desc="Test item", position=0, ncols=80, ascii=True):
        for seed in tqdm(range(t["repeats"]), desc="Iter", position=1, ncols=80, ascii=True):
            actual_g, hist_g = t["generator"].generate(
                graph_class=graphs.FullMatrixGraph, seed=seed, **t.to_dict())

            result.append(run_on_graph(actual_g, hist_g, algorithms=_algorithms, seed=seed))

        pass
    # TODO result writing
    # write_results(result=result)
