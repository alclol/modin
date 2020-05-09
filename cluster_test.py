
#!/opt/conda/bin/python

import os
os.environ["MODIN_IP"]="3.220.239.84"
os.environ["MODIN_CONNECTION"]='aaaf3e305282245549c6645fd64c886c-1218831264.us-east-1.elb.amazonaws.com'
os.environ["MODIN_ENGINE"]="Cloudburst"

import modin.pandas as pd
import pandas as old_pd
import time
from cloudburst.client.client import CloudburstConnection

# s3_path = "s3://modin-testdata/alc.csv"
s3_path = "s3://modin-testdata/onecol.csv"

start = time.time()

start = time.time()
modin_df = pd.read_csv(s3_path)
end = time.time()

modin_duration = end - start
print("Time to read with Modin: {} seconds".format(round(modin_duration, 3)))
print(modin_df)
