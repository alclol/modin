from modin.engines.base.frame.partition_manager import BaseFrameManager
from modin.engines.cloudburst.frame.partition import PandasOnCloudburstFramePartition
from modin.error_message import ErrorMessage
from modin import __execution_engine__


from .axis_partition import (
    PandasOnCloudburstFrameColumnPartition,
    PandasOnCloudburstFrameRowPartition,
)

if __execution_engine__ == "Cloudburst":
    cloudburst = None

class CloudburstFrameManager(BaseFrameManager):
    # This object uses DropletRemotePartition objects as the underlying store.
    _partition_class = PandasOnCloudburstFramePartition
    _column_partitions_class = PandasOnCloudburstFrameColumnPartition
    _row_partition_class = PandasOnCloudburstFrameRowPartition

    @classmethod
    def get_indices(cls, axis, partitions, index_func):
        """This gets the internal indices stored in the partitions.

        Note: These are the global indices of the object. This is mostly useful
            when you have deleted rows/columns internally, but do not know
            which ones were deleted.

        Args:
            axis: This axis to extract the labels. (0 - index, 1 - columns).
            index_func: The function to be used to extract the function.
            old_blocks: An optional previous object that this object was
                created from. This is used to compute the correct offsets.

        Returns:
            A Pandas Index object.
        """

        global cloudburst
        if __execution_engine__ == "Cloudburst" and cloudburst is None:
            from cloudburst.shared.reference import CloudburstReference
            from modin.engines.cloudburst.utils import get_or_init_client
            client = get_or_init_client()

        ErrorMessage.catch_bugs_and_request_email(not callable(index_func))
        func = cls.preprocess_func(index_func)
        if axis == 0:
            # We grab the first column of blocks and extract the indices
            new_idx = (
                [idx.apply(func).future for idx in partitions.T[0]]
                if len(partitions.T)
                else []
            )
        else:
            new_idx = (
                [idx.apply(func).future for idx in partitions[0]]
                if len(partitions)
                else []
            )
        new_idx = client.gather(new_idx)
        return new_idx[0].append(new_idx[1:]) if len(new_idx) else new_idx
