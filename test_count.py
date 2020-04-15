#!/opt/conda/bin/python

import os
os.environ["MODIN_IP"]="127.0.0.1"
os.environ["MODIN_CONNECTION"]="127.0.0.1"
os.environ["MODIN_ENGINE"]="cloudburst"
import modin.pandas as pd
import numpy as np

df = pd.DataFrame({"Person":
                   ["John", "Myla", "Lewis", "John", "Myla"],
                   "Age": [24., np.nan, 21., 33, 26],
                   "Single": [False, True, True, True, False]})
print(df.count())

