# Compilador 

### Diagrama Sintático

![alt text](https://github.com/vitorsv1/Compilador/blob/v1.0/diagrama_sintatico-v2.png)

### EBNF

EXPRESSION = TERM, {("+"|"-"), TERM};
TERM = DIGIT, {("*"|"/"), DIGIT};
DIGIT = 0|1|2|3|4|5|6|7|8|9;
