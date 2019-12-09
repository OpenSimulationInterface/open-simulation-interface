import sys
import unicodedata
import glob
import unittest

PROTO_FILES = glob.glob("*.proto")

class TestNonAscii(unittest.TestCase):
    """Class is checking if there is an "Umlaut" or any non ASCII characters are present."""

    def test_non_ascii(self):
        ''' Test if there are any non ASCII characters present like an "Umlaut". '''
        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                for i, line in enumerate(fin, start=1):
                    if (sys.version_info >= (3, 0)):
                        self.assertEqual(line, unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').decode(), file + " in line " + str(i) + ": a none ASCII char is present")
                    else:
                        self.assertEqual(line, unicodedata.normalize('NFKD', unicode(line, 'ISO-8859-1')).encode('ASCII', 'ignore'), file + " in line " + str(i) + ": a none ASCII char is present")