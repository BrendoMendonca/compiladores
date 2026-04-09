import sys
from ev_lexer import lexer
from ev_parser import TokenStream, parse_programa
from ev_semantics import SemanticAnalyzer
from ev_ast import ProgramaNode

def compile_ev(input_file, output_file):
    #lê o arquivo fonte (.ev)
    try:
        with open(input_file, 'r') as f:
            source = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{input_file}' não encontrado.")
        return

    #análise Léxica
    tokens = lexer(source)
    ts = TokenStream(tokens)

    #análise Sintática (Gera a AST)
    #a gramática agora exige 'main' e suporta 'fun' e 'var'
    ast = parse_programa(ts)

    #análise Semântica
    #calcula offsets (RBP), verifica escopos e assinaturas de funções
    analyzer = SemanticAnalyzer()
    try:
        analyzer.visit(ast)
    except Exception as e:
        print(f"❌ Erro Semântico: {e}")
        return

    #geração de Código Assembly
    code = []
    
    #cabeçalho do arquivo
    code.append("# Codigo gerado pelo compilador Fun")
    
 #seção BSS para variáveis globais
    code.append(".section .bss")
    for name, type_info in analyzer.global_symbols.items():
        if type_info == 'var':
            code.append(f"{name}: .quad 0")
        elif isinstance(type_info, tuple) and type_info[0] == 'array':
            size = type_info[1]
            code.append(f"{name}: .zero {size * 8}") #aloca os bytes necessários

    #seção Text (Código)
    code.append("\n.section .text")
    code.append(".globl _start")
    
    #a AST gera o código das funções e do bloco _start
    ast.gen(code)

    #finalização do programa principal (Saída limpa)
    code.append("\n    # Finalizacao")
    code.append("    mov %rax, %rdi")
    code.append("    call print_int") #chama a função de impressão do runtime
    code.append("    mov $60, %rax")   #syscall exit
    code.append("    xor %rdi, %rdi")  #status 0
    code.append("    syscall")

    #inclusão do runtime para suporte a print_int 
    code.append("\n.include \"runtime.s\"")

    #salva o resultado no arquivo de saída (.s)
    with open(output_file, 'w') as f:
        f.write("\n".join(code))
    
    print(f"✅ Compilação concluída com sucesso! Arquivo gerado: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 ev_compiler.py <entrada.ev> <saida.s>")
    else:
        compile_ev(sys.argv[1], sys.argv[2])