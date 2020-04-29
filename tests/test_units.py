import re
import glob
import unittest

PROTO_FILES = glob.glob("*.proto")

class TestUnits(unittest.TestCase):
    """ Test class for units documentation. """

    def test_no_brackets(self):
        ''' Test to check if units have the right syntax. '''

        NOT_VALID_BRACKETS = [r'\(', r'\)', r'\[', r'\]', r'\{', r'\}']
        
        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                for i, line in enumerate(fin, start=1):
                    found = re.search('Unit:', line, re.IGNORECASE)

                    if found:
                        comment_list = line.split()
                        self.assertEqual(comment_list[0], '//', file + " in line " + str(i) + ": Unit must be on a separate line or have a space between //. (Example: '// Unit: m')")
                        self.assertEqual(comment_list[1], 'Unit:', file + " in line " + str(i) + f": '{comment_list[1]}' do not match 'Unit:'. (Example: '// Unit: m')")
                        self.assertGreaterEqual(len(comment_list), 3, file + " in line " + str(i) + ": No unit defined. (Example: '// Unit: m')")
                        
                        for unit in comment_list:
                            for brackets in NOT_VALID_BRACKETS:
                                self.assertNotRegex(unit, brackets, file + " in line " + str(i) + ": Invalid brackets around units.")
