import pandas as pd
from .data_reader import read_data
from .welspec import extract_welspecs, extract_welspecl, extract_wellspec, extract_welspec2
from .compdat import extract_compdat, extract_compdatl, extract_compdat2
from .wcon import extract_wconprod, extract_wconinje, extract_wconhist, extract_wconinjh
from .property_keywords import read_keyword_from_include, expand_keyword, ijk_index
from .extract_keyword import extract_keyword
from .counter import start_counter

__all__ = ['compdat2df', 'welspecs2df', 'property2df', 'start_counter']
__version__ = '0.5.0'


def compdat2df(path, encoding='cp1252', verbose=False):
    return extract_compdat2(read_data(path, encoding=encoding, verbose=verbose))

def welspec2df(path, encoding='cp1252', verbose=False):
    return extract_welspec2(read_data(path, encoding=encoding, verbose=verbose))

def wconprod2df(path, encoding='cp1252', verbose=False):
    return extract_wconprod(read_data(path, encoding=encoding, verbose=verbose))

def wconinje2df(path, encoding='cp1252', verbose=False):
    return extract_wconinje(read_data(path, encoding=encoding, verbose=verbose))

def wconhist2df(path, encoding='cp1252', verbose=False):
    return extract_wconhist(read_data(path, encoding=encoding, verbose=verbose))

def wconinjh2df(path, encoding='cp1252', verbose=False):
    return extract_wconinjh(read_data(path, encoding=encoding, verbose=verbose))

def keyword2df(path, keyword, record_names=[], encoding='cp1252', verbose=True):
    return extract_keyword(
        read_data(path, encoding=encoding, verbose=verbose),
        keyword=keyword, record_names=record_names
    )

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
