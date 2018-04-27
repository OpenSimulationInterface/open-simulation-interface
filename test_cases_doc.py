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
            if re.search(r"([\s>]|^)#\w",line) is not None:
                print(file + " in line " + str(i) + ": not permitted hash found")
                state = 1


sys.exit(state)
