# ec1_parser.py - Parser para a linguagem EC1
from ec1_ast import Const, OpBin

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def next(self):
        """Retorna o próximo token e avança o ponteiro."""
        if self.i < len(self.tokens):
            t = self.tokens[self.i]
            self.i += 1
            return t
        # Retorna o último token (geralmente EOF) se chegar ao fim
        return self.tokens[-1]

    def peek(self):
        """Apenas olha o próximo token sem avançar o ponteiro."""
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return self.tokens[-1]

def parse_expression(ts):
    tok = ts.next()
    if tok is None: return None

    # Regra: <expressao> ::= <literal-inteiro>
    if tok.kind == "LITERAL":
        return Const(int(tok.lexeme))

    # Regra: <expressao> ::= '(' <exp> <op> <exp> ')'
    if tok.kind == "OPEN_P":
        esq = parse_expression(ts)
        
        tok_op = ts.next()
        op_map = {"SUM": "+", "SUB": "-", "MUL": "*", "DIV": "/"}
        op = op_map[tok_op.kind]
        
        dir = parse_expression(ts)
        
        tok_close = ts.next()
        if tok_close.kind != "CLOSE_P":
            raise SyntaxError(f"Esperado ')' em {tok_close.position}")
            
        return OpBin(esq, op, dir)