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
        return self.value

class BinOp(Node):
    def __init__(self,value,children):
        super().__init__(value,children)
    
    def Evaluate(self):
        if self.value == "-":
            return self.children[0].Evaluate() - self.children[1].Evaluate()
        elif self.value == "+":
            return self.children[0].Evaluate() + self.children[1].Evaluate()
        elif self.value == "*":
            return self.children[0].Evaluate() * self.children[1].Evaluate()
        elif self.value == "/":
            return int(self.children[0].Evaluate() / self.children[1].Evaluate())
        elif self.value == "&&":
            return self.children[0].Evaluate() and self.children[1].Evaluate()
        elif self.value == "||":
            return self.children[0].Evaluate() or self.children[1].Evaluate()
        elif self.value == ">":
            return self.children[0].Evaluate() > self.children[1].Evaluate()
        elif self.value == "<":
            return self.children[0].Evaluate() < self.children[1].Evaluate()
        elif self.value == "==":
            return self.children[0].Evaluate() == self.children[1].Evaluate()

class UnOp(Node):
    def __init__(self,value,children):
        super().__init__(value,children)

    def Evaluate(self):
        if self.value == "-":
            return - self.children[0].Evaluate()
        elif self.value == "+":
            return self.children[0].Evaluate()
        elif self.value == "!":
            return not self.children[0].Evaluate()

class NoOp(Node):
    def __init__(self):
        self.value = None
    def Evaluate(self):
        pass  

class Identifier(Node):
    def __init__(self, value):
        self.value = value
    
    def Evaluate(self):
        return table.getter(self.value)

class Print(Node):
    def __init__(self,children):
        super().__init__(None,children)
    
    def Evaluate(self):
        print(self.children[0].Evaluate())

class Assigment(Node):
    def __init__(self,value,children):
        super().__init__(value,children)
    
    def Evaluate(self):
        if self.value == "=":
            table.setter(self.children[0].value, self.children[1].Evaluate())

class Statement(Node):
    def __init__(self, children):
        super().__init__(None,children)
    
    def Evaluate(self):
        for child in self.children:
            child.Evaluate()

class Readline(Node):
    def __init__(self):
        self.value = None
    
    def Evaluate(self):
        return int(input())

class While(Node):
    def __init__(self, children):
        super().__init__(None,children)
    
    def Evaluate(self):
        while self.children[0].Evaluate():
            self.children[1].Evaluate()

class If(Node):
    def __init__(self, children):
        super().__init__(None,children)
    
    def Evaluate(self):
        if (self.children[0].Evaluate()):
            return self.children[1].Evaluate()
        else:
            if len(self.children) > 2:
                return self.children[2].Evaluate()

class Else(Node):
    def __init__(self, children):
        super().__init__(None,children)

    def Evaluate(self):
        return self.children[0].Evaluate()