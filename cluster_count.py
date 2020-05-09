#!/opt/conda/bin/python

import os
os.environ["MODIN_IP"]="3.220.239.84"
os.environ["MODIN_CONNECTION"]='aaaf3e305282245549c6645fd64c886c-1218831264.us-east-1.elb.amazonaws.com'
os.environ["MODIN_ENGINE"]="Cloudburst"
import modin.pandas as pd
import numpy as np

df = pd.DataFrame({"Person":
                   ["John", "Myla", "Lewis", "John", "Myla"],
                   "Age": [24., np.nan, 21., 33, 26],
                   "Single": [False, True, True, True, False]})
print(df.count())

