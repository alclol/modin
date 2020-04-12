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
    cloudburst = None


    # TODO: Convert to Cloudburst
    def deploy_func(df, other, apply_func, call_queue_df=None, call_queue_other=None):
        if call_queue_df is not None and len(call_queue_df) > 0:
            for call, kwargs in call_queue_df:
                if isinstance(call, bytes):
                    call = pkl.loads(call)
                if isinstance(kwargs, bytes):
                    kwargs = pkl.loads(kwargs)
                df = call(df, **kwargs)
        if call_queue_other is not None and len(call_queue_other) > 0:
            for call, kwargs in call_queue_other:
                if isinstance(call, bytes):
                    call = pkl.loads(call)
                if isinstance(kwargs, bytes):
                    kwargs = pkl.loads(kwargs)
                other = call(other, **kwargs)
        if isinstance(apply_func, bytes):
            apply_func = pkl.loads(apply_func)
        return apply_func(df, other)

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
        # TODO: Is gather valid
        new_idx = client.gather(new_idx)
        return new_idx[0].append(new_idx[1:]) if len(new_idx) else new_idx

    @classmethod
    def broadcast_apply(cls, axis, apply_func, left, right):

        global cloudburst
        if __execution_engine__ == "Cloudburst" and cloudburst is None:
            from cloudburst.shared.reference import CloudburstReference
            from modin.engines.cloudburst.utils import get_or_init_client
            client = get_or_init_client()


        right_parts = np.squeeze(right)
        if len(right_parts.shape) == 0:
            right_parts = np.array([right_parts.item()])
        assert (
            len(right_parts.shape) == 1
        ), "Invalid broadcast partitions shape {}\n{}".format(
            right_parts.shape, [[i.get() for i in j] for j in right_parts]
        )

        r_func = client.register(deploy_func, 'deploy_func')
        return np.array(
            [
                [
                    PandasOnCloudburstFramePartition(
                        deploy_func(
                            part.future,
                            right_parts[col_idx].future
                            if axis
                            else right_parts[row_idx].future,
                            apply_func,
                            part.call_queue,
                            right_parts[col_idx].call_queue
                            if axis
                            else right_parts[row_idx].call_queue,
                        )
                    )
                    for col_idx, part in enumerate(left[row_idx])
                ]
                for row_idx in range(len(left))
            ]
        )
