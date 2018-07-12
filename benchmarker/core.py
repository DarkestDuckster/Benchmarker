from __future__ import absolute_import
import benchmarker.benchmark_timer as bm

_t = bm.benchmark_timer()

def startTiming(name = None):
    _t.startTiming(name)

def endTiming(name = None):
    _t.endTiming(name)

def newTiming(name = None):
    _t.newTiming(name)

def endAllTiming():
    _t.endAllTiming()

def getTimes():
    _t.getTimes()
