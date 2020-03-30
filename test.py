import os
os.environ["MODIN_IP"]="127.0.0.1"
os.environ["MODIN_CONNECTION"]="127.0.0.1"
os.environ["MODIN_ENGINE"]="cloudburst"
import modin.pandas as pd

df = pd.read_csv(os.getcwd() + "/test_files/file.csv")

