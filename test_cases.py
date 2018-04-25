import sys
import unicodedata
import re
from glob import *

state = 0

for file in glob("*.*"):
    with open(file, "rt") as fin:
        i = 0
        isEnum = False
        enumName = ""
        noMessage = 0
        noComment = 0

        for line in fin:
            i = i + 1

            # --------------------------------------------------------------
            # Test case 1 is checking if there are illegal tabulators in the code
            if line.find("\t") != -1:
                print(file + " in line " + str(i) + ": not permitted tab found")
                state = 1

            # --------------------------------------------------------------
            # Test case 2 is checking if there is an "Umlaut" etc.
            if (sys.version_info >= (3, 0)):
                if line != unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').decode():
                    print(file + " in line " + str(i) + ": a none ASCII char is present")
                    state = 1
            else:
                if line != unicodedata.normalize('NFKD', unicode(line, 'ISO-8859-1')).encode('ASCII', 'ignore'):
                    print(file + " in line " + str(i) + ": a none ASCII char is present")
                    state = 1

            if file.find(".proto") != -1:
                # --------------------------------------------------------------
                # Test case 3 is checking if there are more than the two allowed '/'
                if line.find("///") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '///' ")
                    state = 1

                # --------------------------------------------------------------
                # Test case 4 is checking if there is an other type of comment
                if line.find("/*") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '/*' ")
                    state = 1

                # --------------------------------------------------------------
                # Test case 5 is checking if there is an other type of comment
                if line.find("*/") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '*/' ")
                    state = 1

                # --------------------------------------------------------------

                # Search for comment ("//") and add one more slash character ("/") to the comment
                # block to make Doxygen detect it.
                matchComment = re.search("//", line)
                if matchComment is not None:
                    statement = line[:matchComment.start()]
                else:
                    statement = line

                # --------------------------------------------------------------
                # Test case 6-8 camelcase for enums and check enum name?

                # .
                if isEnum is True:
                    matchName = re.search(r"\b\w[\S:]+\b", statement)
                    if matchName is not None:
                        checkName = statement[matchName.start():matchName.end()]
                        # Test case 6: Check correct name
                        if checkName.find(enumName) != 0:
                            print(file + " in line " + str(i) + ": enum type wrong. '"+checkName+"' should start with '"+enumName+"'")
                            state = 1
                        # Test case 7: Check upper case
                        elif checkName != checkName.upper():
                            print(file + " in line " + str(i) + ": enum type wrong. '"+checkName+"' should use upper case")
                            state = 1

                # Search for "enum".
                matchEnum = re.search(r"\benum\b", statement)
                if matchEnum is not None:
                    isEnum = True
                    endOfLine = statement[matchEnum.end():]
                    matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                    if matchName is not None:
                        # Test case 8: Check name - no special char
                        matchNameConv = re.search(r"\b[A-Z][a-zA-Z0-9]*\b",endOfLine[matchName.start():matchName.end()])
                        if matchNameConv is None:
                            print(file + " in line " + str(i) + ": enum name wrong. '"+endOfLine[matchName.start():matchName.end()]+"'")
                            state = 1
                        enumName = convert(endOfLine[matchName.start():matchName.end()])+"_"

                # Search for a closing brace.
                matchClosingBrace = re.search("}", statement)
                if isEnum is True and matchClosingBrace is not None:
                    isEnum = False
                    enumName = ""

                def convert(name):
                    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
                    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).upper()

                # --------------------------------------------------------------
                # Test case 9 is checking if there is '__'
                if line.find("__") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '__' ")
                    state = 1

                # --------------------------------------------------------------
                # Test case 10-12 check message name, field type and field name
                #
                # Check (nested) messages

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
                            if matchNameConv is None:
                                print(file + " in line " + str(i) + ": message name wrong. '"+endOfLine[matchName.start():matchName.end()]+"'")
                                state = 1
                    else:
                        # Check field names
                        if noMessage > 0:
                            matchName = re.search(r"\b\w[\S]*\b\s*=", statement)
                            if matchName is not None:
                                checkName = statement[matchName.start():matchName.end()-1]
                                # Test case 11: Check lowercase letters for field names
                                if checkName != checkName.lower():
                                    print(file + " in line " + str(i) + ": field name wrong. '"+checkName+"' should use lower case")
                                    state = 1
                                # Check field message type (remove field name)
                                type = statement.replace(checkName, "")
                                matchName = re.search(r"\b\w[\S\.]*\s*=", type)
                                if matchName is not None:
                                    checkType = " "+type[matchName.start():matchName.end()-1]+" "
                                    # Test case 12: Check nested message type
                                    matchNameConv = re.search(r"[ ][a-zA-Z][a-zA-Z0-9]*([\.][A-Z][a-zA-Z0-9]*)*[ ]",checkType)
                                    if matchNameConv is None:
                                        print(file + " in line " + str(i) + ": field message type wrong. Check: '"+checkType+"'")
                                        state = 1

                    # Search for a closing brace.
                    matchClosingBrace = re.search("}", statement)
                    if noMessage > 0 and matchClosingBrace is not None:
                        noMessage -= 1

                # --------------------------------------------------------------
                # Test case 13 is checking if comment is min. 2 lines
                if line.find("//") != -1:
                    noComment += 1;
                else:
                    if noComment == 1:
                        print(file + " in line " + str(i-1) + ": short comment - min. 2 lines.")
                        state = 1
                    noComment = 0

                # --------------------------------------------------------------


sys.exit(state)

