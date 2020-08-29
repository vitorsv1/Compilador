from tokenfile import Token


class Tokenizer:

    def __init__(self, origin: str):
        self.origin = origin
        self.position = 0
        self.actual = None

    def selectNext(self):
        string_size = len(self.origin)
        while self.position <= string_size:

            if self.origin[self.position].isnumeric():
                tok = ""
                while (self.position < (string_size)) and \
                        (self.origin[self.position].isnumeric()):
                    tok += self.origin[self.position]
                    self.position += 1
                self.actual = Token("INT", int(tok))

            elif self.origin[self.position] == '+':
                self.actual = Token("PLUS", '+')
                self.position += 1

            elif self.origin[self.position] == '-':
                self.actual = Token("MINUS", '-')
                self.position += 1

            elif self.position == (string_size - 1):
                self.actual = Token("EOF", '"')
                self.position = 0
                break

            elif (self.origin[self.position] == '"') or \
                    (self.origin[self.position].isspace()):
                self.position += 1
            else:
                raise NameError("Invalid character")


# if __name__ == "__main__":
#     a = Tokenizer(' "123123   +    12312" ')
#     a.selectNext()
