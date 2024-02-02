import pandas as pd
import numpy as np
from .dates import parse_dates
from .schedule_keywords import extract_keyword


def extract_wconprod(schedule_dict):
    """
    Shortcut for `extract_keyword` for the WCONPROD keyword.
    Extract the WCONPROD keyword from the schedule dictionary and return a DataFrame of WELSPECS data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    wconprod_columns = ['date', 'well', 'status', 'control mode', 'OIL rate', 'WATER rate', 'GAS rate', 'LIQUID rate', 'RESERVOIR fluid rate', 
                        'BHP limit', 'THP limit', 'VFP', 'ALQ',
                        'wet gas rate', 'total molar rate', 'steam rate',
                        'pressure offset', 'temperature offset', 'calorific target rate', 'linearly combined rate', 'NGL rate'] 
    wconprod_table = extract_keyword(schedule_dict, 'WCONPROD', wconprod_columns)  # {}
    if len(wconprod_table) > 0:
        wconprod_table['date'] = parse_dates(wconprod_table['date'].to_list())  # to parse dates exactly as stated by DATES eclipse format
        wconprod_table['well'] = [well.strip("'") for well in wconprod_table['well']]
        wconprod_table['well'] = wconprod_table['well'].astype('category')
        wconprod_table.replace('1*', np.nan, inplace=True)
        wconprod_table.replace("'1*'", np.nan, inplace=True)
    return wconprod_table


def extract_wconinje(schedule_dict):
    """
    Shortcut for `extract_keyword` for the WCONINJE keyword.
    Extract the WCONINJE keyword from the schedule dictionary and return a DataFrame of WELSPECS data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    wconinje_columns = ['date', 'well', 'injector type', 'status', 'control mode', 'SURFACE fluid rate', 'RESERVOIR fluid rate', 'BHP limit', 'THP limit', 'VFP',
                        'vap oil concentration', 'thermal ratio of gas to steam', 'OIL proportion', 'WATER proportion', 'GAS proportion', 'ratio of oil oil to steam'] 
    wconinje_table = extract_keyword(schedule_dict, 'WCONINJE', wconinje_columns)  # {}
    if len(wconinje_table) > 0:
        wconinje_table['date'] = parse_dates(wconinje_table['date'].to_list())  # to parse dates exactly as stated by DATES eclipse format
        wconinje_table['well'] = [well.strip("'") for well in wconinje_table['well']]
        wconinje_table['well'] = wconinje_table['well'].astype('category')
        wconinje_table.replace('1*', np.nan, inplace=True)
        wconinje_table.replace("'1*'", np.nan, inplace=True)
    return wconinje_table


def extract_wconhist(schedule_dict):
    """
    Shortcut for `extract_keyword` for the WCONHIST keyword.
    Extract the WCONHIST keyword from the schedule dictionary and return a DataFrame of WELSPECS data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    wconhist_columns = ['date', 'well', 'status', 'control mode', 'OIL rate', 'WATER rate', 'GAS rate', 'VFP', 'ALQ',
                        'THP limit', 'BHP limit', 'wet gas rate', 'NGL rate']
    wconhist_table = extract_keyword(schedule_dict, 'WCONHIST', wconhist_columns)  # {}
    if len(wconhist_table) > 0:
        wconhist_table['date'] = parse_dates(wconhist_table['date'].to_list())  # to parse dates exactly as stated by DATES eclipse format
        wconhist_table['well'] = [well.strip("'") for well in wconhist_table['well']]
        wconhist_table['well'] = wconhist_table['well'].astype('category')
        wconhist_table.replace('1*', np.nan, inplace=True)
        wconhist_table.replace("'1*'", np.nan, inplace=True)
    return wconhist_table


def extract_wconinjh(schedule_dict):
    """
    Shortcut for `extract_keyword` for the WCONINJE keyword.
    Extract the WCONINJE keyword from the schedule dictionary and return a DataFrame of WELSPECS data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    wconinjh_columns = ['date', 'well', 'injector type', 'status', 'injection rate', 'BHP', 'THP', 'VFP',
                        'vap oil concentration', 'OIL proportion', 'WATER proportion', 'GAS proportion', 'control model']
    wconinjh_table = extract_keyword(schedule_dict, 'WCONINJH', wconinjh_columns)  # {}
    if len(wconinjh_table) > 0:
        wconinjh_table['date'] = parse_dates(wconinjh_table['date'].to_list())  # to parse dates exactly as stated by DATES eclipse format
        wconinjh_table['well'] = [well.strip("'") for well in wconinjh_table['well']]
        wconinjh_table['well'] = wconinjh_table['well'].astype('category')
        wconinjh_table.replace('1*', np.nan, inplace=True)
        wconinjh_table.replace("'1*'", np.nan, inplace=True)
    return wconinjh_table
