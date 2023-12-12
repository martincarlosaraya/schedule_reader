import pandas as pd
from datetime import datetime

def parse_dates(dates_keyword):
    """
    receives a string of date(s) or list of string(s) and attempt to parse it according to DATES eclipse format: DD 'MMM' YYYY HH:MM:SS 

    Parameters:
        dates_keyword: str or list of str

    Return:
        pandas.Series of dtype datetime64[ns]
    """

    months = {'JAN':  1,
              'FEB':  2,
              'MAR':  3,
              'APR':  4,
              'MAY':  5,
              'JUN':  6,
              'JLY':  7,
              'JUL':  7,
              'AUG':  8,
              'SEP':  9,
              'OCT': 10,
              'NOV': 11,
              'DEC': 12,
              }

    if type(dates_keyword) is str:
        if '\n' in dates_keyword:
            dates_keyword = dates_keyword.split('\n')
        else:
            dates_keyword = [dates_keyword]
        
    # removes 'DATES' keyword or ending slash '/' 
    dates_keyword = [each.strip('/ ').split() 
                     for each in dates_keyword 
                     if not each.strip().upper().startswith('DATES') and not each.strip().startswith('/')]

    # complete HH:MM:SS.SSSS in case some is incomplete

    # parse dates lines
    dates_keyword = [datetime(int(each[2]), months[each[1].strip("'").strip('"')], int(each[0]))
                     if len(each) == 3 else
                     datetime(int(each[2]), months[each[1].strip("'").strip('"')], int(each[0]),
                              int(each[3].split(':')[0]),
                              int(each[3].split(':')[1] if len(each[3].split(':')) >= 2 else 0),
                              float(each[3].split(':')[2] if len(each[3].split(':')) == 3 else 0.0)
                              ) 
                     for each in dates_keyword
                    ]
    
    return pd.to_datetime(dates_keyword).values
