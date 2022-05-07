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
    Vaz(),
    Rand(),
    MinDeg(),
    Oblivious(),
    # FeldmanTSM(),
    MaxFlow()
]


def run_on_graph(id, graph, hist_graph, alg) -> Dict:
    """
    Runts tests with a list on algorithms on a given graph

    :param id: testing id
    :param graph: the populated graph to test on
    :param hist_graph: historic graph for FTSM algorithm
    :param alg: algorithm to run
    :return: a list of dictionary with the results of each algorithm
    """

    kwarg = {"historic_graph": hist_graph}

    matching_size, trend = alg.run(graph=graph, **kwarg)

    if trend is not None:
        trend = np.array(trend)[:, 1]

    return {
        "id": id,
        "name": type(alg).__name__,
        "matching_size": matching_size,
        "trend": trend,
    }


def process_image(arg):
    id, alg, a_g, h_g = arg
    return run_on_graph(id=id, graph=a_g, hist_graph=h_g, alg=alg)


if __name__ == "__main__":

    all_res = []
    test_file = "agg_tests.csv"
    tests = util.parser.load_tests_csv(file=test_file)

    print(f"Preparing tests")
    args = []  # List of (id, algorithm, graph, hist_graph)
    for idx, t in tqdm(tests.iterrows(), total=tests.shape[0], desc="Test", ncols=80, ascii=True, leave=False):
        # For each item in agg_tests.csv
        for s in tqdm(range(t["repeats"]), desc="Repeat", position=1, ncols=70, ascii=True, leave=False):
            # Run tests 'repeats' times with different seeds
            ga, gh = t["generator"].generate(graph_class=graphs.FullMatrixGraph, seed=s, **t.to_dict())
            for a in tqdm(_algorithms, desc="Repeat", position=2, ncols=60, ascii=True, leave=False):
                # For each algorithm
                args.append((idx, a, ga, gh))

    print(f"Prepared {len(args)} tests")
    pool = Pool()
    try:
        p_iter = pool.imap_unordered(process_image, args)
        # Progress bar
        res = list(tqdm(p_iter, total=len(args), desc="Process", leave=False, position=1, ncols=100, ascii=True))
    finally:
        pool.close()
        pool.join()

    df = pd.DataFrame.from_records(res)
    df.to_csv("full_test.csv")

    tests = util.parser.load_tests_csv(file=test_file)
    for idx, t in tests.iterrows():
        df_id = df.loc[df['id'] == idx]
        _agg_result = []
        for a in _algorithms:
            df_alg = df_id.loc[df_id['name'] == type(a).__name__]
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
            write_agg_results_v2(_agg_result, f"agg_mp_res_{idx}")
