#!/usr/bin/env python3
# test_runner.py - monta, linka e executa testes automáticos para ec2_compiler.py
#
# Este script automatiza o fluxo:
#   1) gerar out.s a partir de uma expressão EC2 usando ec2_compiler.compile_expr_to_file
#   2) montar e linkar out.s com runtime.s (usando gcc -no-pie -nostartfiles)
#   3) executar o binário gerado e capturar a saída
#   4) comparar a saída com o valor esperado (calculado por ec.eval_ast)


import subprocess
import os
import sys
import shutil
import time
import ec2_compiler as ec

# ------------------------------------------------------------------------------
# Lista de expressões de teste (todas em conformidade com a gramática EC2)
# Cada expressão deve estar na forma aceita pelo parser:
#   <expressao> ::= (<expressao> <operador> <expressao>) | <literal-inteiro>
# Observação: literais não devem vir entre parênteses (por exemplo "17179869426" é válido,
#       mas "(17179869426)" não é).
# ------------------------------------------------------------------------------

TESTS = [
    "333",                                 # Literal simples
    "7+5*3",                               # Precedência: deve dar 22 (e não 36)
    "10-8-2",                              # Associatividade à esquerda: deve dar 0 (e não 4)
    "2*3+4*5",                             # Múltiplas precedências: deve dar 26
    "100/2/5",                             # Associatividade na divisão: deve dar 10 (e não 250)
    "10+20/2",                             # Divisão após soma: deve dar 20
    "(7+5)*3",                             # Parênteses forçando precedência: deve dar 36
    "2+3*4-5/1",                           # Mistura total: deve dar 9
    "100-(10+20)*2",                       # Parênteses com multiplicação externa: deve dar 40
    "((427/7)+(11*(231+5)))",              # Compatibilidade com o formato EC2 (com parênteses)
    "10-2-2-2",                            # Sequência longa de mesma precedência: deve dar 4
    "2*2*2*2"                              # Sequência longa de multiplicação: deve dar 16
]

# ------------------------------------------------------------------------------
# Configurações / caminhos de arquivo usados pelo runner
# ------------------------------------------------------------------------------
WORK_DIR = os.getcwd()                           # diretório atual de execução
OUT_S = os.path.join(WORK_DIR, "out.s")         # arquivo .s gerado pelo compilador
PROG = os.path.join(WORK_DIR, "prog")           # nome do executável gerado
RUNTIME_S = "runtime.s"                         # runtime que contém imprime_num / sair
MODELO_S = "modelo.s"                           # modelo.s (template) usado pelo compilador

# ------------------------------------------------------------------------------
# Função utilitária para executar comandos de shell e capturar saída
# - cmd: string com o comando a ser executado (ex.: "gcc -no-pie ...")
# - cwd: diretório de trabalho (opcional)
# - timeout: tempo máximo em segundos para o comando
# Retorna: (returncode, stdout_text, stderr_text)
# ------------------------------------------------------------------------------
def run_cmd(cmd, cwd=None, timeout=10):
    res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, timeout=timeout)
    return res.returncode, res.stdout.decode('utf-8', errors='ignore'), res.stderr.decode('utf-8', errors='ignore')

# ------------------------------------------------------------------------------
# Função principal que compila uma expressão EC2, gera .s, monta, linka e executa.
# Retorna uma tupla: (ok: bool, mensagem: str | None, valor_retornado: int | None)
# - ok: True se o teste passou (saída do programa == valor esperado)
# - mensagem: texto de erro em caso de falha (ou None se ok)
# - valor_retornado: inteiro produzido pelo programa (quando aplicável)
# ------------------------------------------------------------------------------
def build_and_run(expr):
    # 1) gerar out.s (chama o compilador)
    try:
        ast, out_text = ec.compile_expr_to_file(expr, OUT_S, modelo_path=MODELO_S, do_fold=True)
    except Exception as e:
        # erro durante lexing/parsing/folding/geração
        return False, f"Erro durante compilação: {e}", None

    # 2) verificar se o runtime.s existe no diretório atual
    if not os.path.exists(RUNTIME_S):
        return False, f"runtime.s não encontrado no diretório ({os.path.abspath(RUNTIME_S)})", None

    # 3) montar + linkar com gcc
    # -no-pie evita problemas de realocação em sistemas que linkam PIE por padrão
    # -nostartfiles evita incluir arquivos de inicialização do C (usamos _start)
    cmd = f"gcc -no-pie -nostartfiles {OUT_S} {RUNTIME_S} -o {PROG}"
    code, out, err = run_cmd(cmd)
    if code != 0:
        # gcc/as/ld retornaram erro; reportamos stdout/stderr para debug
        return False, f"Erro no gcc:\nSTDOUT:{out}\nSTDERR:{err}", None

    # 4) executar o programa gerado e capturar saída (stdout)
    # usamos o nome base do PROG para execução no diretório atual
    code, out, err = run_cmd(f"./{os.path.basename(PROG)}")
    if code != 0:
        # o processo rodou mas retornou código diferente de 0
        return False, f"Programa retornou código {code}. STDERR:\n{err}", None

    # 5) calcular valor esperado (avaliando a AST com o avaliador do compilador)
    try:
        expected = ec.eval_ast(ast)
    except Exception as e:
        return False, f"Erro avaliando AST no runner: {e}", None

    # 6) interpretar a saída do programa (esperamos apenas um número e newline)
    got_text = out.strip()  # remove whitespace ao redor
    try:
        got_int = int(got_text)
    except:
        # saída inesperada (não é um inteiro)
        return False, f"Saída inesperada do programa: '{got_text}'", got_text

    # 7) comparar e retornar resultado
    ok = (got_int == expected)
    msg = None
    if not ok:
        msg = f"Esperado {expected}, obtido {got_int}"
    return ok, msg, got_int

# ------------------------------------------------------------------------------
# Função principal do script: itera sobre a lista de testes e imprime um resumo.
# ------------------------------------------------------------------------------
def main():
    print("Executando testes EC2...")
    passed = 0
    failed = 0

    for e in TESTS:
        print(f"\nTeste: {e}")
        ok, msg, got = build_and_run(e)
        if ok:
            print(f"  OK — saída: {got}")
            passed += 1
        else:
            print(f"  ERRO — {msg}")
            failed += 1

    # resumo final
    print("\nResumo:")
    print(f"  Passaram: {passed}")
    print(f"  Falharam: {failed}")

# ponto de entrada
if __name__ == "__main__":
    main()

