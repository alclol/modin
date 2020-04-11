from modin.engines.base.frame.axis_partition import PandasFrameAxisPartition
from .partition import PandasOnCloudburstFramePartition
from modin import __execution_engine__

if __execution_engine__ == "Cloudburst":
    cloudburst = None

class PandasOnCloudburstFrameAxisPartition(PandasFrameAxisPartition):
    def __init__(self, list_of_blocks):
        # Unwrap from BaseFramePartition object for ease of use
        for obj in list_of_blocks:
            obj.drain_call_queue()
        self.list_of_blocks = [obj.future for obj in list_of_blocks]

    partition_type = PandasOnCloudburstFramePartition
#    if __execution_engine__ == "Dask":
#        instance_type = Future

    @classmethod
    def deploy_axis_func(
        cls, axis, func, num_splits, kwargs, maintain_partitioning, *partitions
    ):
        if not cloudburst:
            from cloudburst.shared.reference import CloudburstReference
            from modin.engines.cloudburst.utils import get_or_init_client
            cloudburst = get_or_init_client()

        func = PandasFrameAxisPartition.deploy_axis_func
        # args = [axis, func, num_splits, kwargs, maintain_partitioning, *partitions, pure]
        args = [axis, func, num_splits, kwargs, maintain_partitioning, *partitions, False]
        f = cloudburst.register(lambda _, _args: func(*_args), func.__name__)
        axis_result = f(args)

        if num_splits == 1:
            return axis_result

        unpack = cloudburst.register(lambda _, l, i: l[i], "unpack")
        return [unpack(axis_result, i) for i in range(num_splits)]

    @classmethod
    def deploy_func_between_two_axis_partitions(
        cls, axis, func, num_splits, len_of_left, kwargs, *partitions
    ):
        if not cloudburst:
            from cloudburst.shared.reference import CloudburstReference
            from modin.engines.cloudburst.utils import get_or_init_client
            cloudburst = get_or_init_client()

        func = PandasFrameAxisPartition.deploy_func_between_two_axis_partitions
        args = [axis, func, num_splits, len_of_left, kwargs, *partitions, False]
        f = cloudburst.register(lambda _, _args: func(*_args), func.__name__)
        axis_result = f(args)

        if num_splits == 1:
            return axis_result

        unpack = cloudburst.register(lambda _, l, i: l[i], "unpack")
        return [unpack(future_obj, i) for i in range(num_splits)]

class PandasOnCloudburstFrameColumnPartition(PandasOnDaskFrameAxisPartition):
    """The column partition implementation for Multiprocess. All of the implementation
        for this class is in the parent class, and this class defines the axis
        to perform the computation over.
    """

    axis = 0


class PandasOnCloudburstFrameRowPartition(PandasOnDaskFrameAxisPartition):
    """The row partition implementation for Multiprocess. All of the implementation
        for this class is in the parent class, and this class defines the axis
        to perform the computation over.
    """

    axis = 1

