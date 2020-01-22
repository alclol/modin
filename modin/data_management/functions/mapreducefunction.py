from .function import Function


class MapReduceFunction(Function):
    @classmethod
    def call(cls, map_function, reduce_function, **call_kwds):
        def caller(query_compiler, *args, **kwargs):
            mapfunc = lambda x: map_function(x, *args, **kwargs)
            mapfunc._pandas_func = map_function
            reducefunc = lambda y: reduce_function(y, *args, **kwargs)
            reducefunc._pandas_func = reduce_function
            return query_compiler.__constructor__(
                query_compiler._modin_frame._map_reduce(
                    call_kwds.get("axis")
                    if "axis" in call_kwds
                    else kwargs.get("axis"),
                    mapfunc,
                    reducefunc,
                )
            )

        return caller

    @classmethod
    def register(cls, map_function, reduce_function, **kwargs):
        return cls.call(map_function, reduce_function, **kwargs)
