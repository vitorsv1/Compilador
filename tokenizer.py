from tokenfile import Token


class Tokenizer:

    def __init__(self, origin: str):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self):

        if self.position == len(self.origin):
            self.actual = Token("EOF", '"')
            return
        
        elif self.origin[self.position].isspace():
            self.position += 1
            self.selectNext()
        
        elif self.origin[self.position].isnumeric():
            tok = ""
            while (self.position < (len(self.origin))) and \
                    (self.origin[self.position].isnumeric()):
                tok += self.origin[self.position]
                self.position += 1
            self.actual = Token("INT", int(tok))
            return

        elif self.origin[self.position] == '+':
            self.actual = Token("PLUS", '+')
            self.position += 1
            return

        elif self.origin[self.position] == '-':
            self.actual = Token("MINUS", '-')
            self.position += 1
            return
        
        elif self.origin[self.position] == '*':
            self.actual = Token("MULTI", '-')
            self.position += 1
            return
        
        elif self.origin[self.position] == '/':
            self.actual = Token("DIV", '-')
            self.position += 1
            return

        else:
            raise NameError("Invalid character")
