from tokenizer import Tokenizer
from prepro import PrePro
from node import *


class Parser:
    tokens = None

    @staticmethod
    def parseBlock():
        s = Statement([])
        while (Parser.tokens.actual.type != "EOF" and
                Parser.tokens.actual.type != "END" and
                Parser.tokens.actual.type != "ELSEIF" and
                Parser.tokens.actual.type != "ELSE"):
            s.children.append(Parser.parseCommand())
        return s

    @staticmethod
    def parseCommand():
        result = None

        if Parser.tokens.actual.type == "IDENTIFIER":
            var = Parser.tokens.actual
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "IGUAL":
                result = Assigment(Parser.tokens.actual.value, [var])
                Parser.tokens.selectNext()

                if Parser.tokens.actual.type == "READLINE":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "OPEN_P":
                        Parser.tokens.selectNext()
                        result.children.append(Readline())

                        if Parser.tokens.actual.type == "CLOSE_P":
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual.type == "BREAK":
                                Parser.tokens.selectNext()
                            else:
                                raise NameError(
                                    'Error no BREAK Token expected')
                        else:
                            raise NameError(
                                f"Syntax error, '(' open but not closed in position {Parser.tokens.position} with value {Parser.tokens.actual.value}")
                else:
                    result.children.append(Parser.parseRelExpression())
                    if Parser.tokens.actual.type == "BREAK":
                        Parser.tokens.selectNext()
                    else:
                        raise NameError('Error BREAK Token expected')
            else:
                raise NameError(
                    f"Syntax error for type {Parser.tokens.actual.type} received")

        elif Parser.tokens.actual.type == "PRINT":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "OPEN_P":
                Parser.tokens.selectNext()
                result = Print([Parser.parseRelExpression()])

                if Parser.tokens.actual.type == "CLOSE_P":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "BREAK":
                        Parser.tokens.selectNext()
                    else:
                        raise NameError('Error on BREAK Token expected')
                else:
                    raise NameError(
                        f"Syntax error, '(' open but not closed in position {Parser.tokens.position} with value {Parser.tokens.actual.value}")
            else:
                raise NameError(
                    f"{Parser.tokens.actual.value} is a reserved word for function println()")

        elif Parser.tokens.actual.type == "WHILE":
            Parser.tokens.selectNext()
            result = While([Parser.parseRelExpression()])

            if Parser.tokens.actual.type == "BREAK":
                Parser.tokens.selectNext()
                result.children.append(Parser.parseBlock())

                if Parser.tokens.actual.type == "END":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "BREAK":
                        Parser.tokens.selectNext()
                    else:
                        raise NameError(
                            f'Error on BREAK Token expected - {Parser.tokens.actual.value}')
                else:
                    raise NameError(
                        f'Error on END Token expected - {Parser.tokens.actual.value}')
            else:
                raise NameError(
                    f'Error on BREAK Token expected - {Parser.tokens.actual.value}')

        elif Parser.tokens.actual.type == "IF":
            Parser.tokens.selectNext()
            result = If([Parser.parseRelExpression()])

            if Parser.tokens.actual.type == "BREAK":
                Parser.tokens.selectNext()
                result.children.append(Parser.parseBlock())
                temp = None
                atual = None

                while Parser.tokens.actual.type == "ELSEIF":
                    Parser.tokens.selectNext()
                    temp = If([Parser.parseRelExpression()])
                    if Parser.tokens.actual.type == "BREAK":
                        Parser.tokens.selectNext()
                        temp.children.append(Parser.parseBlock())
                        if atual is None:
                            result.children.append(temp)
                        else:
                            atual.children.append(temp)
                        atual = temp

                if Parser.tokens.actual.type == "END":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "BREAK":
                        Parser.tokens.selectNext()
                    else:
                        raise NameError(
                            f'Error on BREAK Token expected - {Parser.tokens.actual.value}')

                elif Parser.tokens.actual.type == "ELSE":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "BREAK":
                        Parser.tokens.selectNext()
                        if atual is None:
                            result.children.append(Parser.parseBlock())
                        else:
                            atual.children.append(Parser.parseBlock())
                        if Parser.tokens.actual.type == "END":
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual.type == "BREAK":
                                Parser.tokens.selectNext()
                            else:
                                raise NameError(
                                    f'Error on BREAK Token expected - {Parser.tokens.actual.value}')
                        else:
                            raise NameError(
                                f'Error on END Token expected - {Parser.tokens.actual.value}')
                    else:
                        raise NameError(
                            f'Error on BREAK Token expected - {Parser.tokens.actual.value}')
            else:
                raise NameError(
                    f'Error on BREAK Token expected - {Parser.tokens.actual.value}')

        elif Parser.tokens.actual.type == "BREAK":
            Parser.tokens.selectNext()
            if result is None:
                result = NoOp()

        else:
            raise NameError(
                f"Syntax error for type {Parser.tokens.actual.type} received")

        return result

    @staticmethod
    def parseRelExpression():
        result = Parser.parseExpression()
        while Parser.tokens.actual.type == "IGUAL_I" or Parser.tokens.actual.type == "MAIOR" or Parser.tokens.actual.type == "MENOR":
            if Parser.tokens.actual.type == "IGUAL_I" or Parser.tokens.actual.type == "MAIOR" or Parser.tokens.actual.type == "MENOR":
                result = BinOp(Parser.tokens.actual.value, [result])
                Parser.tokens.selectNext()
                result.children.append(Parser.parseExpression())
            else:
                raise NameError(
                    f"Type difference error, actual is {Parser.tokens.actual.type}")
        return result

    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()
        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "OR":
            if Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "OR":
                result = BinOp(Parser.tokens.actual.value, [result])
                Parser.tokens.selectNext()
                result.children.append(Parser.parseTerm())
            else:
                raise NameError(
                    f"Type difference error, actual is {Parser.tokens.actual.type}")
        return result

    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()
        while Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "AND":
            if Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "AND":
                result = BinOp(Parser.tokens.actual.value, [result])
                Parser.tokens.selectNext()
                result.children.append(Parser.parseFactor())
            else:
                raise NameError(
                    f"First type difference error, actual is {Parser.tokens.actual.type}")
        return result

    @staticmethod
    def parseFactor():
        if Parser.tokens.actual.type == "INT":
            res = IntVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == "OPEN_P":
            Parser.tokens.selectNext()
            res = Parser.parseRelExpression()

            if Parser.tokens.actual.type == "CLOSE_P":
                Parser.tokens.selectNext()
            else:
                raise NameError(
                    f"Syntax error, ( open but not closed in position {Parser.tokens.position} with value {Parser.tokens.actual.value}")

        elif Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "NOT":
            res = UnOp(Parser.tokens.actual.value, [])
            Parser.tokens.selectNext()
            res.children.append(Parser.parseFactor())

        elif Parser.tokens.actual.type == "IDENTIFIER":
            res = Identifier(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        else:
            raise NameError(
                f"Syntax error, Token Received was invalid, received type {Parser.tokens.actual.type}")
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
