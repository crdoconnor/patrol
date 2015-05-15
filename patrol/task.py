import multiprocessing


class Task(object):
    """A task to be completed in a method."""

    def __init__(self, trigger, filenames):
        self.trigger = trigger
        self.args = tuple([filenames] + list(self.trigger.args))
        self.process = multiprocessing.Process(target=self.run_method)
        self.started = False

    def __eq__(self, other):
        return self.trigger.method == other.trigger.method

    def run_method(self):
        self.trigger.method(self.args)

    def start(self):
        if not self.started:
            self.started = True
            self.process.start()

    def is_done(self):
        return self.started and not self.process.is_alive()

    def attempt_stop(self):
        if self.trigger.reaper is not None and self.started:
            self.stop()

    def stop(self):
        if self.process.is_alive():
            self.trigger.reaper.reap(self.trigger.method.func_name, self.process)
