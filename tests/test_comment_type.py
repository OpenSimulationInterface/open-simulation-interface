import sys
import unicodedata
import re
from glob import *
import unittest


class TestCommentType(unittest.TestCase):
    ''' Test class for mandatory new line. ''' 

    def test_brief_necessity(self):
        ''' Test the necessity of "brief" comment. '''

        for file in glob("*.proto"):
            with open(file, "rt") as fin:
                i = 0
                noMessage = 0
                noComment = 0
                hasBrief = False
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

                    statement = statement.strip()
                    # Test to check if '\\brief' is appended in comment section for short comments.
                    if matchComment is not None:
                        noComment += 1;
                        if comment.find("\\brief") != -1:
                            hasBrief = True
                    
                    elif len(saveStatement) == 0:
                        if re.search(r"\bmessage\b", statement) is not None or re.search(r"\bextend\b",statement) is not None:
                            self.assertTrue(hasBrief, file + " in line " + str(i - 1) + ": \\brief section in comment is missing for: '" + statement + "'")

                        elif hasBrief:
                            self.assertFalse(hasBrief, file + " in line " + str(i - 1) + ": \\brief section in comment is not necessary for: '" + statement + "'")

                        noComment = 0
                        hasBrief = False



    def test_min_two_lines(self):
        ''' Test to check if short comment is of minimum two lines. '''

        for file in glob("*.proto"):
            with open(file, "rt") as fin:
                i = 0
                isEnum = False
                noMessage = 0
                noComment = 0
                hasBrief = False
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

                    # Test to check if '\\brief' is appended in comment section for short comments.
                    if matchComment is not None:
                        noComment += 1;
                        if comment.find("\\brief") != -1:
                            hasBrief = True

                    elif len(saveStatement) == 0:
                        self.assertNotEqual(noComment, 1, file + " in line " + str(i - 1) + ": short comment - min. 2 lines.")
                        noComment = 0
                        hasBrief = False


    def test_comment_existence(self):
        ''' Test to check if every message, extend , statement or enum has a comment. '''

        for file in glob("*.proto"):

            with open(file, "rt") as fin:
                i = 0
                isEnum = False
                noMessage = 0
                noComment = 0
                hasBrief = False
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
                                # Test case 10: Check name - no special char -
                                # start with a capital letter
                                matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b",endOfLine[matchName.start():matchName.end()])

                        elif re.search(r"\bextend\b", statement) is not None:
                            # treat extend as message
                            noMessage += 1
                        else:
                            # Check field names
                            if noMessage > 0:
                                matchName = re.search(r"\b\w[\S]*\b\s*=", statement)
                                if matchName is not None:
                                    checkName = statement[matchName.start():matchName.end()-1]

                                    # Check field message type (remove field name)
                                    type = statement.replace(checkName, "")
                                    matchName = re.search(r"\b\w[\S\.]*\s*=", type)
                                    if matchName is not None:
                                        checkType = " "+type[matchName.start():matchName.end()-1]+" "
                                        # Test case 12: Check nested message type
                                        matchNameConv = re.search(r"[ ][a-zA-Z][a-zA-Z0-9]*([\.][A-Z][a-zA-Z0-9]*)*[ ]",checkType)

                        # Search for a closing brace.
                        matchClosingBrace = re.search("}", statement)
                        if noMessage > 0 and matchClosingBrace is not None:
                            noMessage -= 1


                    # Test to check if '\\brief' is appended in comment section for short comments.
                    if matchComment is not None:
                        noComment += 1
                        if comment.find("\\brief") != -1:
                            hasBrief = True

                    elif len(saveStatement) == 0:

                        statement = statement.strip()

                        if re.search(r"\bmessage\b", statement) is not None or re.search(r"\bextend\b",statement) is not None or re.search(r"\benum\b", statement) is not None:

                            self.assertNotEqual(noComment, 0, file + " in line " + str(i - 1) + ": comment is missing for: '" + statement + "'")

                        if noMessage > 0 or isEnum == True:
                            if statement.find(";") != -1:
                                self.assertNotEqual(noComment, 0, file + " in line " + str(i) + ": comment is missing for: '" + statement + "'")

                        noComment = 0
                        hasBrief = False

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

    def convert(self, name):
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).upper()