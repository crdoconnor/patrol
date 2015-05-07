import patrol
import signal
import time
import os


def build():
    print "1: build will be run first."
    os.system("sleep 2 ; echo 2: ...this task should always complete")

def run_test():
    print "3: Run test is run second."
    os.system("sleep 30 ; echo 4: ...this task might be stopped before this message appears.")

patrol.watch(os.getcwd(), [
    patrol.Trigger(
        build,
        includes=["*.py", ],
        excludes=['venv/*', ],
    ),
    patrol.Trigger(
        run_test,
        includes=["*.py", ],
        excludes=['venv/*',],
        reset=signal.SIGTERM,   # If triggered while method is in progress, it will stop it and start again.
        timeout=1,              # How long to wait before SIGKILLing.
    ),
], lockfile="lock")
