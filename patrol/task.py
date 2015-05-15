import multiprocessing


class Task(object):
    """A task to be completed in a method."""

    def __init__(self, trigger, filenames):
        self.trigger = trigger
        self.args = tuple([filenames] + list(self.trigger.args))
        self.process = multiprocessing.Process(target=self.run_method)
        self.started = False

    def __eq__(self, other):
        """Two tasks are the same if the method being run is the same."""
        return self.trigger.method == other.trigger.method

    def run_method(self):
        """Run trigger method with args (this should be run in a different process)."""
        self.trigger.method(self.args)

    def start(self):
        """Start task if not already started."""
        if not self.started:
            self.started = True
            self.process.start()

    def is_done(self):
        """Has the task finished?"""
        return self.started and not self.process.is_alive()

    def attempt_stop(self):
        """Send reaper if there is one, assuming the task was started."""
        if self.trigger.reaper is not None and self.started:
            self.stop()

    def stop(self):
        """Send the reaper after the task."""
        if self.process.is_alive():
            self.trigger.reaper.reap(self.trigger.method.__name__, self.process)
