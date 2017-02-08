'''
Created on Aug 9, 2016

@author: Hector Solano
'''

import re
import ast

STATEMENT = re.compile(ur'(set|jumpt|jump|halt)') # Regular expression to identify key words
#JUMPT = re.compile(ur'(!=|==|>=|<=|>|<)') # Regular expression identify boolean operators


###########################################################################################################
# Class Parser creates an AST according to the grammar rules of the language SIMPLESEM
###########################################################################################################


###########################################################################################################
# The constructor Parser takes a scanner as an argument that contains the list of tokens.
###########################################################################################################
class Parser(object):
    def __init__(self, scanner):
        self.scanner = scanner
        self.nonterminals = []  ### member variable is to assist in debugging
        self.text = ''     ### member variable to assist with debugging
        self.buildText()   ### member variable to assist with debugging
        self.code = []   ### contains a list of statements 
 
###########################################################################################################
# This member function parses a list of tokens according to the SIMPLESEM grammar and return an
# abstract syntax tree
###########################################################################################################  
    def parse(self):
        self.nonterminals.append("Program")
        token = self.scanner.peek()
        while STATEMENT.match(token):
            self.code.append(self.statement())
            if len(self.scanner.tokens) > 0:
                token = self.scanner.peek()
            else:
                token = ''
        return self.code

###########################################################################################################
# This member function parses a list of tokens according to the SIMPLESEM instruction format
###########################################################################################################    
    def statement(self):
        self.nonterminals.append("Statement")
        token = self.scanner.peek()
        astnode = ast.Statement()
        if token == 'set':
            astnode.appendChild(self.set())
        elif token == 'jump':
            astnode.appendChild(self.jump())
        elif token == 'jumpt':
            astnode.appendChild(self.jumpt())
        elif token == 'halt':
            astnode.appendChild(ast.Halt());
            self.scanner.next()
        else:
            print('invalid token Statement: ', token)
        return astnode

###########################################################################################################
# This member function parses a set statement
###########################################################################################################
    def set(self):
        self.nonterminals.append("Set")
        self.scanner.accept('set')
        if self.scanner.accept('write'):
            destination = ast.Write()
        else:
            destination = self.expr()
        self.scanner.accept(',')
        if self.scanner.accept('read'):
            source = ast.Read()
        else:
            source = self.expr()
        return ast.Set(destination, source)


###########################################################################################################
# This member function parses a jump statement
###########################################################################################################      
    def jump(self):
        if self.scanner.accept('jump'):
            node = ast.Jump(self.expr())
        else:
            print('invalid token Jump: ', self.scanner.peek())
        return node
         
###########################################################################################################
# This member function parses a jumpt statement
###########################################################################################################    
    def jumpt(self):
        if self.scanner.accept('jumpt'):
            destination = self.expr()
            if self.scanner.accept(','):
                lhs = self.expr()
                op = self.scanner.next()
                rhs = (self.expr())
                
            else:
                print('invalid token sequence Jumpt: ', self.scanner.peek())
        else:
            print('invalid token sequence Jumpt: ', self.scanner.peek())
        return ast.Jumpt(destination, ast.Op2(op, lhs, rhs))

###########################################################################################################
# This member function parses a expression statement
###########################################################################################################         
    def expr(self):
        node = ast.Expr() 
        node.appendChild(self.term())
        while self.scanner.peek() == '+' or self.scanner.peek() == '-':
            node.appendChild(ast.Op(self.scanner.next(), self.term()))
        return node
  
###########################################################################################################
# This member function parses a term statement and return an abstract syntax tree node
########################################################################################################### 
    def term(self):
        astnode = ast.Term()
        astnode.appendChild(self.factor())
        while self.scanner.peek() == '*' or self.scanner.peek() == '/' or self.scanner.peek() == '%':
            astnode.appendChild(ast.Op(self.scanner.next(), self.term()))
        return astnode

###########################################################################################################
# This member function parses a factor statement and return an abstract syntax tree node
###########################################################################################################     
    def factor(self):
        if self.scanner.accept('D'):
            self.scanner.accept('[')
            node = ast.DataAccess(self.expr())
            self.scanner.accept(']')
        elif self.scanner.accept('('):
            node = self.expr()
            self.scanner.accept(')')
        elif self.isNumber():
            node = (ast.Number(int(self.scanner.next())))
        else:
            print('invalid token sequence Factor: ', self.scanner.peek())
        return ast.Factor(node)
 
# This member function determines if the current token to be parsed in an integer       
    def isNumber(self):
        try:
            int(self.scanner.peek())
            return True
        except ValueError:
            return False

# helper method for debugging  
    def buildText(self):
        for nonterminal in self.nonterminals:
            self.text += nonterminal + '\r\n'
            
