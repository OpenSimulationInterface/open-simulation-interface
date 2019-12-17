import glob
import unittest

PROTO_FILES = glob.glob("*.proto")

class TestInvalidCommentType(unittest.TestCase):
    """Test class for invalid comment types"""

    def test_triple_slash(self):
        ''' Test to check if more than two forward slash('/') are present in comment section of proto file. '''
        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                for i, line in enumerate(fin, start=1):
                    self.assertEqual(line.find("///"), -1, file + " in line " + str(i) + ": not permitted use of '///' ")

    def test_comments_invalid_syntax(self):
        ''' Test to check if comments are given using invalid syntax '/*' or '*/' '''
        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                for i, line in enumerate(fin, start=1):
                    self.assertEqual(line.find("/*"), -1, file + " in line " + str(i) + ": not permitted use of '/*' ")
                    self.assertEqual(line.find("*/"), -1, file + " in line " + str(i) + ": not permitted use of '*/' ")