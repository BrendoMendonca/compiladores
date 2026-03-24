from ev_ast import Programa, Declaracao, Const, OpBin, Var

class TokenStream:
    def __init__(self, tokens):
        self.tokens, self.i = tokens, 0
    def next(self):
        t = self.tokens[self.i]
        if t.kind != "EOF": self.i += 1
        return t
    def peek(self): return self.tokens[self.i]

def parse_programa(ts):
    decls = []
    #enquanto o próximo token for um nome de variável, é uma declaração
    while ts.peek().kind == "IDENT":
        decls.append(parse_decl(ts))
    
    #a expressão final obrigatoriamente começa com '='
    if ts.next().kind != "ASSIGN":
        raise SyntaxError("Esperado '=' para a expressão final")
    
    final_exp = parse_exp(ts)
    return Programa(decls, final_exp)

def parse_decl(ts):
    nome = ts.next().lexeme #identificador
    if ts.next().kind != "ASSIGN": raise SyntaxError("Esperado '=' na atribuição")
    exp = parse_exp(ts)
    if ts.next().kind != "SEMI": raise SyntaxError("Esperado ';' após declaração")
    return Declaracao(nome, exp)

#reutiliza lógica de precedência da EC2
def parse_exp(ts):
    node = parse_exp_m(ts)
    while ts.peek().kind in ("SUM", "SUB"):
        op = "+" if ts.next().kind == "SUM" else "-"
        node = OpBin(node, op, parse_exp_m(ts))
    return node

def parse_exp_m(ts):
    node = parse_prim(ts)
    while ts.peek().kind in ("MUL", "DIV"):
        op = "*" if ts.next().kind == "MUL" else "/"
        node = OpBin(node, op, parse_prim(ts))
    return node

def parse_prim(ts):
    tok = ts.next()
    if tok.kind == "LITERAL": return Const(int(tok.lexeme))
    if tok.kind == "IDENT": return Var(tok.lexeme) #variável como primário
    if tok.kind == "OPEN_P":
        node = parse_exp(ts)
        if ts.next().kind != "CLOSE_P": raise SyntaxError("Esperado ')'")
        return node
    raise SyntaxError(f"Token inesperado: {tok.lexeme}")