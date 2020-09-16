from parserfile import Parser
import sys

def main():
    f = open(sys.argv[1], "r")
    for line in f:
        print(Parser.run(line).Evaluate())
if __name__ == "__main__":
    main()