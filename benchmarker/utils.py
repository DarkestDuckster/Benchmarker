import benchmarker.core as bm
from functools import wraps

def timedMethod(timed_func,name = None):
    if name is None:
        name = timed_func.__name__
    def timed_method():
        bm.startTiming(name)
        timed_func()
        bm.endTiming(name)
    return timed_method
