import os, time
from utils import timeit, generate_dfs, generate_odfs
import pandas as opd
import modin.pandas as pd

def compare_concat(i):
    print(f"Dataframe size: {i} x 4")

    df1, df2 = generate_dfs(i, 4)
    odf1, odf2 = generate_odfs(i, 4)

    print("Modin: ")
    modin_concat(df1, df2)
    modin_concat(df1, df2)
    modin_concat(df1, df2)
    print("Naive Pandas: ")
    pandas_concat(odf1, odf2)
    pandas_concat(odf1, odf2)
    pandas_concat(odf1, odf2)

@timeit
def modin_concat(df1, df2):
    pd.concat([df1, df2])

@timeit
def pandas_concat(df1, df2):
    opd.concat([df1, df2])

print("Compare concat operation performance: ")
for i in [50000, 500000, 5000000, 50000000]:
    compare_concat(i)

