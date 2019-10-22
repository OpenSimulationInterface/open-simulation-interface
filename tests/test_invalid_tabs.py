from glob import *
import sys
import unicodedata
import re
import unittest


class TestInvalidTabs(unittest.TestCase):
    """Test class for invalid tabulators"""

    def test_invalid_tabs(self):
        ''' Test to check if invalid tabs exist. '''
        for file in glob("*.proto"):
            i = 0  
            
            with open(file, "rt") as fin:
                for line in fin:
                    i += 1
                    self.assertEqual(line.find("\t"), -1, file + " in line " + str(i) + ": not permitted tab found")
