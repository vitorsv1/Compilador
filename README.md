# Compilador 

### Diagrama Sintático

![alt text](https://github.com/vitorsv1/Compilador/blob/master/diagrama_sintatico.png)

### EBNF

- EXPRESSION = TERM, { ("+" | "-"), TERM } ;
- TERM = FACTOR, { ("*" | "/"), FACTOR } ;
- FACTOR = ("+" | "-") FACTOR | "(" EXPRESSION ")" | DIGIT ;
- DIGIT = 0|1|2|3|4|5|6|7|8|9;


