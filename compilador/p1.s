#
  # modelo de saida para o compilador
  #
  .section .text
  .globl _start

_start:
  ## saida do compilador deve ser inserida aqui
  mov $88, %rax
  call imprime_num
  call sair

  .include "runtime.s"
