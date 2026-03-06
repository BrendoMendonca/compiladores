# expr2.s - Atividade 03: (9 * 8 * 7) / (6 * 5 * 4 * 3 * 2)

  .section .text
  .globl _start

_start:
  ## Calculando (9 * 8 * 7) / (6 * 5 * 4 * 3 * 2)

  # 1. Calcular o Numerador (504). Resultado em RAX.
  mov $9, %rax
  imul $8, %rax      # RAX = 72
  imul $7, %rax      # RAX = 504

  # 2. Calcular o Denominador (720). Resultado em RBX.
  mov $6, %rbx
  imul $5, %rbx      # RBX = 30
  imul $4, %rbx      # RBX = 120
  imul $3, %rbx      # RBX = 360
  imul $2, %rbx      # RBX = 720

  # 3. Preparar a Divisão (RAX / RBX).
  # A instrução IDIV usa RAX como dividendo e coloca o quociente em RAX.
  # É obrigatório executar CQO antes para estender o sinal de RAX para RDX:RAX. [cite: 249, 251]
  cqo
  idiv %rbx          # RAX = 504 / 720 (Quociente: 0)

  call imprime_num
  call sair

  .include "runtime.s"