import re
import glob
import unittest

PROTO_FILES = glob.glob("*.proto")

class TestInvalidEnum(unittest.TestCase):
    ''' Test class to check invalid enum '''

    def test_correct_enum_name(self):
        ''' Test if enum name is correct. '''
        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                isEnum = False
                enumName = ""
                saveStatement = ""

                for i, line in enumerate(fin, start=1):
                    # Divide statement and comment. Concatenate multi line statements.

                    # Search for comment ("//").
                    matchComment = re.search("//", line)

                    if matchComment is not None:
                        statement = line[:matchComment.start()]
                        comment = line[matchComment.end():]
                    else:
                        statement = line
                        comment = ""

                    # # Add part of the statement from last line.
                    statement = saveStatement + " " + statement
                    saveStatement = ""

                    # # New line is not necessary. Remove for a better output.
                    statement = statement.replace("\n", "")
                    comment = comment.replace("\n", "")

                    # # Is statement complete
                    matchSep = re.search(r"[{};]", statement)
                    if matchSep is None:
                        saveStatement = statement
                        statement = ""
                    else:
                        saveStatement = statement[matchSep.end():]
                        statement = statement[:matchSep.end()]

                    # This section will check camelcase for enums and check enum name?

                    if isEnum is True:
                        matchName = re.search(r"\b\w[\S:]+\b", statement)

                        if matchName is not None:
                            checkName = statement[matchName.start():matchName.end()]

                            # Test to check correct ENUM name.
                            self.assertEqual(checkName.find(enumName), 0, file + " in line " + str(i) + ": enum type wrong. '" + checkName + "' should start with '" + enumName + "'")

                            # Test to check ENUM type is in captial letters/upper case.
                            self.assertEqual(checkName, checkName.upper(), file + " in line " + str(i) + ": enum type wrong. '" + checkName + "' should use upper case")


                    # Search for "enum".
                    matchEnum = re.search(r"\benum\b", statement)

                    if matchEnum is not None:
                        isEnum = True
                        endOfLine = statement[matchEnum.end():]
                        matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                        if matchName is not None:
                                # Test to ensure no special characters are in ENUM name.
                                matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b", endOfLine[matchName.start():matchName.end()])
                                enumName = self.convert(endOfLine[matchName.start():matchName.end()]) + "_"

                    # Search for a closing brace.
                    matchClosingBrace = re.search("}", statement)
                    if isEnum is True and matchClosingBrace is not None:
                        isEnum = False
                        enumName = ""


    def test_invalid_enum(self):
        ''' Test invalid enum definition. '''
        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                isEnum = False
                enumName = ""
                saveStatement = ""

                for i, line in enumerate(fin, start=1):
                    # Divide statement and comment. Concatenate multi line statements.

                    # Search for comment ("//").
                    matchComment = re.search("//", line)

                    if matchComment is not None:
                        statement = line[:matchComment.start()]
                        comment = line[matchComment.end():]
                    else:
                        statement = line
                        comment = ""

                    # Add part of the statement from last line.
                    statement = saveStatement + " " + statement
                    saveStatement = ""

                    # New line is not necessary. Remove for a better output.
                    statement = statement.replace("\n", "")
                    comment = comment.replace("\n", "")

                    # Is statement complete
                    matchSep = re.search(r"[{};]", statement)
                    if matchSep is None:
                        saveStatement = statement
                        statement = ""
                    else:
                        saveStatement = statement[matchSep.end():]
                        statement = statement[:matchSep.end()]

                    # This section will check camelcase for enums and check enum name?

                    if isEnum is True:
                        matchName = re.search(r"\b\w[\S:]+\b", statement)

                        if matchName is not None:
                            checkName = statement[matchName.start():matchName.end()]

                    # Search for "enum".
                    matchEnum = re.search(r"\benum\b", statement)

                    if matchEnum is not None:
                        isEnum = True
                        endOfLine = statement[matchEnum.end():]
                        matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                        if matchName is not None:
                            # Test to ensure no special characters are in ENUM name.
                            matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b", endOfLine[matchName.start():matchName.end()])
                            self.assertIsNotNone(matchNameConv, file + " in line " + str(i) + ": enum name wrong. '" + endOfLine[matchName.start():matchName.end()] + "'")
                            enumName = self.convert(endOfLine[matchName.start():matchName.end()]) + "_"

                    # Search for a closing brace.
                    matchClosingBrace = re.search("}", statement)
                    if isEnum is True and matchClosingBrace is not None:
                        isEnum = False
                        enumName = ""

    def convert(self, name):
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).upper()