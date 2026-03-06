#!/usr/bin/env python3
import sys

# O nome do compilador é tirado do próprio script
COMPILADOR_NOME = sys.argv[0]

def compilar_ci(nome_arquivo_entrada):
    """
    Realiza a compilação de um programa na linguagem CI (Constantes Inteiras).
    O resultado (código assembly) é escrito na saída padrão (stdout).
    """
    try:
        # 1. Ler o Arquivo de Entrada
        with open(nome_arquivo_entrada, 'r') as f:
            # Lemos e removemos espaços em branco/quebras de linha desnecessários
            conteudo = f.read().strip()

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo_entrada}' não encontrado.", file=sys.stderr)
        sys.exit(1)
    
    # --- Etapa de Análise (Verificação de Sintaxe CI) ---
    
    # 2. Verificar se o conteúdo é uma constante inteira válida (apenas dígitos)
    # [cite: 14] Um programa CI é apenas uma constante inteira, formada por um ou mais dígitos.
    if not conteudo:
        print(f"Erro de sintaxe CI: Arquivo vazio. Esperado: <literal-inteiro>", file=sys.stderr)
        sys.exit(1)

    if not conteudo.isdigit():
        # [cite: 73] Um erro de sintaxe significa que o arquivo de entrada não contém uma constante inteira correta (por exemplo, inclui letras).
        print(f"Erro de sintaxe CI: Programa deve conter apenas dígitos. Conteúdo inválido: '{conteudo}'", file=sys.stderr)
        sys.exit(1)
        
    # Se chegamos aqui, o valor é uma constante válida.
    valor_constante = conteudo

    # --- Etapa de Síntese (Geração de Código) ---
    
    # O compilador gera a instrução de movimentação: mov $VALOR, %rax
    # [cite: 38] O compilador CI precisa gerar é apenas uma instrução que coloca o resultado do programa no registrador RAX.
    codigo_gerado = f"  mov ${valor_constante}, %rax"
    
    # O código gerado é inserido no modelo de saída.
    # [cite: 45] A linha gerada pelo compilador deve ser incluída em um modelo de arquivo assembly.
    assembly_completo = f"""
  #
  # modelo de saida para o compilador
  #
  .section .text
  .globl _start

_start:
  ## saida do compilador deve ser inserida aqui
{codigo_gerado}
  call imprime_num
  call sair

  .include "runtime.s"
"""
    # 4. Escrever o Arquivo de Saída na saída padrão (stdout)
    # A saída será redirecionada para p1.s no terminal.
    print(assembly_completo.strip())

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: {COMPILADOR_NOME} <arquivo_de_entrada.ci>", file=sys.stderr)
        sys.exit(1)
        
    compilar_ci(sys.argv[1])