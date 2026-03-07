from ec1_lexer import lexer

def realizar_testes():
    testes = [
        ("Espaços simples", "1 + 2"),
        ("Tabs e Newlines", "10\t+\n(5 * 2)"),
        ("Expressão colada", "((7+11)*2)"),
    ]

    print("--- Testes de Sucesso ---")
    for nome, expr in testes:
        print(f"Testando {nome}: {expr}")
        print(lexer(expr))
        print("-" * 20)

    print("\n--- Teste de Erro Léxico ---")
    try:
        lexer("7 @ 5")
    except SyntaxError as e:
        print(f"Erro detectado corretamente: {e}")

if __name__ == "__main__":
    realizar_testes()