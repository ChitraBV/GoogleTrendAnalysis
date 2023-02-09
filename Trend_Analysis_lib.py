import time

import matplotlib
import pandas as pd
import numpy as np
import os
from pathlib import Path

from IPython import get_ipython
from pytrends.request import TrendReq
import seaborn as sns
from datetime import date
import copy

import matplotlib.pyplot as plt



#Pretty print time elapsed

def pretty_time_delta(seconds):
    sign_string = '-' if seconds < 0 else ''
    seconds = abs((seconds))
    days, seconds = divmod(seconds, 86400)
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    if days > 0:
        return '%s%dd%dh%dm%ds' % (sign_string, days, hours, minutes, seconds)
    elif hours > 0:
        return '%s%dh%dm%ds' % (sign_string, hours, minutes, seconds)
    elif minutes > 0:
        return '%s%dm%ds' % (sign_string, minutes, seconds)
    else:
        if seconds < 1e-1:
            return '%s%dms' % (sign_string, seconds * 1000)
        else:
            return '%s%ds' % (sign_string, seconds)

# Read in Excel file and cache it in on disk.
# Read cache if it exists and is not older than the file.

def read_excel_cache(file_name, sheet_name='Sheet1', skipfooter=0):
    ##Time this function and print elapsed time to console.
    start_time = time.time()
    cache_file_name = Path(file_name).with_suffix('').name+'_'+sheet_name+'.pkl'
    time_file_name = Path(file_name).with_suffix('.time.txt')
    if (os.path.isfile(cache_file_name) and
        os.path.getmtime(cache_file_name) > os.path.getmtime(file_name)):
            print('Reading from cache: ' + cache_file_name)
            df = pd.read_pickle(cache_file_name)
            end_time = time.time()
            print('Elapsed time: ', pretty_time_delta(end_time - start_time))
            if os.path.isfile(time_file_name):
                print('Original reading time: ', open(time_file_name).read())
    else:
        print('Reading from file: ' + file_name)
        df = pd.read_excel(file_name, sheet_name=sheet_name,skipfooter=skipfooter)
        end_time = time.time()
        print('Elapsed time: ', pretty_time_delta(end_time - start_time))
        open(time_file_name, 'w').write(pretty_time_delta(end_time - start_time))
        # Save to cache
        df.to_pickle(cache_file_name)
        print('Elapsed time writing cache: ', pretty_time_delta(time.time() - end_time))
    return df