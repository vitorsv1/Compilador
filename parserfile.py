from tokenizer import Tokenizer

class Parser:
    tokens = None

    @staticmethod
    def parseExpression():
        result = 0
        Parser.tokens.selectNext()
        if Parser.tokens.actual.type == "INT":
            result = Parser.tokens.actual.value
            Parser.tokens.selectNext()
            
            while Parser.tokens.actual.type == "PLUS" or \
                Parser.tokens.actual.type == "MINUS":
                if Parser.tokens.actual.type == "PLUS":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        result += Parser.tokens.actual.value
                    else:
                        raise NameError(f"Type difference error, actual is {Parser.tokens.actual.type}, should be INT")
                elif Parser.tokens.actual.type == "MINUS":
                    Parser.tokens.selectNext()
                    if Parser.tokens.actual.type == "INT":
                        result -= Parser.tokens.actual.value
                    else:
                        raise NameError(f"Type difference error, actual is {Parser.tokens.actual.type}, should be INT")
                Parser.tokens.selectNext()

            if Parser.tokens.actual.type == "INT":
                raise NameError("Error space between numbers, expeting operator type")

            return result
        else:
            raise NameError(f"First type difference error, actual is {Parser.tokens.actual.type}, should be INT")


    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        r = Parser.parseExpression()
        if Parser.tokens.actual.type == "EOF":
            return r
