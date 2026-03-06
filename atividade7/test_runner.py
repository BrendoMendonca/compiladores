import subprocess
import os
import sys
import ec1_compiler as ec

# Configurações de caminhos
RUNTIME_S = "runtime.s"
MODELO_S = "modelo.s"
OUT_S = "out.s"
PROG_EXE = "./prog"

# Lista de Testes Específicos para Atividade 07 (EC1)
# Lembrete: EC1 exige parênteses para cada operação binária
TESTS = [
    ("333", 333),
    ("(2+2)", 4),
    ("(10-5)", 5),
    ("(3*4)", 12),
    ("(20/5)", 4),
    ("((10+5)*2)", 30),
    ("(100-(20*3))", 40),
    ("((427/7)+(11*(231+5)))", 2657), # Caso complexo do PDF
    ("1234567890123", 1234567890123) # Teste de Literal Grande (movabs)
]

def run_test(expr, expected):
    print(f"Testando: {expr:30}", end="")
    
    try:
        # 1. Chamar o compilador modularizado
        # Ele já usa internamente o ec1_lexer, ec1_parser e ec1_ast
        ec.compile_expr_to_file(expr, OUT_S, modelo_path=MODELO_S, do_fold=True)

        # 2. Montar e Linkar (GCC)
        # -no-pie e -nostartfiles são necessários para o nosso runtime.s
        cmd_gcc = ["gcc", "-no-pie", "-nostartfiles", OUT_S, RUNTIME_S, "-o", PROG_EXE]
        subprocess.run(cmd_gcc, check=True, capture_output=True)

        # 3. Executar o programa gerado e capturar a saída
        result = subprocess.run([PROG_EXE], capture_output=True, text=True, check=True)
        actual = int(result.stdout.strip())

        # 4. Validar resultado
        if actual == expected:
            print("\033[92m[OK]\033[0m")
            return True
        else:
            print(f"\033[91m[FALHA]\033[0m (Esperado: {expected}, Obtido: {actual})")
            return False

    except Exception as e:
        print(f"\033[91m[ERRO NO COMPILADOR]\033[0m: {e}")
        return False

def main():
    # Verifica se os arquivos base existem
    for f in [RUNTIME_S, MODELO_S]:
        if not os.path.exists(f):
            print(f"Erro: Arquivo {f} não encontrado no diretório atual.")
            sys.exit(1)

    print("="*50)
    print("INICIANDO TESTES DA ATIVIDADE 07 (MODULAR)")
    print("="*50)

    success_count = 0
    for expr, expected in TESTS:
        if run_test(expr, expected):
            success_count += 1

    print("="*50)
    print(f"Resultado Final: {success_count}/{len(TESTS)} testes passaram.")
    
    # Limpeza opcional de arquivos temporários
    if success_count == len(TESTS):
        if os.path.exists(OUT_S): os.remove(OUT_S)
        if os.path.exists(PROG_EXE): os.remove(PROG_EXE)

if __name__ == "__main__":
    main()