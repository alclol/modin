from modin.engines.cloudburst.frame.partition_manager import CloudburstFrameManager
from modin.engines.base.frame.data import BasePandasFrame

class PandasOnCloudburstFrame(BasePandasFrame):

    _frame_mgr_cls = CloudburstFrameManager

    @property
    def _row_lengths(self):
        """Compute the row lengths if they are not cached.
        Returns:
            A list of row lengths.
        """
        if self._row_lengths_cache is None:
            self._row_lengths_cache = [
                obj.apply(lambda df: len(df)).future.get() 
                for obj in self._partitions.T[0] if obj
            ]
        return self._row_lengths_cache

    @property
    def _column_widths(self):
        """Compute the column widths if they are not cached.
        Returns:
            A list of column widths.
        """
        if self._column_widths_cache is None:
            self._column_widths_cache = [
                obj.apply(lambda df: len(df.columns)).future.get()
                for obj in self._partitions[0] if obj
            ]
        return self._column_widths_cache
