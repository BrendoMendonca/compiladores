class Position:
    """Rastreia a localização exata do cursor no código fonte"""
    def __init__(self, offset=0, line=1, column=1):
        self.offset = offset
        self.line = line
        self.column = column

    def __repr__(self):
        return f"(linha {self.line}, coluna {self.column})"

class Token:
    """Objeto que representa cada símbolo identificado"""
    def __init__(self, position, lexeme, kind):
        self.position = position
        self.lexeme = lexeme
        self.kind = kind

    def __repr__(self):
        return f"Token({self.kind}, '{self.lexeme}', {self.position})"

def lexer(entrada: str):
    """Transforma a string de entrada em uma lista de objetos Token"""
    tokens = []
    i = 0
    pos = Position(0, 1, 1)

    while i < len(entrada):
        c = entrada[i]

        # Ignora espaços em branco
        if c in ' \t\r':
            pos.offset += 1; pos.column += 1; i += 1
            continue

        # Trata quebras de linha para manter a contagem correta
        if c == '\n':
            pos.line += 1; pos.column = 1; pos.offset += 1; i += 1
            continue

        # Reconhecimento de símbolos de um único caractere
        mapa_simbolos = {
            '(': "OPEN_P", ')': "CLOSE_P",
            '+': "SUM",    '-': "SUB",
            '*': "MUL",    '/': "DIV"
        }

        if c in mapa_simbolos:
            tokens.append(Token(Position(pos.offset, pos.line, pos.column), c, mapa_simbolos[c]))
            pos.offset += 1; pos.column += 1; i += 1
            continue

        # Reconhecimento de literais inteiros (números)
        if c.isdigit():
            start = Position(pos.offset, pos.line, pos.column)
            lex = ""
            while i < len(entrada) and entrada[i].isdigit():
                lex += entrada[i]
                pos.offset += 1; pos.column += 1; i += 1
            tokens.append(Token(start, lex, "LITERAL"))
            continue

        # Caso encontre um caractere não previsto na gramática EC2
        raise SyntaxError(f"Erro Léxico: Caractere inválido '{c}' em {pos}")

    # Garante que o Parser saiba onde o arquivo termina
    tokens.append(Token(pos, "", "EOF"))
    return tokens