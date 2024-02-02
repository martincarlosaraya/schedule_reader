import pandas as pd
import numpy as np

from .dates import parse_dates
from .schedule_keywords import extract_keyword
from .welspec import extract_welspecs, extract_welspecl


def _defaultIJ(well, date, IJ, welspec_table):
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
    return welspec_table[(welspec_table['well'] == well) & (welspec_table['date'] <= date), IJ].iloc[-1]


def extract_compdat(schedule_dict):
    """
    Shortcut for `extract_keyword` for the COMPDAT keyword.
    Extract the COMPDAT keyword from the schedule dictionary and return a DataFrame of COMPDAT data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    compdat_columns = ['date', 'well', 'I', 'J', 'K_up', 'K_low', 'status', 'saturation table', 'transimissibility factor', 'well bore diameter', 'Kh', 'skin', 'D-factor', 'direction', 'pressure equivalent radius']
    compdat_table = extract_keyword(schedule_dict, 'COMPDAT', compdat_columns)  # {}
    if len(compdat_table) > 0:
        compdat_table['date'] = parse_dates(compdat_table['date'].to_list())  # to parse dates exactly as stated by DATES eclipse format
        compdat_table['well'] = [well.strip("'") for well in compdat_table['well']]
        compdat_table['well'] = compdat_table['well'].astype('category', errors='ignore')
        compdat_table.replace('1*', np.nan, inplace=True)
        compdat_table.replace("'1*'", np.nan, inplace=True)
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


def extract_compdatl(schedule_dict):
    """
    Shortcut for `extract_keyword` for the COMPDAT keyword.
    Extract the COMPDAT keyword from the schedule dictionary and return a DataFrame of COMPDATL data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    compdatl_columns = ['date', 'well', 'local grid', 'I', 'J', 'K_up', 'K_low', 'status', 'saturation table', 'transimissibility factor', 'well bore diameter', 'Kh', 'skin', 'D-factor', 'direction', 'pressure equivalent radius']
    compdatl_table = extract_keyword(schedule_dict, 'COMPDATL', compdatl_columns)  # {}
    if len(compdatl_table) > 0:
        compdatl_table['date'] = parse_dates(compdatl_table['date'].to_list())  # to parse dates exactly as stated by DATES eclipse format
        compdatl_table['well'] = [well.strip("'") for well in compdatl_table['well']]
        compdatl_table['well'] = compdatl_table['well'].astype('category', errors='ignore')
        compdatl_table.replace('1*', np.nan, inplace=True)
        compdatl_table.replace("'1*'", np.nan, inplace=True)
        to_int = ['I', 'J', 'K_up', 'K_low']
        compdatl_table[to_int] = compdatl_table[to_int].fillna('0').astype(int, errors='ignore')
        if 0 in compdatl_table['I'].values or 0 in compdatl_table['J'].values:
            welspecl_table = extract_welspecl(schedule_dict)
            if 0 in compdatl_table['I'].values:
                compdatl_table['I'] = [compdatl_table['I'].iloc[r] if compdatl_table['I'].iloc[r] > 0 else _defaultIJ(compdatl_table['date'].iloc[r], compdatl_table['date'].iloc[r], 'I', welspecl_table) for r in len(compdatl_table)]
            if 0 in compdatl_table['J'].values:
                compdatl_table['J'] = [compdatl_table['I'].iloc[r] if compdatl_table['I'].iloc[r] > 0 else _defaultIJ(compdatl_table['date'].iloc[r], compdatl_table['date'].iloc[r], 'J', welspecl_table) for r in len(compdatl_table)]
        to_float = ['transimissibility factor', 'well bore diameter', 'Kh', 'skin', 'D-factor', 'pressure equivalent radius']
        compdatl_table[to_float] = compdatl_table[to_float].astype(float, errors='ignore')
        compdatl_table['status'] = compdatl_table['status'].fillna('OPEN').astype('category', errors='ignore')
        compdatl_table['skin'].fillna(0.0, inplace=True)
        compdatl_table['direction'] = compdatl_table['direction'].fillna('Z').astype('category', errors='ignore')
    return compdatl_table


def extract_compdatm(schedule_dict):
    """
    alias for extract_compdatl
    """
    return extract_compdatl(schedule_dict)


def extract_compdat2(schedule_dict):
    """
    Extract COMPDAT, COMPDATL and COMPDATM from the schedule dictionary and return a DataFrame of COMPDAT(s) data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    compdat = extract_compdat(schedule_dict)
    compdatl = extract_compdatl(schedule_dict)

    if len(compdat) > 0 and len(compdatl) > 0:
        return pd.concat([compdat, compdatl], axis=0, ignore_index=False)
    elif len(compdatl) > 0:
        return compdatl
    else:
        return compdat