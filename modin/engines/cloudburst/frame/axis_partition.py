from modin.engines.base.frame.axis_partition import PandasFrameAxisPartition
from .partition import PandasOnCloudburstFramePartition
from modin import __execution_engine__



# TODO: Move to apply
if __execution_engine__ == "Cloudburst":
  from cloudburst.shared.reference import CloudburstReference
  from modin.engines.cloudburst.utils import get_or_init_client

  cloudburst = get_or_init_client()


class PandasOnCloudburstFrameAxisPartition(PandasFrameAxisPartition):
    def __init__(self, list_of_blocks):
        # Unwrap from BaseFramePartition object for ease of use
        for obj in list_of_blocks:
            obj.drain_call_queue()
        self.list_of_blocks = [obj.future for obj in list_of_blocks]

    partition_type = PandasOnCloudburstFramePartition
    if __execution_engine__ == "Cloudburst":
        # TODO: Determine instance type
        # DASK: instance_type = Future
        pass

    @classmethod
    def deploy_axis_func(
        cls, axis, func, num_splits, kwargs, maintain_partitioning, *partitions
    ):
        client = get_or_init_client()
        r_func = cloudburst.register(
            PandasFrameAxisPartition.deploy_axis_func, "PandasFrameAxisPartition.deploy_axis_func"
        )

        axis_result = r_func(
            axis,
            func,
            num_splits,
            kwargs,
            maintain_partitioning,
            *partitions,
          )


        if num_splits == 1:
            return axis_result
        # We have to do this to split it back up. It is already split, but we need to
        # get futures for each.
        return [
            client.submit(lambda l: l[i], axis_result, pure=False)
            for i in range(num_splits)
        ]

    @classmethod
    def deploy_func_between_two_axis_partitions(
        cls, axis, func, num_splits, len_of_left, kwargs, *partitions
    ):
        client = get_or_init_client()
        r_func = cloudburst.register(
            PandasFrameAxisPartition.deploy_func_between_two_axis_partitions, "PandasFrameAxisPartition.deploy_func_between_two_axis_partitions"
        )


        axis_result = r_func(
            axis,
            func,
            num_splits,
            len_of_left,
            kwargs,
            *partitions,
        )
        if num_splits == 1:
            return axis_result
        # We have to do this to split it back up. It is already split, but we need to
        # get futures for each.
        return [
            client.submit(lambda l: l[i], axis_result, pure=False)
            for i in range(num_splits)
        ]


class PandasOnDaskFrameColumnPartition(PandasOnDaskFrameAxisPartition):
    """The column partition implementation for Multiprocess. All of the implementation
        for this class is in the parent class, and this class defines the axis
        to perform the computation over.
    """

    axis = 0


class PandasOnDaskFrameRowPartition(PandasOnDaskFrameAxisPartition):
    """The row partition implementation for Multiprocess. All of the implementation
        for this class is in the parent class, and this class defines the axis
        to perform the computation over.
    """

    axis = 1
>>>>>>> 1a2f8460f6a1ae54a9ec4150583e92a63e7de202
