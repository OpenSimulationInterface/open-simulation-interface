import re
import glob
import unittest

DOC_FILES = glob.glob("doc/html/*.htm*")

class TestDoxygenOutput(unittest.TestCase):
    """ Test class for the doxygen output. """

    def test_hash(self):
        ''' Test case is checking if there are illegal hash chars in the documentation. -> doxygen link not found.  '''
        for file in DOC_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                for i, line in enumerate(fin, start=1):
                    matchHash = re.search(r"([\s>]|^)#\w(\S)*", line)

                    if matchHash is not None:
                        self.assertIsNone(matchHash, file + " in line " + str(i) + ": not permitted hash found. Search for: '"+ line[matchHash.start():matchHash.end()])


    def test_slash_triplet(self):
        ''' Test case is checking if there are slash triplets in the documentation. -> doxygen didn't interpret something properly. '''

        for file in DOC_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                for i, line in enumerate(fin, start=1):
                    matchHash = re.search(r"([\s>]|^)///\s*",line)

                    if matchHash is not None:
                        self.assertIsNone(matchHash, file + " in line " + str(i) + ": not permitted slash triplet found. Search for: '"+line[matchHash.start():matchHash.end()])


    def test_backslash_triplet(self):
        ''' Test case is checking if there are backslash triplets in the documentation. -> doxygen didn't interpret something properly. '''
        for file in DOC_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                for i, line in enumerate(fin, start=1):
                    matchHash = re.search(r"([\s>]|^)\\\\\\\s*",line)

                    if matchHash is not None:
                        self.assertIsNone(matchHash, file + " in line " + str(i) + ": not permitted backslash triplet found. Search for: '"+line[matchHash.start():matchHash.end()])
