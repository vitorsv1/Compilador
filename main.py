from parserfile import Parser
from prepro import *
from symtable import *
import sys

def main():
    symbomtable = SymbolTable()

    f = open(sys.argv[1], "r")
    code = f.read()
    f.close()
    code = PrePro().filter(code)
    res = Parser.run(code)
    res.Evaluate(symbomtable)

if __name__ == "__main__":
    main()