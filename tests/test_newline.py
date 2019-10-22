import sys
import unicodedata
import re
from glob import *
import unittest


class TestNewLine(unittest.TestCase):
    ''' Test class for mandatory new line. ''' 

    def test_newline(self):
        ''' Test to check last line of file must end with a new line. '''
        for file in glob("*.proto"):
            with open(file, "rt") as fin:
                hasNewLine = True

                for line in fin:
                    hasNewLine = line.endswith("\n")

                self.assertTrue(hasNewLine, file + " has no new line at the end of the file.")
                