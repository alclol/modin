
#!/opt/conda/bin/python

import os
os.environ["MODIN_IP"]="3.91.91.212"
os.environ["MODIN_CONNECTION"]='a257bcae8494042b595a651bbfd5c8fe-1212680712.us-east-1.elb.amazonaws.com'
os.environ["MODIN_ENGINE"]="Cloudburst"

import modin.pandas as pd
import pandas as old_pd
import time
from cloudburst.client.client import CloudburstConnection

s3_path = "s3://modin-testdata/username.csv"
# s3_path = "s3://modin-testdata/onecol.csv"

start = time.time()

start = time.time()
modin_df = pd.read_csv(s3_path)
end = time.time()

modin_duration = end - start
print("Time to read with Modin: {} seconds".format(round(modin_duration, 3)))

s3_path = "s3://modin-testdata/country.csv"
start = time.time()
modin_df = pd.read_csv(s3_path)
end = time.time()

modin_duration = end - start
print("Time to read with Modin: {} seconds".format(round(modin_duration, 3)))

