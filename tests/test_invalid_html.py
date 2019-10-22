import sys
import unicodedata
import re
from glob import *
import unittest


class TestInvalidHtml(unittest.TestCase):
    """ Test class for invalid html comment. """

    def test_invalid_slash(self):
        ''' Test case to check invalid slash in htmlonly sections '''
        for file in glob("*.proto"):
            with open(file, "rt") as fin:
                i = 0
                htmlblock = False
                saveStatement = ""

                for line in fin:
                    i += 1

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

                    # Test case is checking comment and html tags
                    if matchComment is not None:
                        htmlComment = ""
                        htmlFreeComment = comment
                        if htmlblock is False:
                            matchHTMLOnly = re.search(r"\\htmlonly", comment)
                            if matchHTMLOnly is not None:

                                htmlComment = comment[matchHTMLOnly.end():]
                                htmlFreeComment = comment[:matchHTMLOnly.start()]
                                htmlblock = True
                        else:
                            htmlComment = comment
                            htmlFreeComment = ""

                        if htmlblock is True:
                            matchEndHTMLOnly = re.search(r"\\endhtmlonly", htmlComment)
                            if matchEndHTMLOnly is not None:
                                htmlFreeComment = htmlFreeComment + htmlComment[matchEndHTMLOnly.end():]
                                htmlComment = htmlComment[:matchEndHTMLOnly.start()]
                                htmlblock = False

                        # Test case to check html tags only in htmlonly sections
                        self.assertEqual(htmlComment.find("\\"), -1, file + " in line " + str(i) + ": doxygen comment \\.. reference found: '" + htmlComment + "'")


    def test_invalid_hash(self):
        ''' Test case to check invalid # in htmlonly sections '''
        for file in glob("*.proto"):
            with open(file, "rt") as fin:
                i = 0
                htmlblock = False
                saveStatement = ""

                for line in fin:
                    i += 1

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

                    # Test case is checking comment and html tags
                    if matchComment is not None:
                        htmlComment = ""
                        htmlFreeComment = comment
                        if htmlblock is False:
                            matchHTMLOnly = re.search(r"\\htmlonly", comment)
                            if matchHTMLOnly is not None:

                                htmlComment = comment[matchHTMLOnly.end():]
                                htmlFreeComment = comment[:matchHTMLOnly.start()]
                                htmlblock = True
                        else:
                            htmlComment = comment
                            htmlFreeComment = ""

                        if htmlblock is True:
                            matchEndHTMLOnly = re.search(r"\\endhtmlonly", htmlComment)
                            if matchEndHTMLOnly is not None:
                                htmlFreeComment = htmlFreeComment + htmlComment[matchEndHTMLOnly.end():]
                                htmlComment = htmlComment[:matchEndHTMLOnly.start()]
                                htmlblock = False

                        self.assertEqual(htmlComment.find("#"), -1, file + " in line " + str(i) + ": doxygen comment #.. reference found: '" + htmlComment + "'")
                        

    def test_invalid_at(self):
        ''' Test case to check invalid @ in comments '''
        for file in glob("*.proto"):
            with open(file, "rt") as fin:
                i = 0
                htmlblock = False
                saveStatement = ""

                for line in fin:
                    i += 1

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

                    # Test case is checking comment and html tags
                    if matchComment is not None:
                        htmlComment = ""
                        htmlFreeComment = comment
                        if htmlblock is False:
                            matchHTMLOnly = re.search(r"\\htmlonly", comment)
                            if matchHTMLOnly is not None:

                                htmlComment = comment[matchHTMLOnly.end():]
                                htmlFreeComment = comment[:matchHTMLOnly.start()]
                                htmlblock = True
                        else:
                            htmlComment = comment
                            htmlFreeComment = ""

                        if htmlblock is True:
                            matchEndHTMLOnly = re.search(r"\\endhtmlonly", htmlComment)
                            if matchEndHTMLOnly is not None:
                                htmlFreeComment = htmlFreeComment + htmlComment[matchEndHTMLOnly.end():]
                                htmlComment = htmlComment[:matchEndHTMLOnly.start()]
                                htmlblock = False

                        self.assertEqual(comment.find("@"), -1, file + " in line " + str(i) + ": @ tag found (please replace with \\): '" + htmlFreeComment + "'")
 

    def test_no_endhtmlonly(self):
        ''' Test case to check no \endhtmlonly in comments '''
        for file in glob("*.proto"):
            with open(file, "rt") as fin:
                i = 0
                htmlblock = False
                saveStatement = ""

                for line in fin:
                    i += 1

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

                    # Test case is checking comment and html tags
                    if matchComment is not None:
                        htmlComment = ""
                        htmlFreeComment = comment
                        if htmlblock is False:
                            matchHTMLOnly = re.search(r"\\htmlonly", comment)
                            if matchHTMLOnly is not None:

                                htmlComment = comment[matchHTMLOnly.end():]
                                htmlFreeComment = comment[:matchHTMLOnly.start()]
                                htmlblock = True
                        else:
                            htmlComment = comment
                            htmlFreeComment = ""

                        if htmlblock is True:
                            matchEndHTMLOnly = re.search(r"\\endhtmlonly", htmlComment)

                            if matchEndHTMLOnly is not None:
                                htmlFreeComment = htmlFreeComment + htmlComment[matchEndHTMLOnly.end():]
                                htmlComment = htmlComment[:matchEndHTMLOnly.start()]
                                htmlblock = False

                    elif htmlblock:
                        self.assertFalse(htmlblock, file + " in line " + str(i - 1) + ": doxygen comment html section without endhtmlonly")
                        htmlblock = False

                    