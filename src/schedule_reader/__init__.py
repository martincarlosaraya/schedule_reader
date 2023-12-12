from .data_reader import read_data
from .welspecs import extract_welspecs
from .compdat import extract_compdat

__all__ = ['compdat2df', 'welspecs2df']


def compdat2df(path, encoding='cp1252', verbose=False):
    return extract_compdat(read_data(path, encoding=encoding, verbose=verbose))

def welspecs2df(path, encoding='cp1252', verbose=False):
    return extract_welspecs(read_data(path, encoding=encoding, verbose=verbose))
