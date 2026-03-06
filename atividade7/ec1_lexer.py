class Position:
    """Rastreia linha e coluna para reporte de erros"""
    def __init__(self, offset=0, line=1, column=1):
        self.offset = offset
        self.line = line
        self.column = column

    def __repr__(self):
        return f"(linha {self.line}, coluna {self.column})"

class Token:
    """Representa os símbolos da linguagem EC1"""
    def __init__(self, position, lexeme, kind):
        self.position = position
        self.lexeme = lexeme
        self.kind = kind

    def __repr__(self):
        return f"Token({self.kind}, '{self.lexeme}', {self.position})"

def lexer(entrada: str):
    """Gera a lista de tokens para o compilador EC1"""
    tokens = []
    i = 0
    pos = Position(0, 1, 1)

    while i < len(entrada):
        c = entrada[i]

        # Ignora espaços em branco
        if c in ' \t\r':
            pos.offset += 1; pos.column += 1; i += 1
            continue

        # Trata quebras de linha
        if c == '\n':
            pos.line += 1; pos.column = 1; pos.offset += 1; i += 1
            continue

        # Símbolos da linguagem EC1 [cite: 26, 27]
        mapa_simbolos = {
            '(': "OPEN_P", ')': "CLOSE_P",
            '+': "SUM",    '-': "SUB",
            '*': "MUL",    '/': "DIV"
        }

        if c in mapa_simbolos:
            tokens.append(Token(Position(pos.offset, pos.line, pos.column), c, mapa_simbolos[c]))
            pos.offset += 1; pos.column += 1; i += 1
            continue

        # Literais Inteiros [cite: 28, 29]
        if c.isdigit():
            start = Position(pos.offset, pos.line, pos.column)
            lex = ""
            while i < len(entrada) and entrada[i].isdigit():
                lex += entrada[i]
                pos.offset += 1; pos.column += 1; i += 1
            tokens.append(Token(start, lex, "LITERAL"))
            continue

        # Erro léxico para caracteres inválidos
        raise SyntaxError(f"Erro Léxico: Caractere inválido '{c}' em {pos}")

    tokens.append(Token(pos, "", "EOF"))
    return tokens