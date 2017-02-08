'''
Created on Aug 10, 2016

@author: Hector Solano
'''
import re
import sys

##########################################################################################################
# Class Scanner is a constructor, it takes a filename and a regex that identifies tokens for the
# SIMPLESEM language. Scanner produces a list of tokens
########################################################################################################## 

class Scanner:
    def __init__(self, filename, regex):
        self.file = open(filename, 'r')
        self.tokens = []
        self.pattern = re.compile(regex)
        self.index = 0
        self.i = 0
        self.tokenize()
        self.n = len(self.tokens)
        self.file.close()
        
##########################################################################################################
# Member function tokenize scans the file containing the SIMPLESEM source code and builds a list of tokens
# from the SIMPLESEM language
##########################################################################################################
    def tokenize(self):
        pos = 0
        buf = self.file.read()
        token = self.pattern.match(buf)
        while token:
            self.tokens.append(token.group(0).strip())
            pos = len(token.group(0)) + pos
            token = self.pattern.match(buf[pos:])
            

##########################################################################################################
# Member function next return the current token and advances the cursor to the next token.
##########################################################################################################        
    def next(self):
        if self.i < self.n:
            self.i += 1
            return self.tokens[self.i - 1]
        else:
            return ''

##########################################################################################################
# Member function accept takes a token as an argument and if the current token in the cursor
# matches the token argument it, it returns the token and advances the cursor to the next token
# otherwise it return false.
##########################################################################################################     
    def accept(self, token):
        if self.i < self.n and self.tokens[self.i] == token:
            self.i += 1
            return self.tokens[self.i - 1]
        else:
            return False
 
###########################################################################################################
# Member function peek, returns the current token in the cursor without advancing the cursor.
##########################################################################################################    
    def peek(self):
        if self.i < self.n:
            data = self.tokens[self.i]
            return data
        else:
            return ''


###########################################################################################################
# Some code for light testing of the scanner
##########################################################################################################       
if __name__ == '__main__':
    filename = sys.argv[1]
    regex = ur'(\s*(halt|set|write|read|jumpt|jump|!=|\(|\)|==|>=|<=|>|<|\+|-|\*|\/|%|D|\[|\]|[0-9]+|,))'
    inFile = sys.argv[4]
    scanner = Scanner(filename, regex)    