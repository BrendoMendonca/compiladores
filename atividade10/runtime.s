.section .text
.globl print_int

print_int:
    push %rbp
    mov %rsp, %rbp
    sub $32, %rsp          # Reserva espaço para os dígitos
    
    mov %rdi, %rax         # Valor para converter
    mov $10, %rbx          # Divisor
    lea 31(%rsp), %rsi     # RSI aponta para o fim do buffer (última posição)
    movb $10, (%rsi)       # Coloca o caractere de nova linha '\n'
    
    mov $1, %rcx           # Contador de caracteres (começa com 1 para o \n)

.Lloop_conv:
    dec %rsi               # Anda para trás no buffer
    inc %rcx               # Aumenta o contador
    xor %rdx, %rdx
    div %rbx               # Divide RAX por 10, resto em RDX
    add $48, %dl           # Converte para ASCII
    movb %dl, (%rsi)       # Guarda o dígito
    
    test %rax, %rax        # Ainda tem números para dividir?
    jnz .Lloop_conv

    # Syscall write(1, buffer, len)
    mov $1, %rax           # sys_write
    mov $1, %rdi           # stdout
    mov %rcx, %rdx         # Quantidade de caracteres calculada
    # RSI já aponta para o início da string no buffer
    syscall

    add $32, %rsp
    pop %rbp
    ret
    