from parserfile import Parser
import sys

def main():
    f = open(sys.argv[1], "r")
    code = f.read()
    f.close()
    Parser.run(code).Evaluate()
if __name__ == "__main__":
    main()