import os, time
from utils import *
import pandas as opd
import modin.pandas as mpd

def compare(i):
    print(f"Dataframe size: {i} x 4")

    df= generate_df(i, 4)

    print("Modin: ")
    modin_func(df)

    df = df._to_pandas()

    print("Naive Pandas: ")
    pandas_func(df)


@timeit
def modin_func(df):
    df.join(df, lsuffix='_left', rsuffix='_right')

@timeit
def pandas_func(df):
    df.join(df, lsuffix='_left', rsuffix='_right')

print("Concat performance: ")
for i in [50000, 500000, 5000000, 50000000]:
    compare(i)
