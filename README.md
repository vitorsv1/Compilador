# Compilador 

### Diagrama Sintático

![alt text](https://github.com/vitorsv1/Compilador/blob/master/diagrama-sintatico.png)

### EBNF

- BLOCK = { COMMAND } ;
- COMMAND = ( λ | ASSIGNMENT | PRINT | IF | WHILE | LOCAL), "\n" ;
- LOCAL = "local", IDENTIFIER, "::", TYPE;
- ASSIGNMENT = IDENTIFIER, "=", (REL_EXPRESSION | readline, "(", ")" ) ;
- PRINT = "println", "(", REL_EXPRESSION, ")" ;
- EXPRESSION = TERM, { ("+" | "-" | "||"), TERM } ;
- REL_EXPRESSION = EXPRESSION, { ("==" | ">" | "<"), EXPRESSION };
- WHILE = "while", REL_EXPRESSION, "\n", BLOCK, "end";
- IF = "if", REL_EXPRESSION, "\n", BLOCK, { ELSEIF | ELSE }, "end";
- ELSEIF = "elseif", REL_EXPRESSION, "\n", BLOCK, { ELSEIF | ELSE };
- ELSE = "else", "\n", BLOCK;
- TERM = FACTOR, { ("-" | "/" | "&&"), FACTOR } ;
- FACTOR = (("+" | "-" | "!"), FACTOR) | NUMBER | STRING | "(", REL_EXPRESSION, ")" | IDENTIFIER | BOOLEAN ;
- IDENTIFIER = LETTER, { LETTER | DIGIT | "_" } ;
- NUMBER = DIGIT, { DIGIT } ;
- TYPE = "Int" | "Bool" | "String"; 
- STRING = '"', (.*?), '"';
- BOOLEAN = "true" | "false";
- LETTER = ( a | ... | z | A | ... | Z ) ;
- DIGIT = ( 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 ) ;
