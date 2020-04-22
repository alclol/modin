#!/opt/conda/bin/python
import pandas

import os
os.environ["MODIN_IP"]="127.0.0.1"
os.environ["MODIN_CONNECTION"]="127.0.0.1"
os.environ["MODIN_ENGINE"]="Cloudburst"
import modin.pandas as pd
import numpy as np

def generate_dfs():
    df = pandas.DataFrame(
        {
            "col1": [0, 1, 2, 3],
            "col2": [4, 5, 6, 7],
            "col3": [8, 9, 10, 11],
            "col4": [12, 13, 14, 15],
            "col5": [0, 0, 0, 0],
        }
    )

    df2 = pandas.DataFrame(
        {
            "col1": [0, 1, 2, 3],
            "col2": [4, 5, 6, 7],
            "col3": [8, 9, 10, 11],
            "col6": [12, 13, 14, 15],
            "col7": [0, 0, 0, 0],
        }
    )
    return df, df2

def df_equals(df1, df2):
    """Tests if df1 and df2 are equal.

    Args:
        df1: (pandas or modin DataFrame or series) dataframe to test if equal.
        df2: (pandas or modin DataFrame or series) dataframe to test if equal.

    Returns:
        True if df1 is equal to df2.
    """
    types_for_almost_equals = (
        pandas.core.indexes.range.RangeIndex,
        pandas.core.indexes.base.Index,
    )

    # Gets AttributError if modin's groupby object is not import like this
    from modin.pandas.groupby import DataFrameGroupBy

    groupby_types = (pandas.core.groupby.DataFrameGroupBy, DataFrameGroupBy)

    # The typing behavior of how pandas treats its index is not consistent when the
    # length of the DataFrame or Series is 0, so we just verify that the contents are
    # the same.
    if (
        hasattr(df1, "index")
        and hasattr(df2, "index")
        and len(df1) == 0
        and len(df2) == 0
    ):
        if type(df1).__name__ == type(df2).__name__:
            if hasattr(df1, "name") and hasattr(df2, "name") and df1.name == df2.name:
                return
            if (
                hasattr(df1, "columns")
                and hasattr(df2, "columns")
                and df1.columns.equals(df2.columns)
            ):
                return
        assert False

    # Convert to pandas
    if isinstance(df1, pd.DataFrame):
        df1 = to_pandas(df1)
    if isinstance(df2, pd.DataFrame):
        df2 = to_pandas(df2)
    if isinstance(df1, pd.Series):
        df1 = to_pandas(df1)
    if isinstance(df2, pd.Series):
        df2 = to_pandas(df2)

    if isinstance(df1, pandas.DataFrame) and isinstance(df2, pandas.DataFrame):
        if (df1.empty and not df2.empty) or (df2.empty and not df1.empty):
            return False
        elif df1.empty and df2.empty and type(df1) != type(df2):
            return False

    if isinstance(df1, pandas.DataFrame) and isinstance(df2, pandas.DataFrame):
        try:
            assert_frame_equal(
                df1.sort_index(axis=1),
                df2.sort_index(axis=1),
                check_dtype=False,
                check_datetimelike_compat=True,
                check_index_type=False,
                check_column_type=False,
            )
        except Exception:
            assert_frame_equal(
                df1,
                df2,
                check_dtype=False,
                check_datetimelike_compat=True,
                check_index_type=False,
                check_column_type=False,
            )
    elif isinstance(df1, types_for_almost_equals) and isinstance(
        df2, types_for_almost_equals
    ):
        assert_almost_equal(df1, df2, check_dtype=False)
    elif isinstance(df1, pandas.Series) and isinstance(df2, pandas.Series):
        assert_almost_equal(df1, df2, check_dtype=False, check_series_type=False)
    elif isinstance(df1, groupby_types) and isinstance(df2, groupby_types):
        for g1, g2 in zip(df1, df2):
            assert g1[0] == g2[0]
            df_equals(g1[1], g2[1])
    elif (
        isinstance(df1, pandas.Series)
        and isinstance(df2, pandas.Series)
        and df1.empty
        and df2.empty
    ):
        assert all(df1.index == df2.index)
        assert df1.dtypes == df2.dtypes
    else:
        if df1 != df2:
            np.testing.assert_almost_equal(df1, df2)

df, df2 = generate_dfs()

#frame_data = np.random.randint(0, 100, size=(2**10, 2**6))
#df = pd.DataFrame(frame_data).add_prefix("col")

cb_res = pd.concat([df, df2])
pd_res = pandas.concat([df, df2])
print(df, df2)
print(cb_res, pd_res)

