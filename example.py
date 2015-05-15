import patrol
import signal
import time
import os


def build(filenames):
    print "1: build will be run first."
    os.system("sleep 2 ; echo 2: ...this task should always complete")

def run_test(filenames):
    print "3: Run test is run second."
    os.system("sleep 10 ; echo 4: ...this task might be stopped before this message appears.")

patrol.watch([
        patrol.Trigger(
            build,
            includes=["*.py", ],
            excludes=['venv/*', ],
            trigger_immediately=True, # When patrol.watch() is first run, initiate trigger.
        ),
        patrol.Trigger(
            run_test,
            includes=["*.py", ],
            excludes=['venv/*',],
            reaper=patrol.Reaper(),   # If triggered while method is in progress, it will stop it and start again.
            trigger_immediately=True,
        ),
    ],
    directory=os.getcwd(),
    lockfiles=["lock", ".git/lockfile",],
)
