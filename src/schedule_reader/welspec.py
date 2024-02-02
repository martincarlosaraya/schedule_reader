import pandas as pd
import numpy as np
from .dates import parse_dates
from .schedule_keywords import extract_keyword

def extract_welspecs(schedule_dict):
    """
    Shortcut for `extract_keyword` for the WELSPECS keyword.
    Extract the WELSPECS keyword from the schedule dictionary and return a DataFrame of WELSPECS data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    welspecs_columns = ['date', 'well', 'group', 'I', 'J', 'reference depth', 'preferred phase', 'drainage radius', 'inflow equation', 'automatic shut-in', 'crossflow', 'pressure table', 'density calculation', 'FIP region', '_reserved1', '_reserved2', 'well model', 'polymer']
    welspecs_table = extract_keyword(schedule_dict, 'WELSPECS', welspecs_columns)  # {}
    if len(welspecs_table) > 0:
        welspecs_table['date'] = parse_dates(welspecs_table['date'].to_list())  # to parse dates exactly as stated by DATES eclipse format
        welspecs_table['well'] = [well.strip("'") for well in welspecs_table['well']]
        welspecs_table['well'] = welspecs_table['well'].astype('category')
        welspecs_table.replace('1*', np.nan, inplace=True)
        welspecs_table.replace("'1*'", np.nan, inplace=True)
        welspecs_table[['I', 'J']] = welspecs_table[['I', 'J']].astype(int)
    return welspecs_table


def extract_welspecl(schedule_dict):
    """
    Shortcut for `extract_keyword` for the WELSPECL keyword.
    Extract the WELSPECL keyword from the schedule dictionary and return a DataFrame of WELSPECL data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    welspecl_columns = ['date', 'well', 'group', 'local grid', 'I', 'J', 'reference depth', 'preferred phase', 'drainage radius', 'inflow equation', 'automatic shut-in', 'crossflow', 'pressure table', 'density calculation', 'FIP region', '_reserved1', '_reserved2', 'well model', 'polymer']
    welspecl_table = extract_keyword(schedule_dict, 'WELSPECL', welspecl_columns)  # {}
    if len(welspecl_table) > 0:
        welspecl_table['date'] = parse_dates(welspecl_table['date'].to_list())  # to parse dates exactly as stated by DATES eclipse format
        welspecl_table['well'] = [well.strip("'") for well in welspecl_table['well']]
        welspecl_table['well'] = welspecl_table['well'].astype('category')
        welspecl_table.replace('1*', np.nan, inplace=True)
        welspecl_table.replace("'1*'", np.nan, inplace=True)
        welspecl_table[['I', 'J']] = welspecl_table[['I', 'J']].astype(int)
    return welspecl_table


def extract_wellspec(schedule_dict):
    """
    Shortcut for `extract_keyword` for the WELLSPEC keyword.
    Extract the WELLSPEC keyword from the schedule dictionary and return a DataFrame of WELLSPEC data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    wellspec_columns = ['date', 'well', 'group', 'I', 'J', 'reference depth', 'separator name', 'FIP region']
    wellspec_table = extract_keyword(schedule_dict, 'WELLSPEC', wellspec_columns)  # {}
    if len(wellspec_table) > 0:
        wellspec_table['date'] = parse_dates(wellspec_table['date'].to_list())  # to parse dates exactly as stated by DATES eclipse format
        wellspec_table['well'] = [well.strip("'") for well in wellspec_table['well']]
        wellspec_table['well'] = wellspec_table['well'].astype('category')
        wellspec_table.replace('1*', np.nan, inplace=True)
        wellspec_table.replace("'1*'", np.nan, inplace=True)
        wellspec_table[['I', 'J']] = wellspec_table[['I', 'J']].astype(int)
    return wellspec_table


def extract_welspec2(schedule_dict):
    """
    Extract WELSPECS, WELSPECL and WELLSPEC from the schedule dictionary and return a DataFrame of COMPDAT(s) data by DATES.

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
    
    Return:
        pandas.DataFrame
    """
    welspecs = extract_welspecs(schedule_dict)
    welspecl = extract_welspecl(schedule_dict)
    wellspec = extract_wellspec(schedule_dict)

    welspec2 = [welspecs, welspecl, wellspec]
    welspec2 = [ws for ws in welspec2 if len(ws) > 0]

    if len(welspec2) > 1:
        return pd.concat(welspec2, axis=0, ignore_index=False)
    elif len(welspec2) == 1:
        return welspec2[0]
    else:
        return welspecs