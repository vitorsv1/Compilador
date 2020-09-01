from parserfile import Parser
import sys

def main():
    print(Parser.run(sys.argv[1]))
if __name__ == "__main__":
    main()