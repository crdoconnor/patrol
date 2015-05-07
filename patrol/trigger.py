import fnmatch
import multiprocessing
from task import Task

class Trigger(object):
    """Some conditions and a python method that yields a task."""

    def __init__(self, method, includes, excludes=None, reset=None, timeout=10, ignore_ctrlc=False):
        self.method = method
        self.includes = includes
        self.excludes = [] if excludes is None else excludes
        self.reset = reset
        self.timeout = int(timeout)
        self.ignore_ctrlc = ignore_ctrlc

    def _match(self, filenames):
        """Return True if trigger matches one of the specified filenames."""
        currently_matching = False

        for filename in filenames:
            for include in self.includes:
                if fnmatch.fnmatch(filename, include):
                    currently_matching = True

            if self.excludes is not None:
                for exclude in self.excludes:
                    if fnmatch.fnmatch(filename, exclude):
                        currently_matching = False
        return currently_matching

    def fire(self, filenames):
        if self._match(filenames):
            print "PATROL: Task '{}' triggered by changes in '{}'".format(self.method.func_name, ', '.join(filenames))
            return Task(self.method, self.ignore_ctrlc, self.reset, self.timeout)
        else:
            return None
