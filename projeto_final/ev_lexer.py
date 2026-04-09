import re

#definição dos tipos de tokens para a Linguagem Fun

TOKENS = [
    ('NUM',      r'\d+'),
    ('FUN',      r'fun\b'),     #nova palavra-chave para funções
    ('VAR',      r'var\b'),     #nova palavra-chave para variáveis
    ('MAIN',     r'main\b'),    #nova palavra-chave para o bloco principal
    ('IF',       r'if\b'),
    ('ELSE',     r'else\b'),
    ('WHILE',    r'while\b'),
    ('RETURN',   r'return\b'),
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'),
    ('LBRACE',   r'\{'),
    ('RBRACE',   r'\}'),
    ('LBRACKET', r'\['),
    ('RBRACKET', r'\]'),
    ('COMMA',    r','),        
    ('LE',       r'<='),
    ('GE',       r'>='),
    ('NEQ',      r'!='),
    ('PLUS_ASSIGN',  r'\+='),
    ('MINUS_ASSIGN', r'-='),
    ('MUL_ASSIGN',   r'\*='),
    ('DIV_ASSIGN',   r'/='),
    ('EQ',       r'=='),
    ('ASSIGN',   r'='),
    ('LT',       r'<'),
    ('GT',       r'>'),
    ('PLUS',     r'\+'),
    ('MINUS',    r'-'),
    ('MUL',      r'\*'),
    ('DIV',      r'/'),
    ('LPAREN',   r'\('),
    ('RPAREN',   r'\)'),
    ('SEMI',     r';'),
    ('COMMENT',  r'#.*'),
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
    
    #mapeamento atualizado de palavras-chave
    keywords = {
        'fun': 'FUN', 
        'var': 'VAR', 
        'main': 'MAIN', 
        'if': 'IF', 
        'else': 'ELSE', 
        'while': 'WHILE', 
        'return': 'RETURN',
        'and': 'AND',
        'or': 'OR',
        'not': 'NOT'
    }
    
    while pos < len(codigo):
        match = None
        for type, pattern in TOKENS:
            regex = re.compile(pattern)
            match = regex.match(codigo, pos)
            if match:
                value = match.group(0)
                if type == 'WS' or type == 'COMMENT':
                    pass 
                elif type == 'ID':
                    t_type = keywords.get(value, 'ID')
                    tokens.append(Token(t_type, value))
                else:
                    tokens.append(Token(type, value))
                pos = match.end()
                break
        
        if not match:
            raise SyntaxError(f"Erro Léxico: Caractere inválido '{codigo[pos]}' na posição {pos}")
            
    return tokens

#teste rápido para a nova sintaxe
if __name__ == "__main__":
    exemplo_fun = "fun abs(x) { var y = 0; return y; } main { return 0; }"
    try:
        resultado = lexer(exemplo_fun)
        print("Tokens gerados com sucesso:")
        for t in resultado:
            print(t)
    except SyntaxError as e:
        print(e)