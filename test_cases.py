import sys
from glob import *

state = 0

for file in glob("*.*"):
    if(file != "test_cases.py"):
        with open(file, "rt") as fin:
            i = 0
            for line in fin:
                i = i + 1

                # Test case 1 is checking if there are illegal tabulators in the code
                if line.find("\t") != -1:
                    print(file + " in line " + str(i) + ": not permitted tab found")
                    state = 1

                # Test case 2 is checking if there are more than the two allowed '/'
                if line.find("///") != -1:
                    print(file + " in line " + str(i) + ": not permitted use of '///' ")
                    state = 1
					
sys.exit(state)