from parserfile import Parser
from node import asm
import sys

def main():
    f = open(sys.argv[1], "r")
    code = f.read()
    f.close()
    Parser.run(code).Evaluate()
    asm.flush()
if __name__ == "__main__":
    main()