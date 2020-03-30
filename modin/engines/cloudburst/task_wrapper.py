from modin import __execution_engine__

if __execution_engine__ == "Cloudburst":
    from modin.engines.cloudburst.utils import get_or_init_client
    cloudburst = get_or_init_client()


class CloudburstTask:
    @classmethod
    def deploy(cls, func, num_return_vals, kwargs):
        f = cloudburst.register(lambda _, kwargs: func(**kwargs), func.__name__)
        future_obj = f(kwargs)
        unpack = cloudburst.register(lambda _, l, i: l[i], "unpack")
        return [unpack(future_obj, i) for i in range(num_return_vals)]

    @classmethod
    def materialize(cls, obj_id):
        if isinstance(obj_id, list):
            return [o.get() for o in obj_id]
        return obj_id.get()
