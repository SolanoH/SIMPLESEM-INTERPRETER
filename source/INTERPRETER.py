'''
Created on Aug 10, 2016

@author: Hector Solano
'''
import sys
from scanner import Scanner
from parser import Parser
import ast 


INPUTFILE = 'input.txt'  #Default input read  file
##############################################################################################################
### Generic node visitor pattern to append node name to visit method.
##############################################################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit{} method'.format(type(node).__name__))
        
        
##############################################################################################################
### SIMPLESEM is an abstract semantic processor that is based on the Von Neumann model of the fetch-execute cycle.
##############################################################################################################     
class SimplesemInterpreter(NodeVisitor):
    def __init__(self, fd, code):
        self.data = [0]*100     # Holds data for the SIMPLESEM interpreter
        self.code = code        # Holds code to be interpreted
        self.run_bit = True
        self.PC = 0             # Instruction Pointer  
        self.IR = None          # Instruction  
        
        # A dictionary to map functions calls to operators.
        self.opSelection = {'!=': self.notEqual, '==': self.Equal, '<=': self.lessThanEqual,
                             '>=': self.graterThanEqual, '<': self.lessThan, '>': self.graterThan, '+': self.add,
                              '-': self.sub, '*': self.mult, '/': self.div, '%': self.mod}
        
        self.readFile = open(INPUTFILE, 'r') # inputfile
        self.writeFile = open(fd, 'w') # output file


##############################################################################################################
### Member function read(self), reads input from a file.
##############################################################################################################     
    def read(self):
        data = self.readFile.readline().strip()
        return int(data)

##############################################################################################################
### Member function write(self, value), writes to a file.
##############################################################################################################     
    def write(self, value):
        self.writeFile.write(str(value).strip() + '\r\n')

##############################################################################################################
### Member function fetch(self), gets the next instruction to be interpreted.
##############################################################################################################      
    def fetch(self):
        self.IR = self.code[self.PC]
    
##############################################################################################################
### Member function increment(self), increments the instruction address pointer.
##############################################################################################################     
    def increment(self):
        self.PC = self.PC + 1

##############################################################################################################
### Member function execute, interprets the current instruction
##############################################################################################################        
    def execute(self):
        self.visit(self.IR)

##############################################################################################################
### The member function interpretCode(self), begins the fetch-increment-execute cycle.
##############################################################################################################              
    def interpretCode(self):
        while self.run_bit:
            self.fetch()
            self.increment()
            self.execute()
        
        self.writeMemoryToFile()
        self.writeFile.close()
        self.readFile.close()

##############################################################################################################
### Member function writeMemoryToFile(self), writes the current state of the memory cells to a file.
##############################################################################################################      
    def writeMemoryToFile(self):  
        line = 0;
        self.writeFile.write('Data Segment Contents\r\n')
        for value in self.data:
            self.writeFile.write(str(line) + ': ' + str(value) + '\r\n')
            line += 1        

##############################################################################################################
### Member function visitStatement(self, node) takes a parameter node, which is an AST node  Statement (instructions) 
### and maps the member function call visit to all the children nodes of Statement.
##############################################################################################################  
    def visitStatement(self, node):
        map(self.visit, node.children)
        
        
##############################################################################################################
### Member function visitSet(self, node) executes the set instruction according to the SIMPLESEM language definition.
##############################################################################################################     
    def visitSet(self, node):
        if isinstance(node.destination, ast.Write):
            self.write(self.visit(node.source))
        else:
            self.data[self.visit(node.destination)] = self.visit(node.source)
 
    
##############################################################################################################
### Member function visitJump(self, node) takes one parameter, jumps performs an unconditional jump to the given address.
##############################################################################################################          
    def visitJump(self, node):
        dest = self.visit(node.destination)
        self.PC = dest
 
##############################################################################################################
### Member function visitRead(self, node) reads integer string from file and return an integer.
##############################################################################################################             
    def visitRead(self, node):
        return int(self.read())

##############################################################################################################
### Member function visitjumpt(self, node) jumps to the given destination if the boolean
### condition is true.
##############################################################################################################  
    def visitJumpt(self, node):
        if self.visit(node.bool):
            self.PC = self.visit(node.destination)

##############################################################################################################
### Member function visitHalt(self, node) sets the run_bit to false to stop the fetch-execute cycle.
##############################################################################################################      
    def visitHalt(self, node):
        self.run_bit = False
    
##############################################################################################################
### Member function visitExpr(self, node) resolves the production <Expr> -> <Term> {(+|-) <Term>}
### and return the left hand side operant
##############################################################################################################      
    def visitExpr(self, node):
        lhs = self.visit(node.children[0])
        index = 1
        while index < len(node.children):
            lhs = self.opSelection[node.children[index].op](lhs, self.visit(node.children[index].rhs))
            index += 1
        return lhs

##############################################################################################################
# Member function visitTerm(self, node) resolves the production  <Term> -> <Factor> {( * | / | % ) <Factor>}
# and return the left hand side operant
##############################################################################################################             
    def visitTerm(self, node):
        lhs = self.visit(node.children[0])
        index = 1
        while index < len(node.children):
            lhs = self.opSelection[node.children[index].op](lhs, self.visit(node.children[index].rhs))
            index += 1
        return lhs
 
##############################################################################################################
# Member function visitFactor resolves the production <Factor> -> <Number> | D[ <Expr> ] | ( <Expr> )
##############################################################################################################      
    def visitFactor(self, node):
        return self.visit(node.children)
 
##############################################################################################################
# Member function visitDataAccess returns a value in memory
##############################################################################################################    
    def visitDataAccess(self, node):
        return self.data[self.visit(node.children)]

##############################################################################################################
# Member function visitOp assist visitTerm and visitFactor perform arithmetic operations
##############################################################################################################       
    def visitOp(self, node):
        return self.visit(node)   

##############################################################################################################
# Member function visitOp2 assist visitJumpt perform arithmetic operations
##############################################################################################################           
    def visitOp2(self, node):
        return self.opSelection[node.op](self.visit(node.lhs), self.visit(node.rhs))          

##############################################################################################################
# Member functions return an integer according to production <Number> -> 0 | ( 1 .. 9 ){ 0 .. 9 }
##############################################################################################################     
    def visitNumber(self, node):
        return node.value

##############################################################################################################
### The following are helper member functions to perform arithmetic and boolean operations 
##############################################################################################################     
    def notEqual(self,lhs,rhs):
        return lhs != rhs
    
    def Equal(self,lhs,rhs):
        return lhs == rhs
    
    def graterThanEqual(self,lhs,rhs):
        return lhs >= rhs
    
    def lessThanEqual(self,lhs,rhs):
        return lhs <= rhs
    
    def graterThan(self,lhs,rhs):
        return lhs > rhs
    
    def lessThan(self,lhs,rhs):
        return lhs < rhs
    
    def add(self,lhs,rhs):
        return lhs + rhs
    
    def sub(self,lhs,rhs):
        return lhs - rhs
    
    def mult(self,lhs,rhs):
        return lhs * rhs
    
    def div(self,lhs,rhs):
        return lhs / rhs
    
    def mod(self,lhs,rhs):
        return lhs % rhs
    
    
            
if __name__ == '__main__':
    regex = ur'(\s*(halt|set|write|read|jumpt|jump|!=|\(|\)|==|>=|<=|>|<|\+|-|\*|\/|%|D|\[|\]|[0-9]+|,))'
    inFile = sys.argv[1]
    fd = inFile + '.out'
    scanner = Scanner(inFile, regex)
    parser = Parser(scanner)
    code = parser.parse()
    SIMPLESEM = SimplesemInterpreter(fd, code)
    SIMPLESEM.interpretCode()
    
