import symtable

table = symtable.SymbolTable()

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, symbomtable):
        pass

class IntVal(Node):
    def __init__(self,value):
        super().__init__(value, None)
        
    def Evaluate(self, symbomtable):
        return [self.value, "Int"]

class StringVal(Node):
    def __init__(self,value):
        super().__init__(value, None)
        
    def Evaluate(self, symbomtable):
        return [self.value, "String"]

class BoolVal(Node):
    def __init__(self,value):
        super().__init__(value, None)
        
    def Evaluate(self, symbomtable):
        if self.value == "false":
            return [0, "Bool"]
        elif self.value == "true":
            return [1, "Bool"]

class BinOp(Node):
    def __init__(self,value):
        super().__init__(value,[None, None])
    
    def Evaluate(self, symbomtable):
        if self.value == "-":
            c0 = self.children[0].Evaluate(symbomtable)
            c1 = self.children[1].Evaluate(symbomtable)
            if c0[0] == "String" or c1[0] == "String":
                raise NameError(f'Incompatible operation - with {c0[0]} and {c1[0]}')
            return [c0[1] - c1[1], "Int"]

        elif self.value == "+":
            c0 = self.children[0].Evaluate(symbomtable)
            c1 = self.children[1].Evaluate(symbomtable)
            if(c0[1] != 'String' and c1[1] != 'String'):
                return [c0[0] + c1[0], 'Int']
            else:
                raise NameError(f'Incompatible operation + with {c0[0]} and {c1[0]}')

        elif self.value == "*":
            c0 = self.children[0].Evaluate(symbomtable)
            c1 = self.children[1].Evaluate(symbomtable)
            if c0[1] == "String" or c1[1] == "String":
                if c0[1] == "Bool":
                    if c0[0] == 1:
                        c0[0] = "true"
                    else:
                        c0[0] = "false"
                if c1[1] == "Bool":
                    if c1[0] == 1:
                        c1[0] = "true"
                    else:
                        c1[0] = "false"
                return [str(c0[0]) + str(c1[0]), "String"]        
            return [c0[0] * c1[0], "Int"]

        elif self.value == "/":
            c0 = self.children[0].Evaluate()
            c1 = self.children[1].Evaluate()
            if c0[1] == "String" or c1[1] == "String":
                raise NameError(f'Incompatible operation / with {c0[1]} and {c1[1]}')
            return [int(c0[0] / c1[0]), "Int"]

        elif self.value == "&&":
            c0 = self.children[0].Evaluate()
            c1 = self.children[1].Evaluate()

            if c0[1] == "String" or c1[1] == "String":
                raise NameError(f'Incompatible operation && with {c0[1]} and {c1[1]}')
            if c0[0] and c1[0]:
                return [1, "Bool"]
            else:
                return [0, "Bool"]

        elif self.value == "||":
            c0 = self.children[0].Evaluate()
            c1 = self.children[1].Evaluate()

            if c0[1] == "String" or c1[1] == "String":
                raise NameError(f'Incompatible operation || with {c0[1]} and {c1[1]}')
            if c0[0] or c1[0]:
                return [1, "Bool"]
            else:
                return [0, "Bool"]

        elif self.value == ">":
            c0 = self.children[0].Evaluate()
            c1 = self.children[1].Evaluate()

            if c0[1] == "String" or c1[1] == "String":
                raise NameError(f'Incompatible operation > with {c0[1]} and {c1[1]}')
            if c0[0] > c1[0]:
                return [1, "Bool"]
            else:
                return [0, "Bool"]

        elif self.value == "<":
            c0 = self.children[0].Evaluate()
            c1 = self.children[1].Evaluate()

            if c0[1] == "String" or c1[1] == "String":
                raise NameError(f'Incompatible operation > with {c0[1]} and {c1[1]}')
            if c0[0] < c1[0]:
                return [1, "Bool"]
            else:
                return [0, "Bool"]

        elif self.value == "==":
            if self.children[0].Evaluate()[0] == self.children[1].Evaluate()[0]:
                return [1, "Bool"]
            else:
                return [0, "Bool"]

class UnOp(Node):
    def __init__(self,value):
        super().__init__(value,[None])

    def Evaluate(self, symbomtable):
        c0 = self.children[0].Evaluate(symbomtable)
        if self.value == "-":
            return [-c0[0], "Int"]
        elif self.value == "+":
            return [c0[0], "Int"]
        elif self.value == "!":
            if not c0[0]:
                return [1, "Bool"]
            else:
                return [0, "Bool"]

class NoOp(Node):
    def __init__(self):
        self.value = None
    def Evaluate(self, symbomtable):
        pass  

class Identifier(Node):
    def __init__(self, value):
        self.value = value
    
    def Evaluate(self, symbomtable):
        return symbomtable.getter_symbol(self.value)

class Print(Node):
    def __init__(self):
        super().__init__(None,[None])
    
    def Evaluate(self, symbomtable):
        res = self.children[0].Evaluate(symbomtable)
        if res[1] == "BOOL":
            if res[0] == 1:
                print("true")
            else:
                print("false")
        else:
            print(res[1])

class Assigment(Node):
    def __init__(self):
        super().__init__(None,[None, None])
    
    def Evaluate(self, symbomtable):
        c1 = self.children[1].Evaluate(symbomtable)
        symbolType = symbomtable.getter_type(self.children[0].value)
        if(c1[1] == symbolType):
            symbomtable.setter_symbol(self.children[0].value, c1[0])
        else:
            raise NameError(f'Type and value are not igual {c1[1]} and {symbolType}')

class AssigmentType(Node):
    def __init__(self):
        self.children = [None, None]

    def Evaluate(self, symboltable):
        symboltable.setter_type(self.children[0].value, self.children[1])
        
class Statement(Node):
    def __init__(self):
        super().__init__(None, [])
    
    def Evaluate(self, symbomtable):
        rv = symbomtable.getter_return()[0]
        i = 0
        while(rv == None and i < len(self.children)):
            self.children[i].Evaluate(symbomtable)
            rv = symbomtable.getter_return()[0]
            i = i + 1

class Readline(Node):
    def __init__(self):
        self.value = None
    
    def Evaluate(self, symbomtable):
        return [int(input()), "Int"]

class While(Node):
    def __init__(self):
        super().__init__(None,[None, None])
    
    def Evaluate(self, symbomtable):
        while self.children[0].Evaluate(symbomtable)[0]:
            self.children[0].Evaluate(symbomtable)

class If(Node):
    def __init__(self):
        super().__init__(None,[None, None, None])
    
    def Evaluate(self, symbomtable):
        if (self.children[0].Evaluate(symbomtable)[1] != "String"):    
            if (self.children[0].Evaluate(symbomtable)[0]):
                self.children[1].Evaluate(symbomtable)
            else:
                if self.children[2]:
                    self.children[2].Evaluate(symbomtable)
        else:
            raise NameError("Stderr string in IF")

class Else(Node):
    def __init__(self):
        self.children[None]

    def Evaluate(self, symboltable):
        return self.children[0].Evaluate(symboltable)

class FunctionDeclaration(Node):
    def __init__(self, value, typ):
        self.typ = typ
        self.value = value
        self.children = []

    def Evaluate(self, symbolTable):
        table.setter_function(self.value, self, self.typ)

class Return(Node):
    def __init__(self):
        self.children = [None]

    def Evaluate(self, symbolTable):
        symbolTable.setter_return(self.children[0].Evaluate(symbolTable)[0], self.children[0].Evaluate(symbolTable)[1])

class FunctionCall(Node):
    def __init__(self, value):
        self.children = []
        self.value = value

    def Evaluate(self, symbolTable):
        function = table.getter_function(self.value)
        size = len(function[0].children)-1
        
        if size != len(self.children):
            raise NameError('Number of arguments doenst match')
        else:
            symbolTableTemp = symtable.SymbolTable()
            
            for i in range(size):
                c1Evaluate = self.children[i].Evaluate(symbolTable)
                value = function[0].children[i][0]
                typeFunction = function[0].children[i][1]
                if(typeFunction != c1Evaluate[1]):
                    raise NameError(f'Argument {typeFunction} type is different then {c1Evaluate[1]}')
                else:
                    symbolTableTemp.setter_type(value, typeFunction)
                    symbolTableTemp.setter_symbol(value, c1Evaluate[0])
            
            function[0].children[-1].Evaluate(symbolTableTemp)
            returno = symbolTableTemp.getter_return()
            
            if(returno[1] == function[1]):
                return returno
            else:
                raise NameError('Return and Function are different')