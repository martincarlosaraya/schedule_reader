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
    
    _len = [len(result_table[each]) for each in result_table]
    if len(_len) > 0 and max(_len) != min(_len):
        _len = max(_len)
        result_table = {each: result_table[each] + (['1*'] * (_len - len(result_table[each]))) for each in result_table}

    if record_names is not None:
        if len(record_names) > 0 and not str(record_names[0]).lower().startswith('date'):
            record_names = ['date'] + record_names
        result = pd.DataFrame(data=result_table).transpose()
        if len(result.columns) == 0:
            pass
        elif len(result.columns) >= len(record_names):
            record_names = record_names + [i for i in range(len(record_names), len(result.columns))]
            result.columns = record_names
        elif len(result.columns) < len(record_names):
            print(f"The last {len(record_names) - len(result.columns)} records were not present in the dataset.")
            result = pd.DataFrame(data=result_table).transpose()
            result.columns = record_names[:len(result.columns)]
            result.loc[:, record_names[len(result.columns):]] = None
    else:
        result = pd.DataFrame(data=result_table).transpose()
        record_names = ['date'] + [i for i in range(1, len(result.columns))]
        result.columns = record_names
    
    result[result.select_dtypes(object).columns] = result.select_dtypes(object)\
        .apply(lambda col : col.str.strip(""""'" """))\
        .replace('1*', np.nan)\
        .convert_dtypes(infer_objects=True, convert_string=False, 
                        convert_integer=True, convert_boolean=True, convert_floating=True)  # dtype_backend='numpy_nullable'
    return result