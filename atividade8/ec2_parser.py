from ec1_ast import Const, OpBin

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def next(self):
        if self.i < len(self.tokens):
            t = self.tokens[self.i]; self.i += 1; return t
        return self.tokens[-1]

    def peek(self):
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return self.tokens[-1]

#nível 1: soma e subtração (menor precedência)
def exp_a(ts):
    node = exp_m(ts)
    while ts.peek().kind in ("SUM", "SUB"):
        op_tok = ts.next()
        op = "+" if op_tok.kind == "SUM" else "-"
        right = exp_m(ts)
        node = OpBin(node, op, right)
    return node

#nível 2: multiplicação e divisão
def exp_m(ts):
    node = prim(ts)
    while ts.peek().kind in ("MUL", "DIV"):
        op_tok = ts.next()
        op = "*" if op_tok.kind == "MUL" else "/"
        right = prim(ts)
        node = OpBin(node, op, right)
    return node

#nível 3: literais e parênteses (maior precedência)
def prim(ts):
    tok = ts.next()
    if tok.kind == "LITERAL":
        return Const(int(tok.lexeme))
    if tok.kind == "OPEN_P":
        node = exp_a(ts) # Volta para o topo da gramática
        if ts.next().kind != "CLOSE_P":
            raise SyntaxError(f"Esperado ')' em {tok.position}")
        return node
    raise SyntaxError(f"Token inesperado: {tok.lexeme}")