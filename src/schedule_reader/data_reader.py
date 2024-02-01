import pandas as pd
from .counter import Counter
from os.path import exists

def read_data(filepath:str, *, paths: dict={}, folder: str=None, encoding: str='cp1252', verbose: bool=False, counter: Counter=None):
    """
    reads the .DATA file, look for schedule section and returns a dictionary of keywords and its records on order of appereance.

    Params:
        filepath: str
            the path to the .DATA or schedule include file
        paths: dict {str: str}, optional
            dictionary of the paths described by PATHS keyword. If the .DATA is provided this data is automatically extracted.
        folder: str, optional
            tha absolute path to the folder where the .DATA file is located. If the .DATA is provided this data is automatically extracted.
        encoding: str
            The enconding format of input text files. For files with especial characters, it might be convenient to use 'cp1252' or 'latin1'.
        verbose: bool
            set it to False to skip printing messages.
        counter: an instance of the Counter class, should not be provided by the user!
            internal counter provided by the same funcion recursive calls when reading include files.

    Return:
        dict of dicts of keywords and their records
            {i: {keyword: [records]}}
    """
    def _keyword_end():
        return datafile[line].strip().startswith('/')
    def _comment_line():
        return datafile[line].strip().startswith('--')
    def _empty_line():
        return len(datafile[line].strip()) == 0
    def _line_data():
        if '/' in  datafile[line]:
            _cut = datafile[line].index('/')
        elif '--' in datafile[line]:
            _cut = datafile[line].index('--')
        else:
            _cut = len(datafile[line])
        return datafile[line][:_cut].strip()
    skip0_keywords = ('ECHO', 'NOECHO', 'SKIPREST', 'SKIP', 'SKIP100', 'SKIP300', 'ENDSKIP', 'RPTONLY', 'RPTONLYO')
    skip1_keywords = ('NEXT', 'NEXTSTEP', 'LIFTOPT', 'GCONTOL', 'GUIDERAT', 'WLIMTOL')
    skip3_keywords = ('TUNING')
        

    # check file exists
    if not exists(filepath):
        raise ValueError(f"The file doesn't exists: {filepath}")
    filepath = filepath.replace('\\', '/')
    if folder is None:
        folder = '/'.join(filepath.split('/')[:-1]) + '/'

    # clean verbose parameter
    if verbose is None:
        verbose = True
    else:
        verbose = bool(verbose)
    
    # initialize the counter
    if counter is None:
        counter = Counter()
    print(f"{str(counter)} keywords until now")

    # read and clean the main file
    if verbose:
        print('reading file:', filepath)
    with open(filepath, 'r', encoding=encoding) as f:
        datafile = f.readlines()
    datafile = [line.strip() for line in datafile]

    # initialize start_date variable, will be populated if START keyword is found
    start_date, found_START = None, False

    # if the file is the .DATA, look for START and PATHS keywords
    if filepath.upper().endswith('.DATA'):
        
        # looks for START
        if 'START' in datafile:
            start_date = datafile[datafile.index('START') + 1].replace('/', '').strip()
            found_START = True
            if verbose:
                print(f"Found START date: {start_date}")

        # looks for PATHS and update dictionary if PATHS found
        if 'PATHS' in datafile:
            line = datafile.index('PATHS') + 1
            while not datafile[line].strip().startswith('/'):
                paths.update({datafile[line].strip().strip('/').split()[0].strip("'"): datafile[line].strip().strip('/').split()[1].strip("'")})
                line += 1
            if verbose:
                print('Found PATHS keyword:\n', "\n   ".join([k + ":" + v for k, v in paths.items()]))

        # jumpt to SCHEDULE keyword line
        schedule_line = None
        if 'SCHEDULE' in datafile:
            schedule_line = datafile.index('SCHEDULE')
        else:
            schedule_line = [line.split()[0].upper().startswith('SCHEDULE') if len(line) > 0 else False for line in datafile]
            schedule_line = schedule_line.index(True) if True in schedule_line else None
        if schedule_line is None:
            schedule_line = 0  # read the entire file
            # raise ValueError("'SCHEDULE' keyword not found in this DATA file.")
        if verbose:
            if schedule_line == 0:
                print(f"SCHEDULE keyword not found in this DATA, will proceed to read everything line by line... it could take some time...")
            else:
                print(f"found SCHEDULE keyword in line {schedule_line}")
    else:
        schedule_line = 0
    
    # intialize the extracted dictionary, where every read keyword will be stored
    if not found_START:
        # empty dictionary, START date by default and can be updated at the end of the loop
        extracted = {counter(): {'DATES': '01 JAN 1900'}}
        if verbose:
            print(f"START keyword not found, will start dates from default value '01 JAN 1900'")
    else:
        # START date is the first keyword in the dictionary
        extracted = {counter(): {'DATES': start_date}}

    
    # start reading the file, from the schedule_line if found
    line = schedule_line
    skip_ = False
    while line < len(datafile):  # read every line until the end


        # skip lines as indicated by SKIP keywords
        if skip_ and not datafile[line].upper().startswith('ENDSKIP'):
            line += 1
        elif skip_ and datafile[line].upper().startswith('ENDSKIP'):
            line += 1
            skip_ = False


        # skip empty lines
        if _empty_line() or _comment_line():
            line += 1


        # if a DATES is found
        elif datafile[line].upper().startswith('DATES'):
            line += 1
            if verbose:
                print("found DATES keyword")
                _counter0 = counter.curr()

            # read all the dates within DATES until the closing /
            while not _keyword_end():  # datafile[line].split()[0] != '/':
                # skip empty and commented lines
                if not _empty_line() and not _comment_line():
                    extracted[counter()] = {'DATES': _line_data()}  # datafile[line].replace('/', '').strip()}
                line += 1
            if verbose:
                print(f" {' until '.join(set([extracted[_counter0], extracted[counter.curr()]]))}")


        # if COMPDAT is found
        elif datafile[line].upper().startswith('COMPDAT'):
            line += 1
            if verbose:
                print("found COMPDAT keyword")
                _counter0 = counter.curr()

            # read all the COMPDAT lines until the closing /
            while not _keyword_end():
                if not _empty_line() and not _comment_line():
                    if '/' not in datafile[line]:
                        raise ValueError(f"Error format in keyword COMPDAT in line {line + 1} in file {filepath}. Missing / at the end of the line.")
                    compdat_line = _line_data()  # datafile[line][:datafile[line].index('/')].replace('/', '').split()
                    
                    # complete default values at the end if requered
                    if len(compdat_line) < 14:
                        compdat_line_expanded = []
                        for each in compdat_line:
                            if len(each) >= 2 and each.endswith('*') and each[:-1].isdigit():
                                compdat_line_expanded = compdat_line_expanded + (['1*'] * int(each[:-1]))
                            else:
                                compdat_line_expanded.append(each)
                        compdat_line_expanded = compdat_line_expanded + (['1*'] * (14 - len(compdat_line_expanded)))
                        compdat_line = compdat_line_expanded
                    extracted[counter()] = {'COMPDAT': compdat_line}
                line += 1
            line += 1
            if verbose:
                print(f" for wells: {', '.join(set([extracted[i_][0] for i_ in range(_counter0, counter.curr()+1)]))}")


        # if WELSPECS is found
        elif datafile[line].upper().startswith('WELSPECS'):
            line += 1
            if verbose:
                print("found WELSPECS keyword")
                _counter0 = counter.curr()

            while not _keyword_end():
                if not _empty_line() and not _comment_line():
                    if '/' not in datafile[line]:
                        raise ValueError(f"Error format in keyword WELSPECS in line {line + 1} in file {filepath}. Missing / at the end of the line.")
                    welspecs_line = _line_data().split()  # datafile[line][:datafile[line].index('/')].replace('/', '').split()
                    
                    # complete default values at the end if requered
                    if len(welspecs_line) < 17:
                        welspecs_line_expanded = []
                        for each in welspecs_line:
                            if len(each) >= 2 and each.endswith('*') and each[:-1].isdigit():
                                welspecs_line_expanded = welspecs_line_expanded + (['1*'] * int(each[:-1]))
                            else:
                                welspecs_line_expanded.append(each)
                        welspecs_line_expanded = welspecs_line_expanded + (['1*'] * (17 - len(welspecs_line_expanded)))
                        welspecs_line = welspecs_line_expanded
                    extracted[counter()] = {'WELSPECS': welspecs_line}
                line += 1
            line += 1
            if verbose:
                print(f" for wells: {', '.join(set([extracted[i_][0] for i_ in range(_counter0, counter.curr()+1)]))}")


        # if INCLUDE is found, will read the include
        elif datafile[line].upper().startswith('INCLUDE'):
            line += 1

            include = datafile[line][::-1][datafile[line][::-1].index('/') + 1:][::-1].strip().strip("'")
            
            if '$' in include:  # identify path from PATHS dictionary
                path_i = include.index('$')
                path_f = include.index('/', path_i)
                path_var = include[path_i: path_f]
                if path_var[1:] not in paths:
                    raise ValueError(f"Path variable '{path_var}' not defined in keyword PATHS.")
                include = folder + include[:path_i] + paths[path_var[1:]] + include[path_f:]
            elif include.startswith('../') or include.startswith('./'):
                include = folder + include
            include = read_data(include, paths=paths, folder=folder, counter=counter)
            extracted.update(include)
            line += 1


        # read the listed keywords, that doesn't have and ending line with /
        elif datafile[line].split()[0].upper() in skip0_keywords:
            keyword_ = datafile[line].split()[0].upper()
            extracted[counter()] = {keyword_: None}
            if verbose:
                print(f"found {keyword_} keyword")
            line += 1
        elif datafile[line].split()[0].upper() in skip1_keywords:
            keyword_ = datafile[line].split()[0].upper()
            if verbose:
                print(f"found {keyword_} keyword")
            line += 1
            extracted[counter()] = {keyword_: datafile[line].split()[0].upper()}
            line += 1
        elif datafile[line].split()[0].upper() in skip3_keywords:
            keyword_ = datafile[line].split()[0].upper()
            if verbose:
                print(f"found {keyword_} keyword")
            line += 1
            for i in range(3):
                extracted[counter()] = {keyword_: datafile[line].split()[0].upper()}
                line += 1


        # generic procedure to read any other COMPLETION, WELL, GROUP or USER DEFINED keyword (because they end with /)
        elif datafile[line].split()[0].upper()[0] in 'CWGU':
            keyword_ = datafile[line].split()[0].upper()
            line += 1
            if verbose:
                print(f"found {keyword_} keyword")
                _counter0 = counter.curr()

            while not _keyword_end():
                if not _empty_line() and not _comment_line():
                    keyword_line = _line_data().split()
                    extracted[counter()] = {keyword_: keyword_line}
                line += 1
            line += 1
            if verbose:
                print(f" for: {', '.join(set([extracted[i_][0] for i_ in range(_counter0, counter.curr()+1)]))}")


        # skip everything else
        else:
            line += 1

        if verbose:
            print(f"closing this file, {str(counter)} keywords until now")

    return extracted
