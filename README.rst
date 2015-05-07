Patrol
======

Trigger methods from changed files - e.g. selectively rebuild your project or
run tests as soon as you hit the save button on your text editor or IDE.

Patrol works well with ProjectKey_.


Use
===

To install::

    pip install patrol


Create a watch class:

.. code-block:: python

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


Features
========

* Patrol does not use polling to detect file changes. It uses libuv_, which creates event driven hooks to filesystem events using epoll, kqueue or IOCP.
* You can queue up triggers by putting a file named 'lock' in the directory patrol.py is run from. Once 'lock' is removed, the pent up triggers will all be fired.

.. _ProjectKey: https://github.com/crdoconnor/projectkey

.. _libuv: https://github.com/libuv/libuv
