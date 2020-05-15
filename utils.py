import time
import modin.pandas as pd
import pandas as opd
import numpy as np

def generate_dfs(row, col):
    df1 = pd.DataFrame(np.random.randint(0,1000,size=(row, col)), columns=list('ABCD'))
    df2 = pd.DataFrame(np.random.randint(0,1000,size=(row, col)), columns=list('ABCD'))
    return df1, df2

def generate_df(row, col):
    df1 = pd.DataFrame(np.random.randint(0,1000,size=(row, col)), columns=list('ABCD'))
    return df1

def generate_odfs(row, col):
    df1 = opd.DataFrame(np.random.randint(0,1000,size=(row, col)), columns=list('ABCD'))
    df2 = opd.DataFrame(np.random.randint(0,1000,size=(row, col)), columns=list('ABCD'))
    return df1, df2

def generate_odf(row, col):
    df1 = opd.DataFrame(np.random.randint(0,1000,size=(row, col)), columns=list('ABCD'))
    return df1

def timeit(func):
    def timed(*args, **kw):
        start = time.time()
        res = func(*args, **kw)
        end = time.time()
        print(f'   {(end-start):.7f}')
        return res

    return timed

