'''
Created on Aug 19, 2016

@author: Hector Solani
'''

##########################################################################################################
# This file contains the class definitions to build an abstract syntax tree
# Each class represents a Non-terminal for the SIMPLESEM grammar
##########################################################################################################


##########################################################################################################
# Class BaseNode is the base class for the AST, all other nodes will inherit from BaseNode
##########################################################################################################

class BaseNode(object):    

    def __init__(self):
        self.children = []   #children is a list of children nodes 


# appendChild method take a AST node and append a node to its list of children
    def appendChild(self,child):
        self.children.append(child)

##########################################################################################################
# Statement node for the AST, inherits from BaseNode
##########################################################################################################
class Statement(BaseNode):pass

##########################################################################################################
# Set node for the AST, inherits from BaseNode
# Set node has to member variables source and destination that emulate CPU registers
# Destination register and Source register
##########################################################################################################

class Set(BaseNode):
    def __init__ (self, destination, source):
        self.destination = destination
        self.source = source


##########################################################################################################
# The class is Write node for the AST, inherits from BaseNode
##########################################################################################################
class Write(BaseNode): pass


##########################################################################################################
# The class is Read node for the AST, inherits from BaseNode
##########################################################################################################
class Read(BaseNode): pass


##########################################################################################################
# The class is Jump node for the AST, inherits from BaseNode
# The Jump node emulates a branch statement
##########################################################################################################
class Jump(BaseNode):
    def __init__(self, destination):
        self.destination = destination


##########################################################################################################
# The class is Jumpt node for the AST, inherits from BaseNode
# The Jumpt node emulates a conditional branch statement
##########################################################################################################
class Jumpt(BaseNode):
    def __init__(self, destination, bool_expr):
        self.destination = destination
        self.bool = bool_expr

##########################################################################################################
# The class is Halt node for the AST, inherits from BaseNode
# The Halt node indicates EOF
##########################################################################################################    
class Halt(BaseNode):pass

##########################################################################################################
# The class is Expr node for the AST, inherits from BaseNode
##########################################################################################################
class Expr(BaseNode): pass
    
 ##########################################################################################################
# The class Term is node for the AST, inherits from BaseNode
##########################################################################################################   
class Term(BaseNode): pass
 
 
##########################################################################################################
# The class Factor is node for the AST, inherits from BaseNode
##########################################################################################################         
class Factor(BaseNode):
        def __init__(self, child):
            self.children = child #Member attribute child
 
##########################################################################################################
# The class DataAccess is node for the AST, inherits from BaseNode
# DataAccess emulates memory
##########################################################################################################         
class DataAccess(BaseNode):
    def __init__(self, child):
            self.children = child

##########################################################################################################
# The class Number is node for the AST, inherits from BaseNode
# the member value is an integer value
##########################################################################################################  
class Number(BaseNode):
    def __init__(self, value):
        self.value = value    
  
##########################################################################################################
# The class Op is node for the AST, inherits from BaseNode.
########################################################################################################## 
class Op(BaseNode):
    def __init__(self, operator, rhs):
        self.op = operator
        self.rhs = rhs
      
##########################################################################################################
# The class Op2 is node for the AST, inherits from BaseNode.
##########################################################################################################         
class Op2(BaseNode):
    def __init__(self, operator, lhs, rhs):
        self.op = operator
        self.rhs = rhs
        self.lhs = lhs


