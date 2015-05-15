Patrol
======

Trigger methods from changed files - e.g. selectively rebuild your project or
run tests as soon as you hit the save button on your text editor or IDE.

Patrol works well with ProjectKey_.


Use
===

To install::

    pip install patrol

Example code:

.. code-block:: python

    import patrol

    def build(filenames):
        touch("output/build_started")
        time.sleep(2)
        touch("output/build_finished")

    def run_test(filenames):
        touch("output/test_started")
        time.sleep(30)
        touch("output/test_finished")

    patrol.watch([
            patrol.Trigger(
                build,
                includes=["data/*", ],
                excludes=['data/exclude/*', 'output/*', ],
            ),
            patrol.Trigger(
                run_test,
                includes=["data/*", ],
                excludes=['data/exclude/*', 'output/*', ],
                reaper=patrol.Reaper(),         # If triggered while method is in progress, this will stop it and start it again.
                fire_on_initialization=True,    # When the watch is initiated, this trigger will also fire.
            ),
        ],
        directory=os.getcwd(),            # By default it patrols the present working directory.
        lockfiles=[".git/index.lock", ],  # This will wait until git has finished its operations before firing any triggers
    )



Features
========

* Patrol does not use polling to detect file changes. It uses libuv_, which creates event driven hooks to filesystem events using epoll, kqueue or IOCP.
* You can queue up triggers when a specified lockfile is present - e.g. you can use to prevent triggers from firing until git operations are done.
* Patrol comes with a customized Reaper class that can be used to specify how a process is stopped.

.. _ProjectKey: https://github.com/crdoconnor/projectkey

.. _libuv: https://github.com/libuv/libuv
