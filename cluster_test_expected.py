
#!/opt/conda/bin/python

import os
os.environ["MODIN_IP"]="3.220.239.84"
os.environ["MODIN_CONNECTION"]='a920eaae0b0a2467c9ebb82a64b5cd75-277539115.us-east-1.elb.amazonaws.com'
os.environ["MODIN_ENGINE"]="Cloudburst"

import pandas as pd
import time
from cloudburst.client.client import CloudburstConnection

s3_path = "s3://modin-testdata/alc.csv"
s3_path = "s3://modin-testdata/onecol.csv"

start = time.time()

start = time.time()
df = pd.read_csv(s3_path)
end = time.time()

modin_duration = end - start
print("Time to read: {} seconds".format(round(modin_duration, 3)))
print(df)
print(df.to_csv())
