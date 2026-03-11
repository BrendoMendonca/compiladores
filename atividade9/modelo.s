#
# Modelo de saída para o compilador EV (Atividade 09)
#

.section .bss
## bss
# O compilador inserirá aqui as diretivas .lcomm para cada variável [cite: 142, 165]

.section .text
.globl _start

_start:
## saida do compilador deve ser inserida aqui
# O compilador inserirá aqui o código das atribuições e da expressão final [cite: 168, 169]

    # Após a expressão final, o resultado estará em RAX
    call imprime_num
    call sair

.include "runtime.s"