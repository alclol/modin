#!/opt/conda/bin/python

import os
os.environ["MODIN_IP"]="127.0.0.1"
os.environ["MODIN_CONNECTION"]="127.0.0.1"
os.environ["MODIN_ENGINE"]="Cloudburst"
import modin.pandas as pd

df = pd.read_csv(os.getcwd() + "/test_files/file.csv")
print(df)
print(df.isna())

