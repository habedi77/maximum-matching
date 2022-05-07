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

tests = util.parser.load_tests_csv(file='agg_tests.csv')

summary = {
    'id': [],
    'size left': [],
    'size right': [],
    'generator': [],
    'mean': [],
    'std': [],
    'Vazirani': [],
    'Min Deg': [],
    'Oblivious': [],
    'Random': [],
    # 'Feldman TSM': [],
    'Max Flow': [],
    'std Vazirani': [],
    'std Min Deg': [],
    'std Oblivious': [],
    'std Random': [],
    # 'std Feldman TSM': [],
    'std Max Flow': [],

    # MaxFlow_matching_avg_std
    # MinDeg_matching_avg_std
    # Oblivious_matching_avg_std
    # Rand_matching_avg_std
    # Vaz_matching_avg_std

}

for idx, t in tests.iterrows():
    file = f'results/agg_mp_res_{str(idx)}.csv'
    df = pd.read_csv(file)

    summary['id'].append(idx)
    summary['size left'].append(t['size_left'])
    summary['size right'].append(t['size_right'])
    summary['generator'].append(type(t['generator']).__name__)
    summary['mean'].append(t['mean'])
    summary['std'].append(t['std'])

    summary['Vazirani'].append(df['Vaz_matching_avg_std'][0])
    summary['Min Deg'].append(df['MinDeg_matching_avg_std'][0])
    summary['Oblivious'].append(df['Oblivious_matching_avg_std'][0])
    summary['Random'].append(df['Rand_matching_avg_std'][0])
    # summary['Feldman TSM'].append(df['FeldmanTSM_matching_avg_std'][0])
    summary['Max Flow'].append(df['MaxFlow_matching_avg_std'][0])

    summary['std Vazirani'].append(df['Vaz_matching_avg_std'][1])
    summary['std Min Deg'].append(df['MinDeg_matching_avg_std'][1])
    summary['std Oblivious'].append(df['Oblivious_matching_avg_std'][1])
    summary['std Random'].append(df['Rand_matching_avg_std'][1])
    # summary['std Feldman TSM'].append(df['FeldmanTSM_matching_avg_std'][1])
    summary['std Max Flow'].append(df['MaxFlow_matching_avg_std'][1])

d = pd.DataFrame.from_dict(summary)
d.to_csv('final_summary.csv')
