import symtable
import assembler

table = symtable.SymbolTable()
asm = assembler.Assembler()

class Node:

    i = 0

    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.i = Node.sumi()

    def Evaluate(self):
        pass

    @staticmethod
    def sumi():
        Node.i += 1
        return Node.i

class IntVal(Node):
    def __init__(self,value):
        super().__init__(value, None)
        
    def Evaluate(self):
        #return ["INT", self.value]
        asm.write_line(f"MOV EBX, {self.value};")

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
            #return ["BOOL", 0]
            asm.write_line("CALL binop_false")
        elif self.value == "true":
            #return ["BOOL", 1]
            asm.write_line("CALL binop_true")

class BinOp(Node):
    def __init__(self,value,children):
        super().__init__(value,children)
    
    def Evaluate(self):
        if self.value == "-":
            self.children[0].Evaluate()
            asm.write_line("PUSH EBX ;")
            self.children[1].Evaluate()
            asm.write_line("POP EAX ;")
            asm.write_line("SUB EAX, EBX ;")
            asm.write_line("MOV EBX, EAX ;")

            #if c0[0] == "STRING" or c1[0] == "STRING":
            #    raise NameError(f'Incompatible operation - with {c0[0]} and {c1[0]}')
            
            #return ["INT", self.children[0].Evaluate()[1] - self.children[1].Evaluate()[1]]

        elif self.value == "+":
            self.children[0].Evaluate()
            asm.write_line("PUSH EBX ;")
            self.children[1].Evaluate()
            asm.write_line("POP EAX ;")
            asm.write_line("ADD EAX, EBX ;")
            asm.write_line("MOV EBX, EAX ;")

            #if c0[0] == c1[0]:
            #    return [c0[0], c0[1] + c1[1]]
            #elif c0[0] == "STRING" or c1[0] == "STRING":
            #    raise NameError(f'Incompatible operation + with {c0[0]} and {c1[0]}')
            #else:
            #    return ["INT", c0[1] + c1[1]]

        elif self.value == "*":
            self.children[0].Evaluate()
            asm.write_line("PUSH EBX ;")
            self.children[1].Evaluate()
            asm.write_line("POP EAX ;")
            asm.write_line("MUL EBX ;")
            asm.write_line("MOV EBX, EAX ;")

            #if c0[0] == "STRING" or c1[0] == "STRING":
            #    if c0[0] == "BOOL":
            #        if c0[1] == 1:
            #            c0[1] = "true"
            #        else:
            #            c0[1] = "false"
            #    if c1[0] == "BOOL":
            #        if c1[1] == 1:
            #            c1[1] = "true"
            #        else:
            #            c1[1] = "false"
            #    return ["STRING", str(c0[1]) + str(c1[1])]        
            #return ["INT", c0[1] * c1[1]]

        elif self.value == "/":
            self.children[0].Evaluate()
            asm.write_line("PUSH EBX ;")
            self.children[1].Evaluate()
            asm.write_line("POP EAX ;")
            asm.write_line("DIV EBX ;")
            asm.write_line("MOV EBX, EAX ;")
            
            #if c0[0] == "STRING" or c1[0] == "STRING":
            #    raise NameError(f'Incompatible operation / with {c0[0]} and {c1[0]}')
            #return ["INT", int(self.children[0].Evaluate()[1] / self.children[1].Evaluate()[1])]

        elif self.value == "&&":
            self.children[0].Evaluate()
            asm.write_line("PUSH EBX ;")
            self.children[1].Evaluate()
            asm.write_line("POP EAX ;")
            asm.write_line("AND EAX, EBX ;")
            asm.write_line("MOV EBX, EAX ;")

            #if c0[0] == "STRING" or c1[0] == "STRING":
            #    raise NameError(f'Incompatible operation && with {c0[0]} and {c1[0]}')
            #if c0[1] and c1[1]:
            #    return ["BOOL", 1]
            #else:
            #    return ["BOOL", 0]

        elif self.value == "||":
            self.children[0].Evaluate()
            asm.write_line("PUSH EBX ;")
            self.children[1].Evaluate()
            asm.write_line("POP EAX ;")
            asm.write_line("OR EAX, EBX ;")
            asm.write_line("MOV EBX, EAX ;")

            #if c0 or c1:
            #    return ["BOOL", 1]
            #else:
            #    return ["BOOL", 0]

        elif self.value == ">":
            self.children[0].Evaluate()
            asm.write_line("PUSH EBX ;")
            self.children[1].Evaluate()
            asm.write_line("POP EAX ;")
            asm.write_line("CMP EAX, EBX")
            asm.write_line("CALL binop_jg")

            #if c0 > c1:
            #    return ["BOOL", 1]
            #else:
            #    return ["BOOL", 0]

        elif self.value == "<":
            self.children[0].Evaluate()
            asm.write_line("PUSH EBX ;")
            self.children[1].Evaluate()
            asm.write_line("POP EAX ;")
            asm.write_line("CMP EAX, EBX")
            asm.write_line("CALL binop_jl")

            #if c0 < c1:
            #    return ["BOOL", 1]
            #else:
            #    return ["BOOL", 0]

        elif self.value == "==":
            self.children[0].Evaluate()
            asm.write_line("PUSH EBX ;")
            self.children[1].Evaluate()
            asm.write_line("POP EAX ;")
            asm.write_line("CMP EAX, EBX")
            asm.write_line("CALL binop_je")
            
            #if c0 == c1:
            #    return ["BOOL", 1]
            #else:
            #    return ["BOOL", 0]

class UnOp(Node):
    def __init__(self,value,children):
        super().__init__(value,children)

    def Evaluate(self):
        if self.value == "+":
            #return ["INT", -self.children[0].Evaluate()[1]]
            self.children[0].Evaluate()
            asm.write_line(f"MOV EBX, EAX")
        elif self.value == "-":
            #return ["INT", self.children[0].Evaluate()[1]]
            self.children[0].Evaluate()
            asm.write_line(f"iMUL -1")
            asm.write_line(f"MOV EBX, EAX")
        elif self.value == "!":
            self.children[0].Evaluate()
            asm.write_line(f"NOT EAX")
            asm.write_line(f"MOV EBX, EAX")
            #if not self.children[0].Evaluate()[1]:
            #    return ["BOOL", 1]
            #else:
            #    return ["BOOL", 0]


class NoOp(Node):
    def __init__(self):
        super().__init__(None, None)
    def Evaluate(self):
        asm.write_line("NOP")  

class Identifier(Node):
    def __init__(self, value):
        super().__init__(value, None)
    
    def Evaluate(self):
        #return table.getter(self.value)
        pos = table.getter(self.value)[2]
        asm.write_line(f"MOV EBX, [EBP-{pos}]")

class Print(Node):
    def __init__(self,children):
        super().__init__(None,children)
    
    def Evaluate(self):
        self.children[0].Evaluate()
        #if res[0] == "BOOL":
        #    if res[1] == 1:
        #        print("true")
        #    else:
        #        print("false")
        #else:
        #    print(res[1])
        asm.write_line("PUSH EBX")
        asm.write_line("CALL print")
        asm.write_line("POP EBX")

class Assigment(Node):
    def __init__(self,value,children):
        super().__init__(value,children)
    
    def Evaluate(self):
        if self.value == "=":
            self.children[1].Evaluate()
            #if c1[0] == table.getter(self.children[0].value)[0]:
            pos = table.getter(self.children[0].value)[2]
            asm.write_line(f"MOV [EBP-{pos}], EBX;")
            #table.setter(self.children[0].value, c1[0], c1[1])
            #else:
            #    raise NameError(f'Type expected was {table.getter(self.children[0].value)[0]} and got {c1[0]}')
        elif self.value == "::":
            asm.write_line("PUSH DWORD 0 ;")
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
        #while self.children[0].Evaluate()[1]:
        #    self.children[1].Evaluate()
        asm.write_line(f"LOOP_{self.i}:")
        self.children[0].Evaluate()
        asm.write_line(f"CMP EBX, False")
        asm.write_line(f"JE EXIT_{self.i}")
        self.children[1].Evaluate()
        asm.write_line(f"JMP LOOP_{self.i}")
        asm.write_line(f"EXIT_{self.i}:")

class If(Node):
    def __init__(self, children):
        super().__init__(None,children)
    
    def Evaluate(self):
        #if (self.children[0].Evaluate()[1]):
        #    return self.children[1].Evaluate()
        #else:
        #    if len(self.children) > 2:
        #        return self.children[2].Evaluate()
        self.children[0].Evaluate()
        asm.write_line(f"CMP EBX, False")
        asm.write_line(f"JE EXIT_{self.i}")
        self.children[1].Evaluate()
        asm.write_line(f"EXIT_{self.i}:")
        if len(self.children) > 2 and self.children[2]:
            
            self.children[0].Evaluate()
            asm.write_line("CMP EBX, False")
            asm.write_line(f"JNE EXIT_ELSE_{self.i}")
            self.children[2].Evaluate()
            asm.write_line(f"EXIT_ELSE_{self.i}:")
