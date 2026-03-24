import sys

class Position:
    def __init__(self, offset=0, line=1, column=1):
        self.offset, self.line, self.column = offset, line, column
    def __repr__(self): return f"(linha {self.line}, coluna {self.column})"

class Token:
    def __init__(self, position, lexeme, kind):
        self.position, self.lexeme, self.kind = position, lexeme, kind
    def __repr__(self): return f"Token({self.kind}, '{self.lexeme}', {self.position})"

def lexer(entrada: str):
    tokens = []
    i, pos = 0, Position()
    while i < len(entrada):
        c = entrada[i]
        if c in ' \t\r': i += 1; pos.column += 1; continue
        if c == '\n': i += 1; pos.line += 1; pos.column = 1; continue

        #identificadores (começam com letra)
        if c.isalpha():
            start = Position(i, pos.line, pos.column)
            lex = ""
            while i < len(entrada) and (entrada[i].isalnum() or entrada[i] == '_'):
                lex += entrada[i]; i += 1; pos.column += 1
            tokens.append(Token(start, lex, "IDENT"))
            continue

        #literais Inteiros
        if c.isdigit():
            start = Position(i, pos.line, pos.column)
            lex = ""
            while i < len(entrada) and entrada[i].isdigit():
                lex += entrada[i]; i += 1; pos.column += 1
            tokens.append(Token(start, lex, "LITERAL"))
            continue

        #símbolos 
        mapa = {'(': "OPEN_P", ')': "CLOSE_P", '+': "SUM", '-': "SUB", 
                '*': "MUL", '/': "DIV", '=': "ASSIGN", ';': "SEMI"}
        if c in mapa:
            tokens.append(Token(Position(i, pos.line, pos.column), c, mapa[c]))
            i += 1; pos.column += 1; continue

        raise SyntaxError(f"Erro Léxico: Caractere inválido '{c}' em {pos}")
    tokens.append(Token(pos, "", "EOF"))
    return tokens