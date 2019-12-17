import glob
import unittest

PROTO_FILES = glob.glob("*.proto")

class TestInvalidTabs(unittest.TestCase):
    """Test class for invalid tabulators"""

    def test_invalid_tabs(self):
        ''' Test to check if invalid tabs exist. '''
        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                for i, line in enumerate(fin, start=1):
                    self.assertEqual(line.find("\t"), -1, file + " in line " + str(i) + ": not permitted tab found")
