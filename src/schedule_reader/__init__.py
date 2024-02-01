import pandas as pd
from .data_reader import read_data
from .welspecs import extract_welspecs
from .compdat import extract_compdat
from .property_keywords import read_keyword_from_include, expand_keyword, ijk_index
from .counter import start_counter

__all__ = ['compdat2df', 'welspecs2df', 'property2df', 'start_counter']


def compdat2df(path, encoding='cp1252', verbose=False):
    return extract_compdat(read_data(path, encoding=encoding, verbose=verbose))

def welspecs2df(path, encoding='cp1252', verbose=False):
    return extract_welspecs(read_data(path, encoding=encoding, verbose=verbose))

def property2df(path, keyword, dimens=(None, None, None), encoding='cp1252', verbose=False, parse_to=None):
    keyword_data = expand_keyword(read_keyword_from_include(path, keyword, encoding='cp1252'))
    if dimens[0] is not None and dimens[1] is not None and dimens[2] is not None:
        cells = ijk_index(dimens[0], dimens[1], dimens[2])
        output = pd.Series(
            keyword_data.split(),
            index=pd.MultiIndex.from_tuples(cells),
            name=keyword).reset_index()
        output.columns = ['I', 'J', 'K', keyword]
        output[['I', 'J', 'K']] = output[['I', 'J', 'K']].astype(int)
        if parse_to is None:
            pars_to = int if keyword.endswith('NUM') else float
        output[keyword] = output[keyword].astype(parse_to)
        return output
    else:
        return keyword_data
