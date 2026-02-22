# expr1.s - Exemplo de entrega para a Atividade 03

  .section .text
  .globl _start

_start:
  ## Calculando (19 * 15 - 18 * 7) + (117 - 33)

  # 1. Calcular 19 * 15. Resultado em RAX.
  mov $19, %rax
  imul $15, %rax      # RAX = 285

  # 2. Calcular 18 * 7. Resultado em RBX.
  mov $18, %rbx
  imul $7, %rbx       # RBX = 126

  # 3. Calcular a primeira parte: (RAX - RBX). Resultado em RAX.
  sub %rbx, %rax      # RAX = 285 - 126 = 159

  # 4. Calcular 117 - 33. Reutilizando RBX.
  mov $117, %rbx
  sub $33, %rbx       # RBX = 84

  # 5. Somar as partes: (RAX + RBX). Resultado final em RAX.
  add %rbx, %rax      # RAX = 159 + 84 = 243

  call imprime_num
  call sair

  .include "runtime.s"