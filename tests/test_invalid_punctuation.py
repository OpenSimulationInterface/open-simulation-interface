import glob
import unittest

PROTO_FILES = glob.glob("*.proto")

class TestInvalidPunctuation(unittest.TestCase):
    ''' Test class to check invalid punctuation character  '__' '''

    def test_invalid_punctuation(self):
        ''' Test to check invalid punctuation character  '__' '''
        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                for i, line in enumerate(fin, start=1):
                    self.assertEqual(line.find("__"), -1, file + " in line " + str(i) + ": not permitted use of '__' ")
