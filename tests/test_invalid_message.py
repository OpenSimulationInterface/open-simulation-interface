import re
import glob
import unittest

PROTO_FILES = glob.glob("*.proto")

class TestInvalidMessage(unittest.TestCase):
    """ Test class for invalid html comment. """

    def test_message_name(self):
        ''' Test to check if message name have any special character. It should not have any special character. '''

        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                i = 0
                isEnum = False
                enumName = ""
                noMessage = 0
                saveStatement = ""

                for line in fin:
                    i += 1

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

                    if isEnum is False:
                        # Check if not inside an enum.

                        # Search for "message".
                        matchMessage = re.search(r"\bmessage\b", statement)
                        if matchMessage is not None:
                            # a new message or a new nested message
                            noMessage += 1
                            endOfLine = statement[matchMessage.end():]
                            matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                            if matchName is not None:
                                # Test to check if message name have any special character. It should not have any special character.
                                # Message should always start with special character.
                                matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b",endOfLine[matchName.start():matchName.end()])
                                self.assertIsNotNone(matchNameConv, file + " in line " + str(i - 1) + ": message name wrong. '" + endOfLine[matchName.start():matchName.end()] + "'")

                    # Search for "enum".
                    matchEnum = re.search(r"\benum\b", statement)

                    if matchEnum is not None:
                        isEnum = True
                        endOfLine = statement[matchEnum.end():]
                        matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                        if matchName is not None:
                            # Test to check presence of invalid special characters
                            matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b", endOfLine[matchName.start():matchName.end()])
                            enumName = self.convert(endOfLine[matchName.start():matchName.end()]) + "_"

                    # Search for a closing brace.
                    matchClosingBrace = re.search("}", statement)
                    if isEnum is True and matchClosingBrace is not None:
                        isEnum = False
                        enumName = ""


    def test_field_name(self):
        ''' Test to check if field names are in lower case. '''

        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                i = 0
                isEnum = False
                enumName = ""
                noMessage = 0
                saveStatement = ""

                for line in fin:
                    i += 1

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

                    if isEnum is False:
                        # Check if not inside an enum.

                        # Search for "message".
                        matchMessage = re.search(r"\bmessage\b", statement)
                        if matchMessage is not None:
                            # a new message or a new nested message
                            noMessage += 1
                            endOfLine = statement[matchMessage.end():]
                            matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                            if matchName is not None:
                                matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b",endOfLine[matchName.start():matchName.end()])

                        elif re.search(r"\bextend\b", statement) is not None:
                            # treat extend as message
                            noMessage += 1
                        else:
                            # Check field names
                            if noMessage > 0:
                                matchName = re.search(r"\b\w[\S]*\b\s*=", statement)

                                if matchName is not None:
                                    checkName = statement[matchName.start():matchName.end() - 1]
                                    self.assertEqual(checkName, checkName.lower(), file + " in line " + str(i) + ": field name wrong. '" + checkName + "' should use lower case")
                                    type = statement.replace(checkName, "")
                                    matchName = re.search(r"\b\w[\S\.]*\s*=", type)

                                    if matchName is not None:
                                        checkType = " " + type[matchName.start():matchName.end() - 1] + " "
                                        # Test to check nested message type
                                        matchNameConv = re.search(r"[ ][a-zA-Z][a-zA-Z0-9]*([\.][A-Z][a-zA-Z0-9]*)*[ ]",checkType)

                        # Search for a closing brace.
                        matchClosingBrace = re.search("}", statement)
                        if noMessage > 0 and matchClosingBrace is not None:
                            noMessage -= 1

                    # Search for "enum".
                    matchEnum = re.search(r"\benum\b", statement)

                    if matchEnum is not None:
                        isEnum = True
                        endOfLine = statement[matchEnum.end():]
                        matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                        if matchName is not None:
                            # Test to check presence of invalid special characters
                            matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b", endOfLine[matchName.start():matchName.end()])
                            enumName = self.convert(endOfLine[matchName.start():matchName.end()]) + "_"

                    # Search for a closing brace.
                    matchClosingBrace = re.search("}", statement)
                    if isEnum is True and matchClosingBrace is not None:
                        isEnum = False
                        enumName = ""

    def test_field_type(self):
        ''' Test to check nested message type. '''

        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                i = 0
                isEnum = False
                enumName = ""
                noMessage = 0
                saveStatement = ""

                for line in fin:
                    i += 1

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

                    if isEnum is False:
                        # Check if not inside an enum.

                        # Search for "message".
                        matchMessage = re.search(r"\bmessage\b", statement)
                        if matchMessage is not None:
                            # a new message or a new nested message
                            noMessage += 1
                            endOfLine = statement[matchMessage.end():]
                            matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                            if matchName is not None:
                                matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b",endOfLine[matchName.start():matchName.end()])

                        elif re.search(r"\bextend\b", statement) is not None:
                            # treat extend as message
                            noMessage += 1
                        else:
                            # Check field names
                            if noMessage > 0:
                                matchName = re.search(r"\b\w[\S]*\b\s*=", statement)
                                if matchName is not None:
                                    checkName = statement[matchName.start():matchName.end() - 1]

                                    # Check field message type (remove field name)
                                    type = statement.replace(checkName, "")
                                    matchName = re.search(r"\b\w[\S\.]*\s*=", type)
                                    if matchName is not None:
                                        checkType = " " + type[matchName.start():matchName.end() - 1] + " "
                                        # Test to check nested message type
                                        matchNameConv = re.search(r"[ ][a-zA-Z][a-zA-Z0-9]*([\.][A-Z][a-zA-Z0-9]*)*[ ]", checkType)

                                        checkType = checkType.strip()
                                        self.assertIsNotNone(matchNameConv, file + " in line " + str(i) + ": field message type wrong. Check: '" + checkType + "'")

                        # Search for a closing brace.
                        matchClosingBrace = re.search("}", statement)
                        if noMessage > 0 and matchClosingBrace is not None:
                            noMessage -= 1

                    # Search for "enum".
                    matchEnum = re.search(r"\benum\b", statement)

                    if matchEnum is not None:
                        isEnum = True
                        endOfLine = statement[matchEnum.end():]
                        matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                        if matchName is not None:
                            # Test to check presence of invalid special characters
                            matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b", endOfLine[matchName.start():matchName.end()])
                            enumName = self.convert(endOfLine[matchName.start():matchName.end()]) + "_"

                    # Search for a closing brace.
                    matchClosingBrace = re.search("}", statement)
                    if isEnum is True and matchClosingBrace is not None:
                        isEnum = False
                        enumName = ""

    def test_field_multiplicity(self):
        ''' Test to check if every field has the multiplicity "repeated" or "optional". '''

        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                i = 0
                isEnum = False
                enumName = ""
                noMessage = 0
                saveStatement = ""

                for line in fin:

                    # Skipping test on multiplicity for protobuf 3.0.0
                    if '"proto3"' in line:
                        break

                    i += 1

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

                    if isEnum is False:
                        # Check if not inside an enum.

                        # Search for "message".
                        matchMessage = re.search(r"\bmessage\b", statement)
                        if matchMessage is not None:
                            # a new message or a new nested message
                            noMessage += 1
                            endOfLine = statement[matchMessage.end():]
                            matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                            if matchName is not None:
                                matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b",endOfLine[matchName.start():matchName.end()])

                        elif re.search(r"\bextend\b", statement) is not None:
                            # treat extend as message
                            noMessage += 1

                        else:
                            # Check field names
                            if noMessage > 0:
                                matchName = re.search(r"\b\w[\S]*\b\s*=", statement)
                                if matchName is not None:
                                    checkName = statement[matchName.start():matchName.end() - 1]

                                    # Check field message type (remove field name)
                                    type = statement.replace(checkName, "")
                                    matchName = re.search(r"\b\w[\S\.]*\s*=", type)
                                    if matchName is not None:
                                        checkType = " " + type[matchName.start():matchName.end() - 1] + " "
                                        # Test to check nested message type
                                        matchNameConv = re.search(r"[ ][a-zA-Z][a-zA-Z0-9]*([\.][A-Z][a-zA-Z0-9]*)*[ ]",checkType)

                                    statement = statement.strip()
                                    self.assertIsNotNone(re.search(r"\boptional\b", type) is None and re.search(r"\brepeated\b",type), file + " in line " + str(i) + ": field multiplicity (\"optional\" or \"repeated\") is missing. Check: '" + statement + "'")

                        # Search for a closing brace.
                        matchClosingBrace = re.search("}", statement)
                        if noMessage > 0 and matchClosingBrace is not None:
                            noMessage -= 1

                    # Search for "enum".
                    matchEnum = re.search(r"\benum\b", statement)

                    if matchEnum is not None:
                        isEnum = True
                        endOfLine = statement[matchEnum.end():]
                        matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                        if matchName is not None:
                            # Test to check presence of invalid special characters
                            matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b", endOfLine[matchName.start():matchName.end()])
                            enumName = self.convert(endOfLine[matchName.start():matchName.end()]) + "_"

                    # Search for a closing brace.
                    matchClosingBrace = re.search("}", statement)
                    if isEnum is True and matchClosingBrace is not None:
                        isEnum = False
                        enumName = ""

    def convert(self, name):
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).upper()

