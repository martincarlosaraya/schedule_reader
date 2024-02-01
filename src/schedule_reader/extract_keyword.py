import pandas as pd
from .dates import parse_dates

def extract_keyword(schedule_dict, keyword: str=None, record_names=None): 
    """
    from the provided schedule dictionay `schedule_dict` extract the desired `keyword`, create a DataFrame and set the column names as the `record_names` provided (optional).

    Params:
        schedule_dict: dict
            shedule dictionary prepared by the .data_reader.read_data function
        keyword: str
            the desired keyword to be extracted
        record_names: list of str
            a list with the name of the record names for the `keyword`
    
    Return:
        pandas.DataFrame
    """
    result_table = {}

    # extract only the dates, all the dates
    if keyword == 'DATES':
        result_table = [schedule_dict[each]['DATES'] for each in schedule_dict if 'DATES' in schedule_dict[each]]
        return pd.Series(parse_dates(result_table), name='DATES')

    # look for especified keyword, only keep the last previous date
    for each in schedule_dict:
        if 'DATES' in schedule_dict[each]:
            date = schedule_dict[each]['DATES']
        elif keyword in schedule_dict[each]:
            result_table[each] = [date] + schedule_dict[each][keyword]
    if record_names is None:
        return pd.DataFrame(data=result_table).transpose().dropna(axis=0, how='all')
    else:
        result = pd.DataFrame(data=result_table).transpose().iloc[:, :len(record_names)]
        result.columns = record_names
        return result