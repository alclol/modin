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
    if __execution_engine__ == "Cloudburst":
        from distributed import Future
        instance_type = Future

    @classmethod
    def deploy_axis_func(
        cls, axis, func, num_splits, kwargs, maintain_partitioning, *partitions
    ):
        global cloudburst
        if not cloudburst:
            from cloudburst.shared.reference import CloudburstReference
            from modin.engines.cloudburst.utils import get_or_init_client
            cloudburst = get_or_init_client()

        args = [axis, func, num_splits, kwargs, maintain_partitioning, *partitions]
        f = cloudburst.register(lambda _, *args: PandasFrameAxisPartition.deploy_axis_func(*args), 'PandasFrameAxisPartition.deploy_axis_func')
        axis_result = f(*args)

        if num_splits == 1:
            return axis_result
        unpack = cloudburst.register(lambda _, l, i: l[i], "unpack")
        res = [unpack(axis_result, i) for i in range(num_splits)]
        return res

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
        print(" axis_res = ", axis_result)

        if num_splits == 1:
            return axis_result

        unpack = cloudburst.register(lambda _, l, i: l[i], "unpack")
        return [unpack(axis_result, i) for i in range(num_splits)]

class PandasOnCloudburstFrameColumnPartition(PandasOnCloudburstFrameAxisPartition):
    """The column partition implementation for Multiprocess. All of the implementation
        for this class is in the parent class, and this class defines the axis
        to perform the computation over.
    """

    axis = 0


class PandasOnCloudburstFrameRowPartition(PandasOnCloudburstFrameAxisPartition):
    """The row partition implementation for Multiprocess. All of the implementation
        for this class is in the parent class, and this class defines the axis
        to perform the computation over.
    """

    axis = 1

