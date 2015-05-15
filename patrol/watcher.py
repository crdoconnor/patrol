from __future__ import print_function
import signal
import pyuv
import os


def watch(triggers, directory=os.getcwd(), lockfiles=None):
    """Initialize the watcher and run it."""
    Watcher(triggers, directory, lockfiles).run()


class Watcher(object):
    """Watches the filesystem and fires triggers using libuv."""

    def __init__(self, triggers, directory, lockfiles):
        self.directory = directory
        self.triggers = triggers
        self.lockfiles = [] if lockfiles is None else lockfiles
        self.change_queue = []
        self.event_handles = []
        self.task_queue = []
        self.signal_handler = None
        self.timer_handler = None
        self.triggered = False

    def empty_task_queue(self):
        """Is the task queue empty?"""
        return len(self.task_queue) == 0

    def first_task(self):
        """Return first task in the queue, or nothing if empty."""
        if self.empty_task_queue():
            return None
        else:
            return self.task_queue[0]

    def close_handles(self):
        """Close all I/O handles prior to exit,
           provided a non-ctrlc ignored task is in progress."""
        if self.first_task() is None or not self.first_task().trigger.ignore_ctrlc:
            for task in self.task_queue:
                task.stop()
            self.signal_handler.close()
            self.timer_handler.close()
            for event_handle in self.event_handles:
                event_handle.close()

    def read_callback(self, handle, filename, events, error):
        """Callback every time something is modified in the repository."""
        fullpath = os.path.realpath(str(handle.path) + os.sep + filename)
        relative_path = fullpath.replace(os.path.realpath(self.directory) + os.sep, "")

        if os.path.exists(fullpath):
            self.change_queue.append(relative_path)

        for lockfile in self.lockfiles:
            if os.path.exists(self.directory + os.sep + lockfile):
                return

        for trigger in self.triggers:
            task = trigger.hit_with(self.change_queue)
            if task is not None and task not in self.task_queue[1:]:
                self.task_queue.append(task)
                self.triggered = True
        self.change_queue = []

    def poll_callback(self, timer_handle):
        """Handle running tasks."""
        if len(self.task_queue) > 0:
            firsttask = self.task_queue[0]
            if self.triggered and len(self.task_queue) > 1:
                firsttask.attempt_stop()

            self.triggered = False
            firsttask.start()
            if firsttask.is_done():
                del self.task_queue[0]

                if len(self.task_queue) == 0:
                    print("PATROL: ALL TASKS COMPLETE")



    def run(self):
        """Run the watcher."""
        print("PATROL: Started")
        loop = pyuv.Loop.default_loop()

        # Attach a handler for each subdirectory underneath
        for subdirectory in [os.path.realpath(x[0]) for x in os.walk(self.directory)]:
            event_handle = pyuv.fs.FSEvent(loop)
            event_handle.start(subdirectory, 0, self.read_callback)
            self.event_handles.append(event_handle)

        # Attach a handler for CTRL-C
        self.signal_handler = pyuv.Signal(loop)
        self.signal_handler.start(lambda handle, signum: self.close_handles(), signal.SIGINT)

        # Attach a handler to start/stop/kill running tasks.
        self.timer_handler = pyuv.Timer(loop)
        self.timer_handler.start(self.poll_callback, 0.05, 0.05)

        # Fire all "fire on initialization" triggers.
        for trigger in self.triggers:
            if trigger.fire_on_initialization:
                self.task_queue.append(trigger.fire([]))

        loop.run()
        print("PATROL: Stopped")
