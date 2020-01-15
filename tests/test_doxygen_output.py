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
                    self.assertNotRegex(line, r"([\s>]|^)#\w(\S)*", file + " in line " + str(i) + ": not permitted hash found.")


    def test_slash_triplet(self):
        ''' Test case is checking if there are slash triplets in the documentation. -> doxygen didn't interpret something properly. '''

        for file in DOC_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                for i, line in enumerate(fin, start=1):
                    self.assertNotRegex(line, r"([\s>]|^)///\s*", file + " in line " + str(i) + ": not permitted slash triplet found.")


    def test_backslash_triplet(self):
        ''' Test case is checking if there are backslash triplets in the documentation. -> doxygen didn't interpret something properly. '''
        for file in DOC_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                for i, line in enumerate(fin, start=1):
                    self.assertNotRegex(line, r"([\s>]|^)\\\\\\\s*", file + " in line " + str(i) + ": not permitted backslash triplet found.")
