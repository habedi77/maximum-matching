from typing import List, Dict

import numpy as np
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool, Queue

from functools import partial

from maximum_matching.algorithms import *
import maximum_matching.graphs as graphs
import maximum_matching.utility as util
from maximum_matching.utility.result_printer import *

# For testing
PRINT_OUTPUT = False

# List the algorithms you would like the program to run
_algorithms = [
    Vaz(),  # Vazirani (Online)
    Rand(),
    MinDeg(),
    Oblivious(),
    # FeldmanTSM(),
    MaxFlow()
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
    # tqdm_inst = tqdm(algorithms, desc="Algorithms", position=2, ncols=80, ascii=True, leave=False)
    kwarg = {"historic_graph": hist_graph}

    for alg in algorithms:
        # tqdm_inst.set_postfix_str(type(alg).__name__)

        matching_size, trend = alg.run(graph=graph, **kwarg)

        if trend is not None:
            trend = np.array(trend)[:, 1]

        results.append({
            "name": type(alg).__name__,
            "matching_size": matching_size,
            "trend": trend,
        })

    return results


def process_image(alg, g):
    a_g, h_g = g
    return run_on_graph(a_g, h_g, alg)
    # print(3)
    # q.put(_res)


if __name__ == "__main__":

    final_agg_result = []
    verbose_res = []
    func = partial(process_image, _algorithms)
    tests = util.parser.load_tests_csv(file="agg_tests.csv")

    # For each item in agg_tests.csv
    for idx, t in tqdm(tests.iterrows(), total=tests.shape[0], desc="Test item", position=0, ncols=80, ascii=True):

        pool = Pool()
        try:
            # Run tests 'repeats' times with different seeds
            gs = [None] * t["repeats"]

            for s in range(t["repeats"]):
                gs[s] = t["generator"].generate(graph_class=graphs.FullMatrixGraph, seed=s, **t.to_dict())

            p_iter = pool.imap_unordered(func, gs)

            # Progress bar
            res = list(tqdm(p_iter, total=t["repeats"], desc="Progress", leave=False, position=1, ncols=80, ascii=True))

        finally:
            pool.close()
            pool.join()

        inner_results = []
        for s in range(t["repeats"]):
            inner_results += res[s]
        df = pd.DataFrame.from_records(inner_results)

        _agg_result = []
        for a in _algorithms:
            df_alg = df.loc[df['name'] == type(a).__name__]
            trend_stack = np.vstack(df_alg['trend'].to_list())
            _r = {
                "id": idx,
                "name": type(a).__name__,
                "avg_matching_size": df_alg['matching_size'].mean(),
                "std_matching_size": df_alg['matching_size'].std(),
                "avg_trend": trend_stack.mean(axis=0),
                "std_trend": trend_stack.std(axis=0),
            }
            _agg_result.append(_r)
            final_agg_result.append(_r)
            write_agg_results_v2(_agg_result, f"agg_mx_res_{idx}")
