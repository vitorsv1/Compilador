from tokenizer import *
from node import *


class Parser:
    tokens = None

    @staticmethod
    def parseBlock():
        s = Statement()
        while (Parser.tokens.actual.type != "EOF" and
                Parser.tokens.actual.type != "END" and
                Parser.tokens.actual.type != "ELSEIF" and
                Parser.tokens.actual.type != "ELSE"):
            s.children.append(Parser.parseCommand())
        return s

    @staticmethod
    def parseStructBlock():
        result = Statement()

        while(Parser.tokens.actual.type != 'EOF'):

            if(Parser.tokens.actual.type == 'FUNCTION'):
                Parser.tokens.selectNext()

                if(Parser.tokens.actual.type == 'IDENTIFIER'):
                    functionDeclare = FunctionDeclaration(Parser.tokens.actual.value, None)
                    result.children.append(functionDeclare)
                    Parser.tokens.selectNext()

                    if(Parser.tokens.actual.type == 'OPEN_P'):
                        Parser.tokens.selectNext()

                        if(Parser.tokens.actual.type == 'IDENTIFIER'):
                            identifier = [None, None]
                            identifier[0] = Parser.tokens.actual.value
                            Parser.tokens.selectNext()

                            if(Parser.tokens.actual.type == 'DOIS_PP'):
                                Parser.tokens.selectNext()

                                if(Parser.tokens.actual.type == 'INT' or Parser.tokens.actual.type == 'BOOL' or Parser.tokens.actual.type == 'STRING'):
                                    identifier[1] = Parser.tokens.actual.value
                                    functionDeclare.children.append(identifier)
                                    Parser.tokens.selectNext()

                                    while(Parser.tokens.actual.type == 'COMMA'):
                                        Parser.tokens.selectNext()

                                        if(Parser.tokens.actual.type == 'IDENTIFIER'):
                                            identifier = [None, None]
                                            identifier[0] = Parser.tokens.actual.value
                                            Parser.tokens.selectNext()

                                            if(Parser.tokens.actual.type == 'DOIS_PP'):
                                                Parser.tokens.selectNext()

                                                if(Parser.tokens.actual.type == 'INT' or Parser.tokens.actual.type == 'BOOL' or Parser.tokens.actual.type == 'STRING'):
                                                    identifier[1] = Parser.tokens.actual.value
                                                    functionDeclare.children.append(identifier)
                                                    Parser.tokens.selectNext()
                                                    
                                                else:
                                                    raise ValueError('Function No Type Declared after ::')
                                            else:
                                                raise ValueError('No "::" after an Identifier in Function')
                                        else:
                                            raise ValueError('No Identifier after "," in Function')
                                else:
                                    raise ValueError('No Type after "::" in Function')
                            else:
                                raise ValueError('No "::" after an Identifier in Function')

                        if(Parser.tokens.actual.type == 'CLOSE_P'):
                            Parser.tokens.selectNext()

                            if(Parser.tokens.actual.type == 'DOIS_PP'):
                                Parser.tokens.selectNext()

                                if(Parser.tokens.actual.type == 'INT' or Parser.tokens.actual.type == 'BOOL' or Parser.tokens.actual.type == 'STRING'):
                                    functionDeclare.typ = Parser.tokens.actual.value
                                    Parser.tokens.selectNext()

                                    if(Parser.tokens.actual.type == 'BREAK'):
                                        Parser.tokens.selectNext()
                                        statement_node = Parser.parseBlock()
                                        functionDeclare.children.append(statement_node)

                                        if(Parser.tokens.actual.type == 'END'):
                                            Parser.tokens.selectNext()

                                            if(Parser.tokens.actual.type == 'BREAK'):
                                                Parser.tokens.selectNext()

                                            else:
                                                raise ValueError('No Break Line after End')
                                        else:
                                            raise ValueError('Missing and END Token')
                                    else:
                                        raise ValueError('No Break Line after type Function Declaration')
                                else:
                                    raise ValueError('No Type after "::" in Function')
                            else:
                                raise ValueError('No "::" after ")" in Function')
                        else:
                            raise ValueError('No ")" after an openning one in Function declaration')
                    else:
                        raise ValueError('No "(" in Function declaration')
                else:
                    raise ValueError('No Identifier in Function declaration')
            else:
                result.children.append(Parser.parseCommand())

        return result
    
    @staticmethod
    def parseCommand():
        result = NoOp()
        
        if Parser.tokens.actual.type == "IDENTIFIER":
            var = Parser.tokens.actual
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == 'OPEN_P':
                result = FunctionCall(var.value)
                Parser.tokens.selectNext()
                if Parser.tokens.actual.type != 'CLOSE_P':
                    result.children.append(Parser.parseRelExpression())
                    while Parser.tokens.actual.type == 'COMMA':
                        Parser.tokens.selectNext()
                        result.children.append(Parser.parseRelExpression())
                if Parser.tokens.actual.type == 'CLOSE_P':
                    Parser.tokens.selectNext()
                else:
                    raise NameError(f"Syntax error, '(' open but not closed in position {Parser.tokens.position} with value {Parser.tokens.actual.value}")
            else:
                identifier = Identifier(var.value)
                if Parser.tokens.actual.type == "IGUAL":
                    Parser.tokens.selectNext()
                    result = Assigment()
                    result.children[0] = identifier
                    if Parser.tokens.actual.type == "READLINE":
                        Parser.tokens.selectNext()
                        result.children[1] = Readline()
                        if Parser.tokens.actual.type == "OPEN_P":
                            Parser.tokens.selectNext()
                            if Parser.tokens.actual.type == "CLOSE_P":
                                Parser.tokens.selectNext()
                            else:
                                raise NameError(f"Syntax error, '(' open but not closed in position {Parser.tokens.position} with value {Parser.tokens.actual.value}")
                    else:
                        result.children[1] = Parser.parseRelExpression()
                else:
                    raise NameError(f"Syntax error for type {Parser.tokens.actual.type} received")

        elif Parser.tokens.actual.type == "PRINT":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "OPEN_P":
                Parser.tokens.selectNext()
                result = Print()
                result.children[0] = Parser.parseRelExpression()
                if Parser.tokens.actual.type == "CLOSE_P":
                    Parser.tokens.selectNext()
                    return result
                else:
                    raise NameError(f"Syntax error, '(' open but not closed in position {Parser.tokens.position} with value {Parser.tokens.actual.value}")
            else:
                raise NameError(f"{Parser.tokens.actual.value} is a reserved word for function println()")

        elif Parser.tokens.actual.type == "WHILE":
            Parser.tokens.selectNext()
            result = While()
            result.children[0] = Parser.parseRelExpression()
            if Parser.tokens.actual.type == "BREAK":
                Parser.tokens.selectNext()
                result.children[1] = Parser.parseBlock()
                if Parser.tokens.actual.type == "END":
                    Parser.tokens.selectNext()
                else:
                    raise NameError(f'Error on END Token expected - {Parser.tokens.actual.value}')
            else:
                raise NameError(f'Error on BREAK Token expected - {Parser.tokens.actual.value}')

        elif Parser.tokens.actual.type == "IF":
            Parser.tokens.selectNext()
            result = If()
            result.children[0] = Parser.parseRelExpression()
            if Parser.tokens.actual.type == "BREAK":
                Parser.tokens.selectNext()
                result.children[1] = Parser.parseBlock()
                if(Parser.tokens.actual.type == 'ELSEIF'):
                    results = []
                    while(Parser.tokens.actual.type == 'ELSEIF'):
                        Parser.tokens.selectNext()
                        result2 = If()
                        result2.children[0] = Parser.parseRelExpression()

                        if(Parser.tokens.actual.type == 'BREAK'):
                            Parser.tokens.selectNext()
                            result2.children[1] = Parser.parseBlock()
                            results.append(result2)
                        else:
                            raise NameError("No Break after ElseIf")

                    result.children[2] = results[0]
                    for i in range(len(results)):
                        if(i != len(results) - 1):
                            results[i].children[2] = results[i+1]

                    if(Parser.tokens.actual.type == 'ELSE'):
                        Parser.tokens.selectNext()
                        if(Parser.tokens.actual.type == 'BREAK'):
                            Parser.tokens.selectNext()
                            result2 = Else()
                            result2.children[0] = Parser.parseBlock()
                            results[-1].children[2] = result2
                            if(Parser.tokens.actual.type == 'END'):
                                Parser.tokens.selectNext()
                            else:
                                raise NameError("No End token after Break Line")
                        else:
                            raise NameError("No Break Line after Else")
                    elif(Parser.tokens.actual.type == 'END'):
                        Parser.tokens.selectNext()
                    else:
                        raise NameError("No End token after else")

                elif Parser.tokens.actual.type == "ELSE":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "BREAK":
                        Parser.tokens.selectNext()
                        result2 = Else()
                        result2.children[0] = Parser.parseBlock()
                        result.children[2] = result2
                        if Parser.tokens.actual.type == "END":
                            Parser.tokens.selectNext()
                        else:
                            raise NameError(f'Error on END Token expected - {Parser.tokens.actual.value}')
                    else:
                        raise NameError(f'Error on BREAK Token expected - {Parser.tokens.actual.value}')
                
                elif Parser.tokens.actual.type == 'END':
                    Parser.tokens.selectNext()
                else:
                    raise NameError(f'Error on END Token expected - {Parser.tokens.actual.type}')
            else:
                raise NameError(f'Error on BREAK Token expected - {Parser.tokens.actual.value}')

        elif(Parser.tokens.actual.type == 'RETURN'):
            result = Return()
            Parser.tokens.selectNext()
            result.children[0] = Parser.parseRelExpression()
        
        elif Parser.tokens.actual.type == "LOCAL":
            Parser.tokens.selectNext()
            if Parser.tokens.actual.type == "IDENTIFIER":
                result = AssigmentType()
                result.children[0] = Identifier(Parser.tokens.actual.value)
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type == 'DOIS_PP'):
                    Parser.tokens.selectNext()
                    if(Parser.tokens.actual.type == 'STRING' or 
                       Parser.tokens.actual.type == 'BOOL' or 
                       Parser.tokens.actual.type == 'INT'):
                        result.children[1] = Parser.tokens.actual.value
                        Parser.tokens.selectNext()
                    else:
                        raise NameError("No Type Declared after ::")
                else:
                    raise NameError("No :: after Identifier")
            else:
                raise NameError("No Identifier after local declaration")

        if Parser.tokens.actual.type == "BREAK":
            Parser.tokens.selectNext()
            return result
        
        else:
            raise NameError(f"Syntax error for type {Parser.tokens.actual.type} received")

    @staticmethod
    def parseRelExpression():
        result = Parser.parseExpression()
        while Parser.tokens.actual.type == "IGUAL_I" or Parser.tokens.actual.type == "MAIOR" or Parser.tokens.actual.type == "MENOR":
            if Parser.tokens.actual.type == "IGUAL_I" or Parser.tokens.actual.type == "MAIOR" or Parser.tokens.actual.type == "MENOR":
                res = BinOp(Parser.tokens.actual.value)
                res.children[0] = result
                result = res
                Parser.tokens.selectNext()
                result.children[1] = Parser.parseExpression()
            else:
                raise NameError(f"Type difference error, actual is {Parser.tokens.actual.type}")
        return result

    @staticmethod
    def parseExpression():
        result = Parser.parseTerm()
        while Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "OR":
            if Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "OR":
                res = BinOp(Parser.tokens.actual.value)
                res.children[0] = result
                result = res
                Parser.tokens.selectNext()
                result.children[1] = Parser.parseTerm()
            else:
                raise NameError(f"Type difference error, actual is {Parser.tokens.actual.type}")
        return result

    @staticmethod
    def parseTerm():
        result = Parser.parseFactor()
        while Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "AND":
            if Parser.tokens.actual.type == "MULTI" or Parser.tokens.actual.type == "DIV" or Parser.tokens.actual.type == "AND":
                res = BinOp(Parser.tokens.actual.value)
                res.children[0] = result
                result = res
                Parser.tokens.selectNext()
                result.children[1] = Parser.parseFactor()                
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
            res = Parser.parseRelExpression()

            if Parser.tokens.actual.type == "CLOSE_P":
                Parser.tokens.selectNext()
            else:
                raise NameError("Syntax error, ( open but not closed in position {Parser.tokens.position} with value {Parser.tokens.actual.value}")

        elif Parser.tokens.actual.type == "MINUS" or Parser.tokens.actual.type == "PLUS" or Parser.tokens.actual.type == "NOT":
            res = UnOp(Parser.tokens.actual.value)
            Parser.tokens.selectNext()
            res.children[0] = Parser.parseFactor()

        elif Parser.tokens.actual.type == "IDENTIFIER":
            res = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            if(Parser.tokens.actual.type == 'OPEN_P'):
                result = FunctionCall(res)
                Parser.tokens.selectNext()
                if(Parser.tokens.actual.type != 'CLOSE_P'):
                    result.children.append(Parser.parseRelExpression())
                    while(Parser.tokens.actual.type == 'COMMA'):
                        Parser.tokens.selectNext()
                        result.children.append(Parser.parseRelExpression())
                if(Parser.tokens.actual.type == 'CLOSE_P'):
                    Parser.tokens.selectNext()
                else:
                    raise NameError('No "(" after an open one')
            else:
                result = Identifier(res)
            return result

        elif Parser.tokens.actual.type == "TRUE" or Parser.tokens.actual.type == "FALSE":
            res = BoolVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        elif Parser.tokens.actual.type == "STRING":
            res = StringVal(Parser.tokens.actual.value)
            Parser.tokens.selectNext()

        else:
            raise NameError(f"Syntax error, Token Received was invalid, received type {Parser.tokens.actual.type}")
        
        return res

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.tokens.selectNext()
        r = Parser.parseStructBlock()
        if Parser.tokens.actual.type == "EOF":
            return r

        raise NameError(f"Last token was not EOF Type")
