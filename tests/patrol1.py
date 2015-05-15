from os import path, chdir, getcwd, utime, sep
import patrol
import shutil
import time
import os

# Change directory to the directory this file is in
chdir(path.dirname(getcwd() + sep + __file__))

def touch(filename):
    """Platform independent equivalent of UNIX touch cmd."""
    with open(filename, "a"):
        utime(filename, None)

def build(filenames):
    touch("output/build_started")
    time.sleep(1)
    touch("output/build_finished")

def run_test(filenames):
    touch("output/test_started")
    time.sleep(2)
    touch("output/test_finished")

patrol.watch([
        patrol.Trigger(
            build,
            includes=["data/*", ],
            excludes=['data/exclude/*', 'output/*', ],
            fire_on_initialization=True, # When patrol.watch() is first run, initiate trigger.
        ),
        patrol.Trigger(
            run_test,
            includes=["data/*", ],
            excludes=['data/exclude/*', 'output/*', ],
            reaper=patrol.Reaper(),   # If triggered while method is in progress, it will stop it and start again.
            fire_on_initialization=True,
        ),
    ],
    directory=getcwd(),
    lockfiles=["lock", ],
)
