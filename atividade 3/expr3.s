# expr3.s - Atividade 03: (42 - 222) * 11 + (1988)

  .section .text
  .globl _start

_start:
  ## Calculando (42 - 222) * 11 + (1988)

  # 1. Calcular a Subtração (42 - 222). Resultado em RAX.
  mov $42, %rax
  sub $222, %rax     # RAX = 42 - 222 = -180

  # 2. Multiplicar por 11 (IMUL). Resultado em RAX.
  # IMUL com operando imediato é uma forma que pode ser usada. [cite: 232]
  imul $11, %rax     # RAX = -180 * 11 = -1980

  # 3. Somar 1988. Resultado final em RAX.
  add $1988, %rax    # RAX = -1980 + 1988 = 8

  call imprime_num
  call sair

  .include "runtime.s"