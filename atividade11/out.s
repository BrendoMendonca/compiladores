# Codigo gerado pelo compilador Fun
.section .bss
x: .quad 0

.section .text
.globl _start

fib:
    push %rbp
    sub $8, %rsp
    mov %rsp, %rbp
    mov $0, %rax
    mov %rax, 0(%rbp)
    mov $2, %rax
    push %rax
    mov 24(%rbp), %rax
    pop %rbx
    xor %rcx, %rcx
    cmp %rbx, %rax
    setl %cl
    mov %rcx, %rax
    cmp $0, %rax
    jz Lfalso0
    mov $1, %rax
    mov %rax, 0(%rbp)
    jmp Lfim1
Lfalso0:
    mov $2, %rax
    push %rax
    mov 24(%rbp), %rax
    pop %rbx
    sub %rbx, %rax
    push %rax
    call fib
    add $8, %rsp
    push %rax
    mov $1, %rax
    push %rax
    mov 24(%rbp), %rax
    pop %rbx
    sub %rbx, %rax
    push %rax
    call fib
    add $8, %rsp
    pop %rbx
    add %rbx, %rax
    mov %rax, 0(%rbp)
Lfim1:
    mov 0(%rbp), %rax
    add $8, %rsp
    pop %rbp
    ret

_start:
    mov $0, %rax
    mov %rax, x
    mov $5, %rax
    push %rax
    call fib
    add $8, %rsp
    mov %rax, x
    mov x, %rax

    # Finalizacao
    mov %rax, %rdi
    call print_int
    mov $60, %rax
    xor %rdi, %rdi
    syscall

.include "runtime.s"