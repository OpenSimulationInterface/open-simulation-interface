import glob
import unittest

PROTO_FILES = glob.glob("*.proto")

class TestNewLine(unittest.TestCase):
    ''' Test class for mandatory new line. '''

    def test_newline(self):
        ''' Test to check last line of file must end with a new line. '''
        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                lastCharacter = fin.read()[-1]
                self.assertEqual(lastCharacter, "\n", file + " has no new line at the end of the file.")
