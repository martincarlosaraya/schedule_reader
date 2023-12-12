import pandas as pd

def read_data(filepath:str, *, paths={}, folder=None, i=0, encoding='cp1252', verbose=False):
    """
    reads the .DATA file, look for schedule section and returns a dictionary of keywords and its records on order of appereance.

    Params:
        filepath: str
            the path to the .DATA or schedule include file
        paths: dict {str: str}, optional
            dictionary of the paths described by PATHS keyword. If the .DATA is provided this data is automatically extracted.
        folder: str, optional
            tha absolute path to the folder where the .DATA file is located. If the .DATA is provided this data is automatically extracted.
        i: int, should not be provided by the user!
            internal counter provided by the same funcion recursive calls when reading include files.
        encoding: str
            The enconding format of input text files. For files with especial characters, it might be convenient to use 'cp1252' or 'latin1'.
        verbose: bool
            set it to False to skip printing messages.

    Return:
        dict of dicts of keywords and their records
            {i: {keyword: [records]}}
    """

    filepath = filepath.replace('\\', '/')
    if folder is None:
        folder = '/'.join(filepath.split('/')[:-1]) + '/'
    if verbose is None:
        print('reading file:', filepath)
        verbose = False
    elif verbose is True:
        print('reading file:', filepath)
    
    with open(filepath, 'r', encoding=encoding) as f:
        datafile = f.readlines()
    datafile = [line.strip() for line in datafile]

    start_date = None
    if filepath.upper().endswith('.DATA'):
        if 'START' in datafile:
            start_date = datafile[datafile.index('START') + 1].replace('/', '').strip()

        if 'PATHS' in datafile:
            line = datafile.index('PATHS') + 1
            while not datafile[line].strip().startswith('/'):
                paths.update({datafile[line].strip().strip('/').split()[0].strip("'"): datafile[line].strip().strip('/').split()[1].strip("'")})
                line += 1
            if verbose:
                print('found PATHS keyword:\n', "\n   ".join([k + ":" + v for k, v in paths.items()]))

        schedule_line = None
        if 'SCHEDULE' in datafile:
            schedule_line = datafile.index('SCHEDULE')
        else:
            schedule_line = [line.split()[0].upper().startswith('SCHEDULE') if len(line) > 0 else False for line in datafile]
            schedule_line = schedule_line.index(True) if True in schedule_line else None
        if schedule_line is None:
            schedule_line = 0  # read the entire file
            # raise ValueError("'SCHEDULE' keyword not found in this DATA file.")
    else:
        schedule_line = 0
    
    if start_date is None:
        extracted = {}
    else:
        extracted = {i: {'DATES': start_date}}
        i += 1
    line = schedule_line
    while line < len(datafile):
        if datafile[line].upper().startswith('DATES'):
            line += 1
            # last_date = None
            while datafile[line].split()[0] != '/':
                if len(datafile[line].strip()) > 0 and not datafile[line].strip().startswith('--'):
                    # last_date = line
                    extracted[i] = {'DATES': datafile[line].replace('/', '').strip()}
                    i += 1
                line += 1
            # if last_date is None:
            #    raise ValueError("error format in keyword DATES in line " + line + 1 + " in file " + filepath)
            # extracted[i] = {'DATES': datafile[line - 1].replace('/', '').strip()}
            # i += 1
            # line += 1

        elif datafile[line].upper().startswith('COMPDAT'):
            # keyword = None
            line += 1
            while datafile[line].split()[0] != '/':
                if not datafile[line].strip().startswith('--'):
                    if '/' not in datafile[line]:
                        raise ValueError("error format in keyword COMPDAT in line " + line + 1 + " in file " + filepath)
                    compdat_line = datafile[line][:datafile[line].index('/')].replace('/', '').split()
                    if len(compdat_line) < 14:
                        compdat_line_expanded = []
                        for each in compdat_line:
                            if len(each) >= 2 and each.endswith('*') and each[:-1].isdigit():
                                compdat_line_expanded = compdat_line_expanded + (['1*'] * int(each[:-1]))
                            else:
                                compdat_line_expanded.append(each)
                        compdat_line_expanded = compdat_line_expanded + (['1*'] * (14 - len(compdat_line_expanded)))
                        compdat_line = compdat_line_expanded
                    extracted[i] = {'COMPDAT': compdat_line}
                    i += 1
                line += 1
            line += 1
        
        elif datafile[line].upper().startswith('WELSPECS'):
            # keyword = None
            line += 1
            while datafile[line].split()[0] != '/':
                if not datafile[line].strip().startswith('--'):
                    if '/' not in datafile[line]:
                        raise ValueError("error format in keyword WELSPECS in line " + line + 1 + " in file " + filepath)
                    welspecs_line = datafile[line][:datafile[line].index('/')].replace('/', '').split()
                    if len(welspecs_line) < 17:
                        welspecs_line_expanded = []
                        for each in welspecs_line:
                            if len(each) >= 2 and each.endswith('*') and each[:-1].isdigit():
                                welspecs_line_expanded = welspecs_line_expanded + (['1*'] * int(each[:-1]))
                            else:
                                welspecs_line_expanded.append(each)
                        welspecs_line_expanded = welspecs_line_expanded + (['1*'] * (17 - len(welspecs_line_expanded)))
                        welspecs_line = welspecs_line_expanded
                    extracted[i] = {'WELSPECS': welspecs_line}
                    i += 1
                line += 1
            line += 1

        elif datafile[line].upper().startswith('INCLUDE'):
            # keyword = None
            line += 1
            include = datafile[line][::-1][datafile[line][::-1].index('/') + 1:][::-1].strip().strip("'")
            if '$' in include:
                path_i = include.index('$')
                path_f = include.index('/', path_i)
                path_var = include[path_i: path_f]
                if path_var[1:] not in paths:
                    raise ValueError("path variable '" + path_var + "' not defined in keyword PATHS.")
                include = folder + include[:path_i] + paths[path_var[1:]] + include[path_f:]
            elif include.startswith('../') or include.startswith('./'):
                include = folder + include
            include = read_data(include, i=i, paths=paths, folder=folder)
            extracted.update(include)
            line += 1
        
        elif len(datafile[line].strip()) == 0 or datafile[line].upper().startswith('--'):
            line += 1

        else:
            line += 1

        # else:
        #     keyword = datafile[line].split()[0]
        #     line += 1
        #    while not datafile[line].strip().startswith('/'):
        #        print(datafile[line])
        #        if len(datafile[line].split()) > 0 and not datafile[line].startswith('--'):
        #            if '/' in datafile[line]:
        #                keyword_line = datafile[line][:datafile[line].index('/')].replace('/', '').split()
        #                if True in ['*' in each for each in keyword_line]:
        #                     keyword_line_expanded = []
        #                     for each in keyword_line:
        #                         if len(each) >= 2 and each.endswith('*') and each[:-1].isdigit():
        #                             keyword_line_expanded = keyword_line_expanded + (['1*'] * int(each[:-1]))
        #                         else:
        #                             keyword_line_expanded.append(each)
        #                     keyword_line_expanded = keyword_line_expanded + ([None] * (100 - len(keyword_line_expanded)))
        #                     keyword_line = keyword_line_expanded
        #                 extracted[i] = {keyword: keyword_line}
        #                 i += 1
        #             elif len(datafile[line].strip()) == 0:
        #                 line += 1
        #             else:  # '/' not in datafile[line] and len(datafile[line].strip()) > 0:
        #                 extracted[i] = {keyword: ''}
        #                 i += 1
        #                 # keyword = datafile[line].split()[0]
        #                 # line += 1
        #                 break
        #         line += 1
        #     line += 1

    return extracted
