import pandas as pd

__all__ = ['read_keyword_from_include', 'expand_keyword', 'ijk_index']

def read_keyword_from_include(path, keyword=None, encoding='cp1252'):
    """
    reads the ASCII include file from the `path`, looks for the `keyword` and extracts its data.

    Returns:

    """
    with open(path, 'r') as f:
        keyword_data = f.readlines()
    
    if keyword not in keyword_data:
        raise ValueError(f"The requested keyword {keyword} is not in this file {path}")

    keyword_data = ''.join(keyword_data)
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

def ijk_index(i, j, k):
    cells = [(i, j, k)
             for k in range(1, dimens[2]+1)
             for j in range(1, dimens[1]+1)
             for i in range(1, dimens[0]+1)
             ]
    return pd.MultiIndex.from_tuples(cells))
    