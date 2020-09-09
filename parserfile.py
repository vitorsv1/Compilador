from tokenizer import Tokenizer
from prepro import PrePro

class Parser:
    tokens = None

    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()
        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
            if Parser.tokens.actual.type == "PLUS":
                Parser.tokens.selectNext()
                result += Parser.parseTerm()
            elif Parser.tokens.actual.type == "MINUS":
                Parser.tokens.selectNext()
                result -= Parser.parseTerm()
            else:
                raise NameError(f"Type difference error, actual is {Parser.tokens.actual.type}")
        return result

    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()
        while Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV":
            if Parser.tokens.actual.type == "MULTI":
                Parser.tokens.selectNext()
                result = int(result * Parser.parseFactor())
            elif Parser.tokens.actual.type == "DIV":
                Parser.tokens.selectNext()
                result = int(result / Parser.parseFactor())
            else:
                raise NameError(f"First type difference error, actual is {Parser.tokens.actual.type}")
        return result

    @staticmethod
    def parseFactor():
        res = 0
        if Parser.tokens.actual.type == "INT":
            res = int(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == "OPEN_P":
            Parser.tokens.selectNext()
            res = Parser.parseExpression()

            if Parser.tokens.actual.type == "CLOSE_P":
                Parser.tokens.selectNext()
            else:
                raise NameError(f"Syntax error, ( open but not closed in position {Parser.tokens.position} with value {Parser.tokens.actual.value}")
        
        elif Parser.tokens.actual.type == "MINUS":
            Parser.tokens.selectNext()
            res -= Parser.parseFactor()

        elif Parser.tokens.actual.type == "PLUS":
            Parser.tokens.selectNext()
            res += Parser.parseFactor()

        else:
            raise NameError(f"Syntax error, Token Received was invalid, received type {Parser.tokens.actual.type}")
        return res


    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        r = int(Parser.parseExpression())
        if Parser.tokens.actual.type == "EOF":
            return r
        
        raise NameError(f"Last token was not EOF Type")
