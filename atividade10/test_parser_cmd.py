from ev_lexer import lexer
from ev_parser import TokenStream, parse_programa

def testar_compilador_cmd():
    # Exemplo da página 4 do guia [cite: 32-42]
    codigo_ev = """
    a = 1;
    b = 2;
    c = 3;
    delta = b * b - 4 * a * c;
    {
        if delta < 0 {
            delta = 0 - delta;
        } else {
            delta = delta;
        }
        return delta;
    }
    """

    print("--- Iniciando Teste da Linguagem Cmd ---")
    
    try:
        # 1. Análise Léxica
        tokens = lexer(codigo_ev)
        print("1. Léxico: OK")

        # 2. Análise Sintática (Parser)
        ts = TokenStream(tokens)
        ast = parse_programa(ts)
        print("2. Sintático: OK (AST construída)")

        # 3. Geração de Código
        codigo_assembly = []
        ast.gen(codigo_assembly)
        print("3. Geração de Código: OK\n")

        print("--- Assembly Resultante (Trecho de Comandos) ---")
        for linha in codigo_assembly:
            print(linha)

    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    testar_compilador_cmd()