import symtable

table = symtable.SymbolTable()

class Node:
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self):
        pass

class IntVal(Node):
    def __init__(self,value):
        super().__init__(value, None)
        
    def Evaluate(self):
        return ["INT", self.value]

class StringVal(Node):
    def __init__(self,value):
        super().__init__(value, None)
        
    def Evaluate(self):
        return ["STRING", self.value]

class BoolVal(Node):
    def __init__(self,value):
        super().__init__(value, None)
        
    def Evaluate(self):
        if self.value == "false":
            return ["BOOL", 0]
        elif self.value == "true":
            return ["BOOL", 1]

class BinOp(Node):
    def __init__(self,value,children):
        super().__init__(value,children)
    
    def Evaluate(self):
        if self.value == "-":
            c0 = self.children[0].Evaluate()
            c1 = self.children[1].Evaluate()
            if c0[0] == "STRING" or c1[0] == "STRING":
                raise NameError(f'Incompatible operation - with {c0[0]} and {c1[0]}')
            
            return ["INT", self.children[0].Evaluate()[1] - self.children[1].Evaluate()[1]]

        elif self.value == "+":
            c0 = self.children[0].Evaluate()
            c1 = self.children[1].Evaluate()
            if c0[0] == c1[0]:
                return [c0[0], c0[1] + c1[1]]
            elif c0[0] == "STRING" or c1[0] == "STRING":
                raise NameError(f'Incompatible operation + with {c0[0]} and {c1[0]}')
            else:
                return ["INT", c0[1] + c1[1]]

        elif self.value == "*":
            c0 = self.children[0].Evaluate()
            c1 = self.children[1].Evaluate()
            if c0[0] == "STRING" or c1[0] == "STRING":
                if c0[0] == "BOOL":
                    if c0[1] == 1:
                        c0[1] = "true"
                    else:
                        c0[1] = "false"
                if c1[0] == "BOOL":
                    if c1[1] == 1:
                        c1[1] = "true"
                    else:
                        c1[1] = "false"
                return ["STRING", str(c0[1]) + str(c1[1])]        
            return ["INT", c0[1] * c1[1]]

        elif self.value == "/":
            c0 = self.children[0].Evaluate()
            c1 = self.children[1].Evaluate()
            if c0[0] == "STRING" or c1[0] == "STRING":
                raise NameError(f'Incompatible operation / with {c0[0]} and {c1[0]}')
            return ["INT", int(self.children[0].Evaluate()[1] / self.children[1].Evaluate()[1])]

        elif self.value == "&&":
            c0 = self.children[0].Evaluate()
            c1 = self.children[1].Evaluate()

            if c0[0] == "STRING" or c1[0] == "STRING":
                raise NameError(f'Incompatible operation && with {c0[0]} and {c1[0]}')
            if c0[1] and c1[1]:
                return ["BOOL", 1]
            else:
                return ["BOOL", 0]

        elif self.value == "||":
            if self.children[0].Evaluate()[1] or self.children[1].Evaluate()[1]:
                return ["BOOL", 1]
            else:
                return ["BOOL", 0]

        elif self.value == ">":
            if self.children[0].Evaluate()[1] > self.children[1].Evaluate()[1]:
                return ["BOOL", 1]
            else:
                return ["BOOL", 0]

        elif self.value == "<":
            if self.children[0].Evaluate()[1] < self.children[1].Evaluate()[1]:
                return ["BOOL", 1]
            else:
                return ["BOOL", 0]

        elif self.value == "==":
            if self.children[0].Evaluate()[1] == self.children[1].Evaluate()[1]:
                return ["BOOL", 1]
            else:
                return ["BOOL", 0]

class UnOp(Node):
    def __init__(self,value,children):
        super().__init__(value,children)

    def Evaluate(self):
        if self.value == "-":
            return ["INT", -self.children[0].Evaluate()[1]]
        elif self.value == "+":
            return ["INT", self.children[0].Evaluate()[1]]
        elif self.value == "!":
            if not self.children[0].Evaluate()[1]:
                return ["BOOL", 1]
            else:
                return ["BOOL", 0]

class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)
    def Evaluate(self):
        pass  

class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, None)
    
    def Evaluate(self):
        return table.getter(self.value)

class Print(Node):
    def __init__(self,children):
        super().__init__(None,children)
    
    def Evaluate(self):
        res = self.children[0].Evaluate()
        if res[0] == "BOOL":
            if res[1] == 1:
                print("true")
            else:
                print("false")
        else:
            print(res[1])

class Assigment(Node):
    def __init__(self,value,children):
        super().__init__(value,children)
    
    def Evaluate(self):
        if self.value == "=":
            c1 = self.children[1].Evaluate()
            if c1[0] == table.getter(self.children[0].value)[0]:
                #print(self.children[0].value, c1[0], c1[1])
                table.setter(self.children[0].value, c1[0], c1[1])
            else:
                raise NameError(f'Type expected was {table.getter(self.children[0].value)[0]} and got {c1[0]}')
        elif self.value == "::":
            table.setter(self.children[0], self.children[1], None)

class Statement(Node):
    def __init__(self, children):
        super().__init__(None,children)
    
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

class Readline(Node):
    def __init__(self):
        super().__init__(None, None)
    
    def Evaluate(self):
        return ["INT", int(input())]

class While(Node):
    def __init__(self, children):
        super().__init__(None,children)
    
    def Evaluate(self):
        while self.children[0].Evaluate()[1]:
            self.children[1].Evaluate()

class If(Node):
    def __init__(self, children):
        super().__init__(None,children)
    
    def Evaluate(self):
        if (self.children[0].Evaluate()[1]):
            return self.children[1].Evaluate()
        else:
            if len(self.children) > 2:
                return self.children[2].Evaluate()
