import pandas as pd

__all__ = ['read_keyword_from_include', 'expand_keyword', 'ijk_index']

def read_keyword_from_include(path, keyword=None, encoding='cp1252'):
    """
    reads the ASCII include file from the `path`, looks for the `keyword` and extracts its data.

    Returns:

    """
    with open(path, 'r') as f:
        keyword_data = ''.join(f.readlines())
    
    if keyword not in keyword_data:
        raise ValueError(f"The requested keyword {keyword} is not in this file {path}")

    i = keyword_data.index(keyword)
    f = keyword_data.index('/', i)
    keyword_data = keyword_data[i+len(keyword): f].strip()

    while '--' in keyword_data:
        i = keyword_data.index('--')
        f = keyword_data.index('\n', i)
        keyword_data = keyword_data[:i] + keyword_data[f+1:]
    
    return keyword_data

def expand_keyword(string):
    """
    received the string readout from the property keyword and return the string property expanded.
    """
    return ' '.join(
        [' '.join([each.split('*')[1]] * int(each.split('*')[0])) 
         if '*' in each
         else each
         for each in string.split()]
    )

def ijk_index(i, j=None, k=None):
    if j is None and k is None and hasattr(i, '__iter__') and len(i) == 3 \
        and i[0] is not None and i[1] is not None and i[2] is not None:
        i, j, k = i[0], i[1], i[2]
    elif j is None or k is None:
        raise ValueError(f"must provide i, j, k or a tuple of (i, j, k), but received i={i}, j={j}, k={k}")

    cells = [(i_, j_, k_)
             for k_ in range(1, k+1)
             for j_ in range(1, j+1)
             for i_ in range(1, i+1)
             ]
    return pd.MultiIndex.from_tuples(cells)
    