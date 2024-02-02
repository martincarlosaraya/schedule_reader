import pandas as pd
import numpy as np
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
            result_table[each] = [date] + (schedule_dict[each][keyword] 
                                           if type(schedule_dict[each][keyword]) is list 
                                           else [schedule_dict[each][keyword]])
    if record_names is not None:
        result = pd.DataFrame(data=result_table).transpose()
        if len(result.columns) == 0:
            pass
        elif len(result.columns) >= len(record_names):
            result = result.iloc[:, :len(record_names)]
            result.columns = record_names
        elif len(result_table.index) < len(record_names):
            print(f"The last {len(record_names) - len(result.columns)} records were not present in the dataset.")
            result = pd.DataFrame(data=result_table).transpose()
            result.columns = record_names[:len(result.columns)]
    else:
        result = pd.DataFrame(data=result_table).transpose().dropna(axis=0, how='all')
    
    
    result[result.select_dtypes(object).columns] = result.select_dtypes(object)\
        .apply(lambda col : col.str.strip(""""'" """))\
        .replace('1*', np.nan)\
        .convert_dtypes(infer_objects=True, convert_string=False, 
                        convert_integer=True, convert_boolean=True, convert_floating=True, dtype_backend='numpy_nullable')
    return result