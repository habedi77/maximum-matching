import pandas as pd

"""
    Write the results from the algorithms to an xls file
"""


def write_results(result):
    array = []

    # Formatting the results for the xls file
    for i in result[0]:
        trend_matches = []
        result = [i['name'], i['matching_size'], ' ', '# Vertices evaluated']

        for k in i['trend']:
            result.append(k[0])
            trend_matches.append(k[1])

        array.append(result)
        col = [' ', ' ', ' ', '# matches']
        for matches in trend_matches:
            col.append(matches)

        array.append(col)

    df = pd.DataFrame(array).T
    df.to_excel(excel_writer="results.xls", sheet_name='sheet1')

    pass
