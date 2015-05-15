import subprocess
import sys
import time
import unittest
import os
import shutil


class PatrolTestCase(unittest.TestCase):
    """Run a patrol script that mimics a running build and a test."""

    def setUp(self):
        # Change directory to the folder this file is in
        os.chdir(os.path.join(os.path.abspath(os.path.dirname(__file__))))
        self.clean_output()

    def wait_for_file_to_exist(self, filename, timeout=2):
        for _ in range(0, int(timeout * 100)):
            time.sleep(0.01)
            if os.path.exists(filename):
                return
        raise AssertionError("{} filename never appeared.".format(filename))

    def clean_output(self):
        shutil.rmtree("output", ignore_errors=True)
        os.makedirs("output")

    def touch(self, filename):
        """Platform independent equivalent of UNIX touch cmd."""
        with open(filename, "a"):
            os.utime(filename, None)

    def test_fire_on_initialization(self):
        """Test that triggers got fired without a change."""
        patrol_proc = subprocess.Popen([sys.executable, "patrol1.py",])

        self.wait_for_file_to_exist("output/build_started", timeout=0.5)
        self.wait_for_file_to_exist("output/build_finished", timeout=1)
        self.wait_for_file_to_exist("output/test_started", timeout=0.5)
        self.wait_for_file_to_exist("output/test_finished", timeout=2)

        patrol_proc.terminate()

    def test_reaper(self):
        patrol_proc = subprocess.Popen([sys.executable, "patrol1.py",])

        time.sleep(3.5)
        self.clean_output()
        self.touch("data/a")
        self.wait_for_file_to_exist("output/build_started", timeout=0.5)
        self.wait_for_file_to_exist("output/build_finished", timeout=1)
        self.wait_for_file_to_exist("output/test_started", timeout=0.5)
        self.touch("data/a")
        self.clean_output()
        self.wait_for_file_to_exist("output/build_started", timeout=0.5)
        self.wait_for_file_to_exist("output/build_finished", timeout=1)
        self.wait_for_file_to_exist("output/test_started", timeout=0.5)
        self.assertFalse(os.path.exists("output/test_finished"))

        patrol_proc.terminate()




if __name__ == "__main__":
    unittest.main()
