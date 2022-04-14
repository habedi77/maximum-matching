import numpy as np
import pandas as pd
from .gaussian_generator import GaussianGenerator


def load_tests_csv(file="tests.csv") -> pd.DataFrame:
    """
    load the tests csv and parse the generators to their objects
    :param file: tests csv file. defaults to "tests.csv"
    :return: pandas dataframe with tests parameters, generators and their parameters
    """
    replace_dict = {
        np.nan: None,
        "gaussian": GaussianGenerator()
    }

    df = pd.read_csv(file, index_col="id")

    set_generators = set(df["generator"])
    if len(set_generators - set(replace_dict.keys())) > 0:
        raise ValueError(f"Unrecognized generators: {set_generators - set(replace_dict.keys())}")

    df = df.replace(replace_dict)

    return df
