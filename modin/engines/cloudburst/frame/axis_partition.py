from modin.engines.base.frame.axis_partition import PandasFrameAxisPartition
from .partition import PandasOnRayFramePartition
from modin import __execution_engine__

if __execution_engine__ == "Cloudburst":
  # TODO: Determine imports for CB
  from distributed.client import get_client
  from distributed import Future


class PandasOnCloudburstFrameAxisPartition(PandasFrameAxisPartition):
  def __init__(self, list_of_blocks):
    # Unwrap from BaseFramePartition object for ease of use
    for obj in list_of_blocks:
      obj.drain_call_queue()
    self.list_of_blocks = [obj.oid for obj in list_of_blocks]

  partition_type = PandasOnCloudburstFramePartition
  if __execution_engine__ == "Cloudburst":
  # TODO: Check if this is valid
    instance_type = Future

  @classmethod
  def deploy_axis_func(
    cls, axis, func, num_splits, kwargs, maintain_partitioning, *partitions
  ):
    # TODO: Implement

  @classmethod
  def deploy_func_between_two_axis_partitions(
    cls, axis, func, num_splits, len_of_left, kwargs, *partitions
  ):
    # TODO: Implement

class PandasOnRayFrameColumnPartition(PandasOnCloudburstFrameAxisPartition):
  """The column partition implementation for Cloudburst. All of the implementation
      for this class is in the parent class, and this class defines the axis
      to perform the computation over.
  """

  axis = 0


class PandasOnRayFrameRowPartition(PandasOnCloudburstFrameAxisPartition):
  """The row partition implementation for CLoudburst. All of the implementation
      for this class is in the parent class, and this class defines the axis
      to perform the computation over.
  """

  axis = 1

