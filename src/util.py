def lazy_static(fn):
    """Attribute for lazily-evaluated properties.
    Functions marked with @lazy will be evaluated
    once, their output cached and that cache returned
    without evaluation for all subsequent calls."""
    attr = '_lazy_' + fn.__name__

    # credit:
    # https://towardsdatascience.com/what-is-lazy-evaluation-in-python-9efb1d3bfed0
    def _lazy(self):
        # has been evaluated?
        if not hasattr(self.__class__, attr):
            # if not, evaluate once
            setattr(self.__class__, attr, fn(self))
        # return value
        return getattr(self.__class__, attr)
            
    return _lazy

class vec2:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    @property
    def x(self): return self._x
    @x.setter
    def x(self, val): self._x = val

    @property
    def y(self): return self._y
    @y.setter
    def y(self, val): self._y = val
