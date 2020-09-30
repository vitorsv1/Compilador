from tokenizer import Tokenizer
from prepro import PrePro
from node import *

class Parser:
    tokens = None

    @staticmethod
    def parseBlock():
        s = Statement([])
        while (Parser.tokens.actual.type != "EOF"):
            s.children.append(Parser.parseCommand())
        return s
    
    @staticmethod
    def parseCommand():
        result = None
        if Parser.tokens.actual.type == "BREAK":
            if result is None:
                result = NoOp(Parser.tokens.actual.value)
        
        elif Parser.tokens.actual.type == "IDENTIFIER":
            var = Parser.tokens.actual
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "EQUAL":
                result = Assigment(Parser.tokens.actual.value,[var])
                Parser.tokens.selectNext()
                result.children.append(Parser.parseExpression())
        
        elif Parser.tokens.actual.type == "PRINT":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "OPEN_P":
                Parser.tokens.selectNext()
                result = Print(Parser.tokens.actual.value, [Parser.parseExpression()])
                #Parser.tokens.selectNext()

                if Parser.tokens.actual.type == "CLOSE_P":
                    Parser.tokens.selectNext()
                else:
                    raise NameError(f"Syntax error, '(' open but not closed in position {Parser.tokens.position} with value {Parser.tokens.actual.value}")
            else:
                raise NameError(f"{Parser.tokens.actual.value} is a reserved word for function println()")
        
        else:
            raise NameError(f"Syntax error for type {Parser.tokens.actual.type} received")
        
        return result
    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()
        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
            if Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS":
                result = BinOp(Parser.tokens.actual.value, [result])
                Parser.tokens.selectNext()
                result.children.append(Parser.parseTerm())
            else:
                raise NameError(f"Type difference error, actual is {Parser.tokens.actual.type}")
        return result

    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()
        while Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV":
            if Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV":
                result = BinOp(Parser.tokens.actual.value, [result])
                Parser.tokens.selectNext()
                result.children.append(Parser.parseFactor())
            else:
                raise NameError(f"First type difference error, actual is {Parser.tokens.actual.type}")
        return result

    @staticmethod
    def parseFactor():
        if Parser.tokens.actual.type == "INT":
            res = IntVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == "OPEN_P":
            Parser.tokens.selectNext()
            res = Parser.parseExpression()

            if Parser.tokens.actual.type == "CLOSE_P":
                Parser.tokens.selectNext()
            else:
                raise NameError(f"Syntax error, ( open but not closed in position {Parser.tokens.position} with value {Parser.tokens.actual.value}")
        
        elif Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "PLUS":
            res = UnOp(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            res.children.append(Parser.parseFactor())

        elif Parser.tokens.actual.type == "IDENTIFIER":
            res = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        else:
            raise NameError(f"Syntax error, Token Received was invalid, received type {Parser.tokens.actual.type}")
        return res




    @staticmethod
    def run(code):
        code = PrePro.filter(code)
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        r = Parser.parseBlock()
        if Parser.tokens.actual.type == "EOF":
            return r
        
        raise NameError(f"Last token was not EOF Type")
