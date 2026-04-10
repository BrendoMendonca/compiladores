import re

#definição dos tipos de tokens para a Linguagem Fun

TOKENS = [
    ('NUM',      r'\d+'), #sequência de 1 ou mais dígitos de números inteiros
    ('FUN',      r'fun\b'),     #nova palavra-chave para funções
    ('VAR',      r'var\b'),     #nova palavra-chave para variáveis
    ('MAIN',     r'main\b'),    #nova palavra-chave para o bloco principal
    ('IF',       r'if\b'),#palavra-chave para estrutura condicional se
    ('ELSE',     r'else\b'),#palavra-chave para estrutura condicional senão
    ('WHILE',    r'while\b'),#palavra-chave para laço de repetição enquanto
    ('RETURN',   r'return\b'), #palavra-chave para retornar um valor de uma função
    ('ID',       r'[a-zA-Z_][a-zA-Z0-9_]*'), #nomes de variáveis/funções
    ('LBRACE',   r'\{'), #abre chaves '{' para início de um bloco de código
    ('RBRACE',   r'\}'),# fecha chaves '{' fim de um bloco de código
    ('LBRACKET', r'\['),#abre colchetes '[' início de um array
    ('RBRACKET', r'\]'),#fecha colchetes '[' fim de um array
    ('COMMA',    r','),#vírgula ',' para separar argumentos em funções
    ('LE',       r'<='),#operador de comparação: Menor ou igual
    ('GE',       r'>='),#operador de comparação: Maior ou igual
    ('NEQ',      r'!='),#operador de comparação: Diferente
    ('PLUS_ASSIGN',  r'\+='),#atribuição composta: Soma e guarda
    ('MINUS_ASSIGN', r'-='),#atribuição composta: Subtrai e guarda
    ('MUL_ASSIGN',   r'\*='),#atribuição composta: Multiplica e guarda
    ('DIV_ASSIGN',   r'/='),#atribuição composta: Divide e guarda
    ('EQ',       r'=='),#operador de comparação: Igualdade exata
    ('ASSIGN',   r'='),#atribuição simples: Grava um valor em uma variável
    ('LT',       r'<'),#operador de comparação: Estritamente menor que
    ('GT',       r'>'),#operador de comparação: Estritamente maior que
    ('PLUS',     r'\+'),#operador aritmético: Adição
    ('MINUS',    r'-'),#operador aritmético: Subtração
    ('MUL',      r'\*'),#operador aritmético: Multiplicação
    ('DIV',      r'/'),#operador aritmético: Divisão
    ('LPAREN',   r'\('),#abre parênteses '(' para agrupamento de expressões e parâmetros
    ('RPAREN',   r'\)'),#fehca parênteses '(' para agrupamento de expressões e parâmetros
    ('SEMI',     r';'),#ponto e vírgula ';' marca o fim de um comando
    ('COMMENT',  r'#.*'),#comentários
    ('WS',       r'\s+'),#espaço em branco
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