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

class UnOp(Node):
    def __init__(self,value,children):
        super().__init__(value,children)

    def Evaluate(self):
        if self.value == "-":
            return - self.children[0].Evaluate()
        elif self.value == "+":
            return self.children[0].Evaluate()


class NoOp(Node):
    def __init__(self, value):
        self.value = None
    def Evaluate(self):
        pass  

