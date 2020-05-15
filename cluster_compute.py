import os, time
from utils import *
import pandas as opd
import modin.pandas as pd

def compare_mul(i):
    print(f"Dataframe size: {i} x 4")

    df1 = generate_df(i, 4)
    odf1 = generate_odf(i, 4)

    print("Modin: ")
    cloud_res = modin_mul(df1)
    modin_mul(df1)
    print("Naive Pandas: ")
    local = pandas_mul(odf1)
    pandas_mul(odf1)

    print(cloud_res._to_pandas().equals(local))

@timeit
def modin_mul(df1):
    res = df1[['A']].multiply(df1['A'], axis='index')
    return res

@timeit
def pandas_mul(df1):
    return df1[['A']].multiply(df1['A'], axis='index')

print("Compare mul operation performance: ")
for i in [500, 5000]:
# for i in [50000, 500000, 5000000, 50000000]:
    compare_mul(i)

