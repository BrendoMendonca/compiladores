# Codigo gerado pelo compilador Fun
.section .bss
vetor_global: .zero 16
vetor_local: .zero 24
index: .quad 0

.section .text
.globl _start

_start:
    mov $0, %rax
    mov %rax, index
    mov $5, %rax
    push %rax
    mov $0, %rax
    mov %rax, %rcx
    pop %rax
    lea vetor_local(%rip), %rbx
    mov %rax, (%rbx, %rcx, 8)
    mov $10, %rax
    push %rax
    mov $1, %rax
    mov %rax, %rcx
    pop %rax
    lea vetor_local(%rip), %rbx
    mov %rax, (%rbx, %rcx, 8)
    mov $20, %rax
    push %rax
    mov $2, %rax
    mov %rax, %rcx
    pop %rax
    lea vetor_local(%rip), %rbx
    mov %rax, (%rbx, %rcx, 8)
    mov $2, %rax
    push %rax
    mov $1, %rax
    lea vetor_local(%rip), %rbx
    mov (%rbx, %rax, 8), %rax
    pop %rbx
    imul %rbx, %rax
    push %rax
    mov $0, %rax
    mov %rax, %rcx
    pop %rax
    lea vetor_global(%rip), %rbx
    mov %rax, (%rbx, %rcx, 8)
    mov $0, %rax
    lea vetor_global(%rip), %rbx
    mov (%rbx, %rax, 8), %rax
    push %rax
    mov $2, %rax
    lea vetor_local(%rip), %rbx
    mov (%rbx, %rax, 8), %rax
    push %rax
    mov $1, %rax
    lea vetor_local(%rip), %rbx
    mov (%rbx, %rax, 8), %rax
    push %rax
    mov $0, %rax
    lea vetor_local(%rip), %rbx
    mov (%rbx, %rax, 8), %rax
    pop %rbx
    add %rbx, %rax
    pop %rbx
    add %rbx, %rax
    pop %rbx
    add %rbx, %rax

    # Finalizacao
    mov %rax, %rdi
    call print_int
    mov $60, %rax
    xor %rdi, %rdi
    syscall

.include "runtime.s"