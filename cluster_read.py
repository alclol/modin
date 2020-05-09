
#!/opt/conda/bin/python

import os
os.environ["MODIN_IP"]="3.220.239.84"
os.environ["MODIN_CONNECTION"]='a78011eebf0be41d3b94b96000a33320-1322524692.us-east-1.elb.amazonaws.com'
os.environ["MODIN_ENGINE"]="Cloudburst"

import modin.pandas as pd
import pandas as old_pd
import time
from cloudburst.client.client import CloudburstConnection

# s3_path = "s3://dask-data/nyc-taxi/2015/yellow_tripdata_2015-01.csv"
# s3_path = "S3://ryft-public-sample-data/case.csv"
s3_path = "s3://modin-testdata/alc.csv"

start = time.time()

# pandas_df = old_pd.read_csv(s3_path, parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"])
# end = time.time()
# pandas_duration = end - start
# print("Time to read with pandas: {} seconds".format(round(pandas_duration, 3)))

start = time.time()
# modin_df = pd.read_csv(os.getcwd() + "/test_files/file.csv")
# modin_df = pd.read_csv(s3_path, parse_dates=["tpep_pickup_datetime", "tpep_dropoff_datetime"])
modin_df = pd.read_csv(s3_path)
end = time.time()

modin_duration = end - start
print("Time to read with Modin: {} seconds".format(round(modin_duration, 3)))

pandas_df = modin_df

###########################################pandas map op########################################
start = time.time()
pandas_isnull = pandas_df.isnull()
pandas_isnull.tail()
end = time.time()
pandas_duration = end - start
print("Time to isnull with pandas: {} seconds".format(round(pandas_duration, 3)))

###########################################m-cb map op########################################
start = time.time()

modin_isnull = modin_df.isnull()
modin_isnull.tail()

end = time.time()
modin_duration = end - start
print("Time to isnull with Modin: {} seconds".format(round(modin_duration, 3)))

start = time.time()

pandas_groupby = pandas_df.groupby(by="passenger_count").count()
pandas_groupby.tail()

end = time.time()
pandas_duration = end - start

print("Time to groupby with pandas: {} seconds".format(round(pandas_duration, 3)))
start = time.time()

modin_groupby = modin_df.groupby(by="passenger_count").count()
modin_groupby.tail()

end = time.time()
modin_duration = end - start
print("Time to groupby with Modin: {} seconds".format(round(modin_duration, 3)))

# printmd("### Modin is {}x faster than pandas at `groupby`!".format(round(pandas_duration / modin_duration, 2)))

# print("### Modin is {}x faster than pandas at `isnull`!".format(round(pandas_duration / modin_duration, 2)))
# df = pd.read_csv(os.getcwd() + "/test_files/file.csv")
# print(df)
# print(df.isna())

