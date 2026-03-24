#
# Modelo de saída para o compilador EV (Atividade 09)
#

.section .bss
.section .bss
    .lcomm a, 8
    .lcomm b, 8
# O compilador inserirá aqui as diretivas .lcomm para cada variável

.section .text
.globl _start

_start:
    # Atribuição: a
    mov $12, %rax
    push %rax
    mov $4, %rax
    push %rax
    mov $7, %rax
    pop %rbx
    add %rbx, %rax
    pop %rbx
    imul %rbx, %rax
    mov %rax, a
    # Atribuição: b
    mov $11, %rax
    push %rax
    mov $3, %rax
    push %rax
    mov a, %rax
    pop %rbx
    imul %rbx, %rax
    pop %rbx
    add %rbx, %rax
    mov %rax, b
    mov $13, %rax
    push %rax
    mov b, %rax
    pop %rbx
    imul %rbx, %rax
    push %rax
    mov $11, %rax
    push %rax
    mov a, %rax
    pop %rbx
    imul %rbx, %rax
    push %rax
    mov b, %rax
    push %rax
    mov a, %rax
    pop %rbx
    imul %rbx, %rax
    pop %rbx
    add %rbx, %rax
    pop %rbx
    add %rbx, %rax
# O compilador inserirá aqui o código das atribuições e da expressão final [cite: 168, 169]

    # Após a expressão final, o resultado estará em RAX
    call imprime_num
    call sair

.include "runtime.s"