from tokenizer import Tokenizer
from prepro import PrePro

class Parser:
    tokens = None

    @staticmethod
    def parseExpression():
        Parser.tokens.selectNext()
        result = Parser.parseTerm()
        
        while Parser.tokens.actual.type == "PLUS" or \
            Parser.tokens.actual.type == "MINUS":
            if Parser.tokens.actual.type == "PLUS":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "INT":
                    result += Parser.parseTerm()
                else:
                    raise NameError(f"Type difference error, actual is {Parser.tokens.actual.type}, should be INT")
            elif Parser.tokens.actual.type == "MINUS":
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type == "INT":
                    result -= Parser.parseTerm()
                else:
                    raise NameError(f"Type difference error, actual is {Parser.tokens.actual.type}, should be INT")
        return result

    @staticmethod
    def parseTerm():
        result = 0
        if Parser.tokens.actual.type == "INT":
            result = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            
            while Parser.tokens.actual.type == "MULTI" or \
                Parser.tokens.actual.type == "DIV":
                if Parser.tokens.actual.type == "MULTI":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        result = result * Parser.tokens.actual.value
                    else:
                        raise NameError(f"Type difference error, actual is {Parser.tokens.actual.type}, should be INT")
                elif Parser.tokens.actual.type == "DIV":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        result = result / Parser.tokens.actual.value
                    else:
                        raise NameError(f"Type difference error, actual is {Parser.tokens.actual.type}, should be INT")
                Parser.tokens.selectNext()
            return result
        else:
            raise NameError(f"First type difference error, actual is {Parser.tokens.actual.type}, should be INT")

    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        r = int(Parser.parseExpression())
        if Parser.tokens.actual.type == "EOF":
            return r
        
        raise NameError(f"Last token was not EOF Type")
