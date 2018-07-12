import time

'''
Block Elements found at range:
    0x2580 -> 0x259F
'''

class benchmark_timer:
    '''
    To be used by the benchmarker module, keeps track of a nested structure of times.

    variable explanations:
        'start': None,          # Used to measure time
        'times': dict(),        # Keeps track of total time
        'ttimes' : dict(),      # Keeps track of number of number of times a time has been taken
        'time_hist' : dict(),   # Keeps history of the times
        'current' : None,       # Tracks the current section name
        'timers' : dict()       # Implements a component structure.
        'level' : int           # Keeps track of the current depth of the timer
    '''

    def __init__(self, level = 0):
        self._start = None
        self._times = dict()
        self._ttimes = dict()
        self._time_hist = dict()
        self._current = None
        self._timers = dict()
        self._level = level

    def startTiming(self, name = None):
        if name is None:
            name = 'NO_NAME_GIVEN'
        if self._current is None:
            self._current = name
            self._start = time.clock()
        else:
            keyval = self._current
            if keyval not in self._timers.keys():
                self._timers[keyval] = benchmark_timer(self._level+1)
            self._timers[keyval].startTiming(name)

    def endTiming(self, name = None, tm = None):
        t = time.clock()
        if self._start is None:
            return

        if tm is not None:
            t = tm
        if self._current is not None:
            if name is None and \
                not (self._current in self._timers and self._timers[self._current]._current is not None):
                    name = self._current
            if self._current is name:
                deltaT = t - self._start
                if name in self._times:
                    self._times[name] += deltaT
                    self._ttimes[name] += 1
                    self._time_hist[name].append(t)
                else:
                    self._times[name] = deltaT
                    self._ttimes[name] = 1
                    self._time_hist[name] = [deltaT]
                if self._current in self._timers.keys():
                    self._timers[self._current].endTiming(self._timers[self._current]._current)
                self._current = None
                self._start = None
            else:
                if self._current in self._timers:
                    self._timers[self._current].endTiming(name, tm = t)

    def endAllTiming(self, tm = None):
        t = time.clock()
        assert self._current is not None, "No timing started yet"
        if tm is None:
            t = tm
        self.endTiming(name=self._current, tm = t)


    def newTiming(self, name = None):
        if self._current in self._timers and self._timers[self._current]._current is not None:
            self._timers[self._current].newTiming(name)
        elif self._current is not name:
            self.endTiming()
            self.startTiming(name)


    def getTimes(self,offset = None, depth = 1):
        if offset is None:
            offset = 0
        else:
            offset += 3
        if not self._times:
            print ("No times recorded yet")
        for key in self._times.keys():
                print ("{:<{pad}}'\033[1;31m{}\033[0m' took a total time of \033[1;33m{:f}\033[0m with an average of time \033[1;33m{:f}\033[0m".
                        format(depth,key,self._times[key],self._times[key]/self._ttimes[key],pad=offset))
                if key in self._timers:
                    new_depth = depth+1
                    self._timers[key].getTimes(offset,new_depth)

    def getTimeHist(name):
        assert name in self._time_hist, 'No history found for key {}'.format(name)
        return self._time_hist[name]


    def reset():
        self._times.clear()
        self._ttimes.clear()
        self._time_hist.clear()
        self._start = None
