import re
import glob
import unittest
import yaml

PROTO_FILES = glob.glob("*.proto")

class TestRules(unittest.TestCase):
    """ Test class for units documentation. """

    def test_rules_compliance(self):
        ''' Test rule compliance syntax of proto files. '''

        with open(r'rules.yml') as rules_file:
            RULES_DICT = yaml.load(rules_file, Loader=yaml.BaseLoader)
        
        for file in PROTO_FILES:
            with open(file, "rt") as fin, self.subTest(file=file):
                line_number = 0
                numMessage = 0
                lineruleCount = 0
                foundruleCount = 0
                saveStatement = ""
                isEnum = False

                for line in fin:
                    line_number += 1

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

                    # Search for "message".
                    matchMessage = re.search(r"\bmessage\b", statement)
                    if matchMessage is not None:
                        # a new message or a new nested message
                        numMessage += 1
                        self.assertFalse(foundruleCount > 0 or lineruleCount > 0, file + f" in line {str(line_number-1)}: message should not have rules for '{statement.strip()}'")
                        endOfLine = statement[matchMessage.end():]
                        matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                        
                    elif re.search(r"\bextend\b", statement) is not None:
                        # treat extend as message
                        numMessage += 1
                    else:
                        # Check field names
                        if numMessage > 0:
                            matchName = re.search(r"\b\w[\S]*\b\s*=", statement)
                            if matchName is not None:
                                checkName = statement[matchName.start():matchName.end()-1]
                                # Check field message type (remove field name)
                                type = statement.replace(checkName, "")
                                matchName = re.search(r"\b\w[\S\.]*\s*=", type)

                    if isEnum:
                        matchName = re.search(r"\b\w[\S:]+\b", statement)
                        if matchName is not None:
                            checkName = statement[matchName.start():matchName.end()]
                            self.assertFalse(foundruleCount > 0 or lineruleCount > 0, file + f" in line {str(line_number-1)}: enum field should not have rules for '{statement.strip()}'")

                    # Search for "enum".
                    matchEnum = re.search(r"\benum\b", statement)
                    if matchEnum is not None:
                        isEnum = True
                        endOfLine = statement[matchEnum.end():]
                        matchName = re.search(r"\b\w[\S]*\b", endOfLine)
                        if matchName is not None:
                            self.assertFalse(foundruleCount > 0 or lineruleCount > 0, file + f" in line {str(line_number-1)}: enum should not have rules for '{statement.strip()}'")

                    # Search for a closing brace.
                    matchClosingBrace = re.search("}", statement)
                    if numMessage > 0 and matchClosingBrace is not None:
                        numMessage -= 1

                    if isEnum is True and matchClosingBrace is not None:
                        isEnum = False

                    if matchComment is not None:
                        if re.search(r"^[ ]\\\bendrules\b$", comment) is not None:
                            endRule = True

                        if re.search(r"^[ ]\\\brules\b$", comment) is not None:
                            hasRule = True
                            lineruleCount = 0
                            foundruleCount = 0

                        if not endRule and comment != '':
                            for rulename, ruleregex in RULES_DICT.items():
                                if re.search(ruleregex, comment):
                                    foundruleCount += 1

                    elif len(saveStatement) == 0:
                        if numMessage > 0:
                            if statement.find(";") != -1:
                                statement = statement.strip()
                                self.assertFalse(hasRule and lineruleCount != foundruleCount and endRule and lineruleCount-foundruleCount-1>0, file + " in line " + str(line_number) + ": "+str(lineruleCount-foundruleCount-1)+" defined rule(s) does not exists for: '"+statement+"'")
                                self.assertFalse(hasRule and not endRule, file + " in line " + str(line_number) + ": \\endrules statement does not exists for: '"+statement+"'. Check spacing and rule syntax.")
                                self.assertFalse(not hasRule and endRule, file + " in line " + str(line_number) + ": \\rules statement does not exists for: '"+statement+"'. Check spacing and rule syntax.")
                                self.assertFalse(not hasRule and not endRule and lineruleCount < foundruleCount, file + " in line " + str(line_number) + ": rules found but no statements (\\rules and \\endrules) around it for: '"+statement+"'")
                                lineruleCount = 0
                                foundruleCount = 0

                        hasRule = False
                        endRule = False

                    if hasRule and not endRule or not hasRule and endRule:
                        lineruleCount += 1

if __name__ == '__main__':
    unittest.main()