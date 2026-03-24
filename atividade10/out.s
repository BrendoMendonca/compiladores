.section .text
.globl _start
_start:
    mov $5, %rax
    mov %rax, n
    mov $1, %rax
    mov %rax, res
Linicio0:
    mov $1, %rax
    push %rax
    mov n, %rax
    pop %rbx
    xor %rcx, %rcx
    cmp %rbx, %rax
    setg %cl
    mov %rcx, %rax
    cmp $0, %rax
    jz Lfim1
    mov n, %rax
    push %rax
    mov res, %rax
    pop %rbx
    imul %rbx, %rax
    mov %rax, res
    mov $1, %rax
    push %rax
    mov n, %rax
    pop %rbx
    sub %rbx, %rax
    mov %rax, n
    jmp Linicio0
Lfim1:
    mov res, %rax
    mov %rax, %rdi
    call print_int
    mov $0, %rdi
    mov $60, %rax
    syscall

.section .bss
n: .quad 0
res: .quad 0
