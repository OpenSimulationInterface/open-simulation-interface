import sys
import unicodedata
import re
from glob import *

state = 0

for file in glob("doc/html/*.htm*"):
    with open(file, "rt") as fin:
        i = 0

        for line in fin:
            i = i + 1
            
            # --------------------------------------------------------------
            # Test case 1 is checking if there are illegal hash chars in the
            # documentation. -> doxygen link not found.
            matchHash = re.search(r"([\s>]|^)#\w(\S)*",line)
            if matchHash is not None:
                print(file + " in line " + str(i) + ": not permitted hash found. Search for: '"+line[matchHash.start():matchHash.end()])
                state = 1

            # --------------------------------------------------------------
            # Test case 2 is checking if there are slash triplets in the
            # documentation. -> doxygen didn't interpret something properly.
            matchHash = re.search(r"([\s>]|^)///\s*",line)
            if matchHash is not None:
                print(file + " in line " + str(i) + ": not permitted slash triplet found. Search for: '"+line[matchHash.start():matchHash.end()])
                state = 1

            # --------------------------------------------------------------
            # Test case 3 is checking if there are backslash triplets in the
            # documentation. -> doxygen didn't interpret something properly.
            matchHash = re.search(r"([\s>]|^)\\\\\\\s*",line)
            if matchHash is not None:
                print(file + " in line " + str(i) + ": not permitted slash triplet found. Search for: '"+line[matchHash.start():matchHash.end()])
                state = 1

sys.exit(state)
