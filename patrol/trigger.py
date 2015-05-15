from __future__ import print_function
from patrol.task import Task
import fnmatch



class Trigger(object):
    """Some conditions and a python method that yields a task."""

    def __init__(self,
                 method,
                 includes,
                 excludes=None,
                 args=None,
                 reaper=None,
                 ignore_ctrlc=False,
                 fire_on_initialization=False):

        self.method = method
        self.includes = includes
        self.args = [] if args is None else args
        self.excludes = [] if excludes is None else excludes
        self.reaper = reaper
        self.ignore_ctrlc = ignore_ctrlc
        self.fire_on_initialization = fire_on_initialization

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

    def hit_with(self, filenames):
        """Return new task if filenames match trigger, else return None."""
        if self._match(filenames):
            return self.fire(filenames)
        else:
            return None

    def fire(self, filenames):
        """Fire trigger and return task."""
        if filenames == []:
            print("PATROL: Task '{}' triggered by changes to '{}'".format(
                self.method.__name__, ', '.join(filenames)
            ))
        else:
            print("PATROL: Task '{}' triggered.".format(self.method.__name__))
        return Task(self, filenames)
