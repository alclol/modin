from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import logging
import argparse
import os
import ray
import modin.pandas as pd

from utils import time_logger


parser = argparse.ArgumentParser(description='read_csv benchmark')
parser.add_argument('--path', dest='path', help='path to the csv file')
parser.add_argument('--logfile', dest='logfile', help='path to the log file')
args = parser.parse_args()
file = args.path
file_size = os.path.getsize(file)

logging.basicConfig(filename=args.logfile, level=logging.INFO)

with time_logger("Read csv file: {}; Size: {} bytes".format(file, file_size)):
    df = pd.read_csv(file)
    blocks = df._block_partitions.flatten().tolist()
    ray.wait(blocks, len(blocks))

with time_logger("Write csv file; Size: {} bytes".format(file_size)):
    df.to_csv("/tmp/test_file.csv")

os.remove("/tmp/test_file.csv")