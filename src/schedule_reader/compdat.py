import pandas as pd
import numpy as np

from .dates import parse_dates
from .extract_keyword import extract_keyword
from .welspecs import extract_welspecs


def _defaultIJ(well, date, IJ, welspecs_table):
    """
    Helper function to find the I and J coordinates for a well, from its WELSPECS definition.
    Used when the I or J coordinates are defaulted in the COMPDAT keyword.

    Params:
        well: str
        date: str or datetime
        IJ: str 'I' 'J'
            the coordinate to be extracted
        welspecs_table: pandas.DataFrame
            A DataFrame containing at least the 'date', 'well', 'I' and 'J' data from the WELSPEC keyword.
            This DataFrame is prepared by the function `extract_welspecs`. It is automatically called by the function `extract_compdat` if required.
    """
    return welspecs_table[(welspecs_table['well'] == well) & (welspecs_table['date'] <= date), IJ].iloc[-1]


def extract_compdat(schedule_dict):
    """
    Shortcut for `extract_keyword` for the COMPDAT keyword.
    Extract the COMPDAT keyword from the schedule dictionary and return a DataFrame of WELSPECS data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    compdat_columns = ['date', 'well', 'I', 'J', 'K_up', 'K_low', 'status', 'saturation table', 'transimissibility factor', 'well bore diameter', 'Kh', 'skin', 'D-factor', 'direction', 'pressure equivalent radius']
    compdat_table = extract_keyword(schedule_dict, 'COMPDAT', compdat_columns)  # {}
    compdat_table['date'] = parse_dates(compdat_table['date'].to_list())  # to parse dates exactly as stated by DATES eclipse format
    compdat_table['well'] = [well.strip("'") for well in compdat_table['well']]
    compdat_table['well'] = compdat_table['well'].astype('category', errors='ignore')
    compdat_table.replace('1*', None, inplace=True)
    compdat_table.replace("'1*'", None, inplace=True)
    to_int = ['I', 'J', 'K_up', 'K_low']
    compdat_table[to_int] = compdat_table[to_int].fillna('0').astype(int, errors='ignore')
    if 0 in compdat_table['I'].values or 0 in compdat_table['J'].values:
        welspecs_table = extract_welspecs(schedule_dict)
        if 0 in compdat_table['I'].values:
            compdat_table['I'] = [compdat_table['I'].iloc[r] if compdat_table['I'].iloc[r] > 0 else _defaultIJ(compdat_table['date'].iloc[r], compdat_table['date'].iloc[r], 'I', welspecs_table) for r in len(compdat_table)]
        if 0 in compdat_table['J'].values:
            compdat_table['J'] = [compdat_table['I'].iloc[r] if compdat_table['I'].iloc[r] > 0 else _defaultIJ(compdat_table['date'].iloc[r], compdat_table['date'].iloc[r], 'J', welspecs_table) for r in len(compdat_table)]
    to_float = ['transimissibility factor', 'well bore diameter', 'Kh', 'skin', 'D-factor', 'pressure equivalent radius']
    compdat_table[to_float] = compdat_table[to_float].astype(float, errors='ignore')
    compdat_table['status'] = compdat_table['status'].fillna('OPEN').astype('category', errors='ignore')
    compdat_table['skin'].fillna(0.0, inplace=True)
    compdat_table['direction'] = compdat_table['direction'].fillna('Z').astype('category', errors='ignore')
    return compdat_table

