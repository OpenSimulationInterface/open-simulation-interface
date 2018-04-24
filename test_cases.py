import sys
import unicodedata
import re
from glob import *

state = 0

for file in glob("*.*"):
    if(file != "test_cases.py") and (file != "setup.py"):
        with open(file, "rt") as fin:
            i = 0
            isEnum = False
            enumName = ""
            for line in fin:
                i = i + 1

                # --------------------------------------------------------------
                # Test case 1 is checking if there are illegal tabulators in the code
                if line.find("\t") != -1:
                    print(file + " in line " + str(i) + ": not permitted tab found")
                    state = 1

                # --------------------------------------------------------------
                # Test case 2 is checking if there are more than the two allowed '/'
                if line.find("///") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '///' ")
                    state = 1

                # --------------------------------------------------------------
                # Test case 3 is checking if there is an other type of comment
                if line.find("/*") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '/*' ")
                    state = 1

                # --------------------------------------------------------------
                # Test case 4 is checking if there is an other type of comment
                if line.find("*/") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '*/' ")
                    state = 1

                # --------------------------------------------------------------
                # Test case 5 is checking if there is an "Umlaut" etc.
                if (sys.version_info > (3, 0)):
                    if line != unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').decode():
                        print(file + " in line " + str(i) + ": a none ASCII char is present")
                        state = 1
                else:
                    if line != unicodedata.normalize('NFKD', line).encode('ASCII', 'ignore').decode('ASCII'):
                        print(file + " in line " + str(i) + ": a none ASCII char is present")
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
                # Test case 6/7 camelcase for enums? 
                
                # Search again for semicolon if we have detected an enum, and replace semicolon with comma.
                if isEnum is True:
                    matchName = re.search(r"\b\w[\S:]+\b", statement);
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
                    matchName = re.search(r"\b\w[\S:]+\b", endOfLine);
                    if matchName is not None:
                        enumName = convert(endOfLine[matchName.start():matchName.end()])+"_"
        
                # Search for a closing brace.
                matchClosingBrace = re.search("}", statement)
                if isEnum is True and matchClosingBrace is not None:
                    isEnum = False
                    enumName = ""

                # --------------------------------------------------------------
                # Test case 8 is checking if there is '__'
                if line.find("__") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '__' ")
                    state = 1

                # --------------------------------------------------------------

                
    def convert(name):
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).upper()

sys.exit(state)

