from __future__ import print_function
from signal import SIGTERM
import psutil
import time


class Reaper(object):
    """Object responsible for stopping processes - softly or violently."""

    def __init__(self, signal=SIGTERM, timeout=10):
        self.signal = signal
        self.timeout = timeout

    def reap(self, name, process):
        print("PATROL: Stopping task '{}'".format(name))
        proc_list = psutil.Process(process.pid).children(recursive=True)
        for childproc in proc_list:
            try:
                childproc.send_signal(self.signal)
            except psutil.NoSuchProcess:
                pass

        for _ in range(0, int(self.timeout * 10)):
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
                    full_name = ' '.join(proc.cmdline()).strip()
                    print("PATROL: Killing process '{}'".format(full_name))
                    proc.kill()
        else:
            print("PATROL: '{}' finished cleanly.".format(name))

        process.terminate()
