import multiprocessing
import psutil
import time
import os


class Task(object):
    """A task to be completed in a method."""

    def __init__(self, method, ignore_ctrlc, reset, timeout):
        self.process = multiprocessing.Process(target=self.run_method)
        self.process.reset = reset
        self.started = False
        self.reset = reset
        self.method = method
        self.timeout = timeout
        self.ignore_ctrlc = ignore_ctrlc

    def __eq__(self, other):
        return self.method == other.method

    def run_method(self):
        self.method()

    def start(self):
        if not self.started:
            self.started = True
            self.process.start()

    def is_done(self):
        return self.started and not self.process.is_alive()

    def attempt_stop(self):
        if self.reset is not None and self.started:
            self.stop()

    def stop(self):
        if self.process.is_alive():
            print "PATROL: Stopping task '{}'".format(self.method.func_name)
            proc_list = psutil.Process(self.process.pid).get_children(recursive=True)
            for childproc in proc_list:
                try:
                    childproc.send_signal(self.reset)
                except psutil.NoSuchProcess:
                    pass

            for i in range(0, int(self.timeout * 10)):
                time.sleep(0.1)
                still_alive = False

                for childproc in proc_list:
                    if childproc.is_running():
                        still_alive = True

                if not still_alive:
                    break

            if still_alive:
                for proc in proc_list:
                    if proc.is_running():
                        full_name = ' '.join(proc.cmdline).strip()
                        print "PATROL: Killing process '{}'".format(full_name)
                        proc.kill()
            else:
                print "PATROL: '{}' finished cleanly.".format(self.method.func_name)

            self.process.terminate()
