#!/opt/conda/bin/python

import os, time
os.environ["MODIN_IP"]="3.91.91.212"
os.environ["MODIN_CONNECTION"]="a257bcae8494042b595a651bbfd5c8fe-1212680712.us-east-1.elb.amazonaws.com"
os.environ["MODIN_ENGINE"]="Cloudburst"
import modin.pandas as pd
import pandas as opd
import numpy as np

def generate_dfs(row, col):
    df1 = pd.DataFrame(np.random.randint(0,1000,size=(row, col)), columns=list('ABCD'))
    df2 = pd.DataFrame(np.random.randint(0,1000,size=(row, col)), columns=list('ABCD'))
#    df = pandas.DataFrame(
#        {
#            "col1": [0, 1, 2, 3],
#            "col2": [4, 5, 6, 7],
#            "col3": [8, 9, 10, 11],
#            "col4": [12, 13, 14, 15],
#            "col5": [0, 0, 0, 0],
#        }
#    )
#
#    df2 = pandas.DataFrame(
#        {
#            "col1": [0, 1, 2, 3],
#            "col2": [4, 5, 6, 7],
#            "col3": [8, 9, 10, 11],
#            "col6": [12, 13, 14, 15],
#            "col7": [0, 0, 0, 0],
#        }
#    )
    return df1, df2

def generate_odfs(row, col):
    df1 = opd.DataFrame(np.random.randint(0,1000,size=(row, col)), columns=list('ABCD'))
    df2 = opd.DataFrame(np.random.randint(0,1000,size=(row, col)), columns=list('ABCD'))
    return df1, df2


print("Compare concat operation performance: ")
for i in [500, 5000, 50000, 500000, 5000000, 50000000, 500000000]:
    print(f"Dataframe size: {i} x 4")

    df1, df2 = generate_dfs(i, 4)
    odf1, odf2 = generate_odfs(i, 4)

#frame_data = np.random.randint(0, 100, size=(2**10, 2**6))
#df = pd.DataFrame(frame_data).add_prefix("col")

    start = time.time()
    res = pd.concat([df1, df2])
    end = time.time()
    print(f'modin spent = {end-start} seconds')

    start = time.time()
    res = opd.concat([odf1, odf2])
    end = time.time()
    print(f'old pandas spent = {end-start} seconds')

