import subprocess
import os

# Lista de testes: (codigo, resultado_esperado, deve_falhar_na_semantica)
testes = [
    # --- Casos de Sucesso ---
    ("x = 10; y = x + 5; = y * 2", 30, False),
    ("largura = 30; comprimento = 40; = largura + largura + comprimento + comprimento", 140, False),
    ("a = (7+4)*12; b = a*3+11; = (a*b)+(a*11)+(b*13)", 60467, False),
    
    # --- Casos de Erro Semântico (Atividade 09) ---
    ("x = y + 5; y = 10; = x", None, True),      # y usado antes de ser declarado
    ("a = 10; = a + b", None, True),             # b nunca declarado
    ("x = x + 1; = x", None, True),              # auto-referência antes de existir na tabela
]

def run_test(i, code, expected, should_fail):
    print(f"Teste {i+1}: ", end="")
    
    # 1. Cria arquivo temporário .ev
    with open("temp.ev", "w") as f:
        f.write(code)

    # 2. Tenta compilar
    res_comp = subprocess.run(["python3", "ev_compiler.py", "temp.ev", "out.s"], 
                              capture_output=True, text=True)

    if should_fail:
        if res_comp.returncode != 0:
            print("✅ PASSOU (Erro semântico detectado corretamente)")
            return True
        else:
            print("❌ FALHOU (Deveria ter detectado erro semântico, mas compilou)")
            return False

    if res_comp.returncode != 0:
        print(f"❌ FALHOU (Erro de compilação inesperado: {res_comp.stderr})")
        return False

    # 3. Monta e Executa (GCC)
    try:
        subprocess.run(["gcc", "-no-pie", "-nostartfiles", "out.s", "-o", "prog"], check=True)
        res_exec = subprocess.run(["./prog"], capture_output=True, text=True)
        output = int(res_exec.stdout.strip())

        if output == expected:
            print(f"✅ PASSOU (Resultado: {output})")
            return True
        else:
            print(f"❌ FALHOU (Esperado {expected}, obtido {output})")
            return False
    except Exception as e:
        print(f"❌ ERRO NA EXECUÇÃO: {e}")
        return False

# Execução da bateria
sucessos = 0
for i, (c, e, f) in enumerate(testes):
    if run_test(i, c, e, f):
        sucessos += 1

print(f"\nResultado Final: {sucessos}/{len(testes)} testes passaram.")