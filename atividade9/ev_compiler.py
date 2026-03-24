import sys
import os
from ev_lexer import lexer
from ev_parser import TokenStream, parse_programa
from ev_semantics import SemanticAnalyzer, SemanticError

def compile_ev_to_file(codigo_fonte, out_path, modelo_path="modelo.s"):
    #pipeline
    tokens = lexer(codigo_fonte)
    ts = TokenStream(tokens)
    ast = parse_programa(ts)
    
    #semântica (Atividade 09)
    analyzer = SemanticAnalyzer()
    analyzer.visit(ast) 
    
    #geração da Seção BSS(variáveis)
    #coleta nomes únicos de variáveis declaradas 
    var_names = list(dict.fromkeys([d.nome for d in ast.declaracoes]))
    bss_lines = [".section .bss"]
    for name in var_names:
        bss_lines.append(f"    .lcomm {name}, 8") # 8 bytes por variável
    bss_text = "\n".join(bss_lines)

    #geração do Código TEXT
    code_lines = []
    ast.gen(code_lines)
    code_text = "\n".join(code_lines)

    #leitura do Modelo e Gravação 
    with open(modelo_path, "r") as f:
        model = f.read()

    out_text = model.replace("## bss", bss_text)
    out_text = out_text.replace("## saida do compilador deve ser inserida aqui", code_text)

  
    with open(out_path, "w") as f:
        f.write(out_text)
    
    print(f"Arquivo {out_path} gerado com sucesso!")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 ev_compiler.py <arquivo_entrada.ev> <arquivo_saida.s>")
        sys.exit(1)

    entrada = sys.argv[1]
    saida = sys.argv[2]

    try:
        with open(entrada, 'r') as f:
            conteudo = f.read()
        
        compile_ev_to_file(conteudo, saida)
        
    except FileNotFoundError:
        print(f"Erro: O arquivo '{entrada}' não foi encontrado.")
        sys.exit(1)
    except SemanticError as e:
        #captura especificamente o erro de variável não declarada
        print(f"Erro Semântico: {e}")
        sys.exit(1) #o test_runner detecta a falha
    except Exception as e:
        print(f"Erro inesperado: {e}")
        sys.exit(1)