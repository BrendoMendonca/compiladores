import re

# Definição dos tipos de tokens para a Linguagem Cmd
# Adicionados: LBRACE, RBRACE, LT, GT, EQ, IF, ELSE, WHILE, RETURN 
TOKENS = [
    ('NUM',      r'\d+'),
    ('IF',       r'if\b'),      # \b garante que 'if' não case com 'if_variable'
    ('ELSE',     r'else\b'),
    ('WHILE',    r'while\b'),
    ('RETURN',   r'return\b'),
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('LBRACE',   r'\{'),        # Delimitador de corpo
    ('RBRACE',   r'\}'),
    ('EQ',       r'=='),        # Comparação de igualdade
    ('ASSIGN',   r'='),         # Atribuição ou Declaração
    ('LT',       r'<'),         # Menor que
    ('GT',       r'>'),         # Maior que
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('MUL',      r'\*'),
    ('DIV',      r'/'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('SEMI',     r';'),
    ('WS',       r'\s+'),
]

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value})"

def lexer(codigo):
    tokens = []
    pos = 0
    
    # Mapeamento de palavras-chave para evitar que sejam tratadas como ID
    keywords = {'if': 'IF', 'else': 'ELSE', 'while': 'WHILE', 'return': 'RETURN'}
    
    while pos < len(codigo):
        match = None
        for type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(codigo, pos)
            if match:
                value = match.group(0)
                if type == 'WS':
                    pass # Ignora espaços
                elif type == 'ID':
                    # Se o ID for uma palavra-chave, altera o tipo 
                    t_type = keywords.get(value, 'ID')
                    tokens.append(Token(t_type, value))
                else:
                    tokens.append(Token(type, value))
                pos = match.end()
                break
        
        if not match:
            raise SyntaxError(f"Erro Léxico: Caractere inválido '{codigo[pos]}' na posição {pos}")
            
    return tokens

# Teste rápido
# --- ÁREA DE TESTES NO CÓDIGO ---
if __name__ == "__main__":
    # 1. Teste de Sucesso
    print("--- Teste de Sucesso ---")
    try:
        exemplo = "x = 10; { return x; }"
        print(lexer(exemplo))
    except SyntaxError as e:
        print(f"Erro inesperado: {e}")

    print("\n--- Testes de Erro Léxico ---")
    
    # Lista de códigos que DEVEM dar erro na Linguagem Cmd [cite: 104, 105]
    testes_proibidos = [
        "x = 10 $ 5;",       # Caractere '$' não existe na gramática [cite: 61]
        "valor#total = 1;",   # Caractere '#' é inválido [cite: 66]
        "if x @ 0 { }"        # Caractere '@' é inválido [cite: 105]
    ]

    for i, codigo in enumerate(testes_proibidos):
        try:
            lexer(codigo)
            print(f"Caso {i+1}: FALHOU (Aceitou código inválido: {codigo})")
        except SyntaxError as e:
            # O comportamento correto é cair aqui
            print(f"Caso {i+1}: PASSOU (Detectou erro corretamente: {e})")