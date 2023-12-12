import pandas as pd
from .dates import parse_dates
from .extract_keyword import extract_keyword

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
    welspecs_columns = ['date', 'well', 'I', 'J', 'reference depth', 'preferred phase', 'drainage radius', 'inflow equation', 'automatic shut-in', 'crossflow', 'pressure table', 'density calculation', 'FIP region', '_reserved1', '_reserved2', 'well model', 'polymer']
    welspecs_table = extract_keyword(schedule_dict, 'WELSPECS', welspecs_columns)  # {}
    welspecs_table['date'] = parse_dates(welspecs_table['date'].to_list())  # to parse dates exactly as stated by DATES eclipse format
    welspecs_table['well'] = [well.strip("'") for well in welspecs_table['well']]
    welspecs_table['well'] = welspecs_table['well'].astype('category')
    welspecs_table.replace('1*', None, inplace=True)
    welspecs_table.replace("'1*'", None, inplace=True)
    welspecs_table[['I', 'J']] = welspecs_table[['I', 'J']].astype(int)
    return welspecs_table
