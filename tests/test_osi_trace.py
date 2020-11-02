import os
import tempfile
import unittest

from format.OSITrace import OSITrace


class TestOSITrace(unittest.TestCase):
    def test_osi_trace(self):
        cur_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(cur_dir, "data", "small_test.txt.lzma")

        with tempfile.TemporaryDirectory() as tmpdirname:
            path_output = os.path.join(tmpdirname, "output.txth")
            trace = OSITrace()
            trace.from_file(path=path)
            trace.make_readable(path_output, index=1)
            trace.scenario_file.close()

            self.assertTrue(os.path.exists(path_output))

