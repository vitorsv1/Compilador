
SYS_EXIT equ 1
SYS_READ equ 3
SYS_WRITE equ 4
STDIN equ 0
STDOUT equ 1
True equ 1
False equ 0

segment .data

segment .bss 
res RESB 1

section .text
global _start

print : ; subrotina print
PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; e s t a b e l e c e um novo base pointer
MOV EAX, [EBP+8] ; 1 argumento antes do RET e EBP
XOR ESI , ESI

print_dec : ; empilha todos os d i g i t o s
MOV EDX, 0
MOV EBX, 0x000A
DIV EBX
ADD EDX, '0 '
PUSH EDX
INC ESI ; contador de d i g i t o s
CMP EAX, 0
JZ print_next ; quando acabar pula
JMP print_dec

print_next :
CMP ESI , 0
JZ print_exit ; quando acabar de imprimir
DEC ESI
MOV EAX, SYS_WRITE
MOV EBX, STDOUT
POP ECX
MOV [res] , ECX
MOV ECX, res
MOV EDX, 1
INT 0x80
JMP print_next

print_exit :
POP EBP
RET

; subrotinas i f / while
binop_je :
JE binop_true
JMP binop_false

binop_jg :
JG binop_true
JMP binop_false

binop_jl :
JL binop_true
JMP binop_false

binop_false :
MOV EBX, False
JMP binop_exit

binop_true :
MOV EBX, True

binop_exit :
RET

_start :
PUSH EBP ; guarda o base pointer
MOV EBP, ESP ; e s t a b e l e c e um novo base pointer

PUSH DWORD 0 ;
NOP
PUSH DWORD 0 ;
NOP
PUSH DWORD 0 ;
NOP
MOV EBX, 2;
MOV [EBP-4], EBX;
MOV EBX, 5;
MOV [EBP-8], EBX;
MOV EBX, 1;
MOV [EBP-12], EBX;
LOOP_19:
MOV EBX, [EBP-4]
PUSH EBX ;
MOV EBX, [EBP-8]
PUSH EBX ;
MOV EBX, 1;
POP EAX ;
ADD EAX, EBX ;
MOV EBX, EAX ;
POP EAX ;
CMP EAX, EBX
CALL binop_jl
CMP EBX, False
JE EXIT_19
MOV EBX, [EBP-12]
PUSH EBX ;
MOV EBX, [EBP-4]
POP EAX ;
MUL EBX ;
MOV EBX, EAX ;
MOV [EBP-12], EBX;
MOV EBX, [EBP-4]
PUSH EBX ;
MOV EBX, 1;
POP EAX ;
ADD EAX, EBX ;
MOV EBX, EAX ;
MOV [EBP-4], EBX;
JMP LOOP_19
EXIT_19
MOV EBX, [EBP-12]
PUSH EBX
CALL print
POP EBX

POP EBP
MOV EAX, 1
INT 0x80
