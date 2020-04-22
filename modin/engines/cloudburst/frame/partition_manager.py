import numpy as np

from modin.engines.base.frame.partition_manager import BaseFrameManager
from modin.engines.cloudburst.frame.partition import PandasOnCloudburstFramePartition
from modin.error_message import ErrorMessage
from modin import __execution_engine__


from .axis_partition import (
    PandasOnCloudburstFrameColumnPartition,
    PandasOnCloudburstFrameRowPartition,
)

if __execution_engine__ == "Cloudburst":
    client = None
    import cloudpickle as pkl


  

class CloudburstFrameManager(BaseFrameManager):
    # This object uses DropletRemotePartition objects as the underlying store.
    _partition_class = PandasOnCloudburstFramePartition
    _column_partitions_class = PandasOnCloudburstFrameColumnPartition
    _row_partition_class = PandasOnCloudburstFrameRowPartition
