def lazy(fn):
    """Functions marked with this attribute will be lazily evaluated,
    that is, their return value is computed then cached when first
    called, then that cached value is returned"""
    def _lazy(*args, **kargs):
        try:
            # return the cached value
            return fn._evaluated
        except AttributeError:
            # evaluated for the first time
            fn._evaluated = fn(*args, **kargs)
            return fn._evaluated
    return _lazy