#
# Modelo de saída para o compilador EV (Atividade 09)
#

.section .bss
## bss
# O compilador inserirá aqui as diretivas .lcomm para cada variável 

.section .text
.globl _start

_start:
## saida do compilador deve ser inserida aqui
# O compilador inserirá aqui o código das atribuições e da expressão final

    # Após a expressão final, o resultado estará em RAX
    call imprime_num
    call sair

.include "runtime.s"