import sys
from ev_lexer import lexer
from ev_parser import TokenStream, parse_programa
from ev_semantics import SemanticAnalyzer, SemanticError

def compiler():
    if len(sys.argv) < 3:
        print("Uso: python3 ev_compiler.py entrada.ev saida.s")
        return

    arquivo_entrada = sys.argv[1]
    arquivo_saida = sys.argv[2]

    try:
        # 1. Leitura do arquivo fonte
        with open(arquivo_entrada, 'r') as f:
            codigo = f.read()

        # 2. Análise Léxica
        tokens = lexer(codigo)

        # 3. Análise Sintática (Parser)
        ts = TokenStream(tokens)
        ast = parse_programa(ts)

        # 4. Análise Semântica (A grande novidade da Atividade 10)
        # Verifica se variáveis foram declaradas antes de usadas [cite: 126]
        analyzer = SemanticAnalyzer()
        analyzer.visit(ast)

        # 5. Geração de Código
        code_lines = []
        
        # Cabeçalho padrão Assembly x86-64
        code_lines.append(".section .text")
        code_lines.append(".globl _start")
        code_lines.append("_start:")
        
        # Gera as instruções a partir da AST
        ast.gen(code_lines)
        
        # 1. O resultado da última expressão (do return) está em RAX. 
        # Passamos para RDI, que é o argumento esperado pela função print_int.
        code_lines.append("    mov %rax, %rdi")

        # 2. Chamamos a função de conversão e escrita que está no runtime.s
        code_lines.append("    call print_int") 

        # 3. Agora sim, finalizamos o processo com a syscall de exit (60)
        code_lines.append("    mov $0, %rdi") 
        code_lines.append("    mov $60, %rax")
        code_lines.append("    syscall")

        # 6. Seção BSS (Reserva de memória para variáveis) 
        code_lines.append("\n.section .bss")
        for var in analyzer.symbol_table:
            code_lines.append(f"{var}: .quad 0")

        # Gravação do arquivo final
        with open(arquivo_saida, 'w') as f:
            for line in code_lines:
                f.write(line + "\n")
        
        print(f"✅ Compilação concluída com sucesso! Arquivo gerado: {arquivo_saida}")

    except SemanticError as e:
        print(f"❌ Erro Semântico: {e}")
        sys.exit(1)
    except SyntaxError as e:
        print(f"❌ Erro de Sintaxe: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro Crítico: {e}")
        sys.exit(1)

if __name__ == "__main__":
    compiler()