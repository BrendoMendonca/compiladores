.section .text
.globl print_int

print_int:
    push %rbp
    mov %rsp, %rbp
    sub $32, %rsp
    mov %rdi, %rax
    mov $10, %rbx
    lea 31(%rsp), %rsi
    movb $10, (%rsi)
    mov $1, %rcx
.Lloop_conv:
    dec %rsi
    inc %rcx
    xor %rdx, %rdx
    div %rbx
    add $48, %dl
    movb %dl, (%rsi)
    test %rax, %rax
    jnz .Lloop_conv
    mov $1, %rax
    mov $1, %rdi
    mov %rcx, %rdx
    syscall
    add $32, %rsp
    pop %rbp
    ret