import sys
import os
from ec2_lexer import lexer, Token, Position
from ec2_parser import TokenStream, exp_a as parse_expression

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.i = 0

    def next(self):
        if self.i < len(self.tokens):
            t = self.tokens[self.i]; self.i += 1; return t
        return Token(Position(), "", "EOF")

    def peek(self):
        if self.i < len(self.tokens):
            return self.tokens[self.i]
        return Token(Position(), "", "EOF")

class Exp:
    pass

class Const(Exp):
    def __init__(self, v: int):
        self.v = v

    def __repr__(self):
        return f"Const({self.v})"

class OpBin(Exp):
    def __init__(self, left: Exp, op: str, right: Exp):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return f"OpBin('{self.op}', {self.left}, {self.right})"





def parse_expression(ts: TokenStream):
    tok = ts.next()

    if tok.kind == "LITERAL":
        return Const(int(tok.lexeme))

    if tok.kind == "OPEN_P":
        left = parse_expression(ts)

        op_tok = ts.next()
        if op_tok.kind not in ("SUM", "SUB", "MUL", "DIV"):
            raise SyntaxError(f"Operador esperado na posição {op_tok.position}, encontrado '{op_tok.lexeme}'")

        op_map = {"SUM": "+", "SUB": "-", "MUL": "*", "DIV": "/"}
        op = op_map[op_tok.kind]

        right = parse_expression(ts)

        close = ts.next()
        if close.kind != "CLOSE_P":
            raise SyntaxError(f"')' esperado na posição {close.position}, encontrado '{close.lexeme}'")

        return OpBin(left, op, right)

    raise SyntaxError(f"Token inesperado no parse: {tok} (posição {tok.position})")

def trunc_div(a: int, b: int) -> int:
    if b == 0:
        raise ZeroDivisionError("Divisão por zero em tempo de compilação/execução")
    q = abs(a) // abs(b)
    return q if a * b >= 0 else -q

def constant_fold(node: Exp):
    if isinstance(node, Const):
        return node

    if isinstance(node, OpBin):
        L = constant_fold(node.left)
        R = constant_fold(node.right)

        if isinstance(L, Const) and isinstance(R, Const):
            a, b = L.v, R.v
            if node.op == '+':
                return Const(a + b)
            if node.op == '-':
                return Const(a - b)
            if node.op == '*':
                return Const(a * b)
            if node.op == '/':
                return Const(trunc_div(a, b))

        return OpBin(L, node.op, R)

    raise RuntimeError("AST inválida durante constant_fold")

def fits_32bit_signed(x: int):
    return -2**31 <= x <= 2**31 - 1

def emit_mov_immediate(reg: str, value: int):
    if fits_32bit_signed(value):
        return f"    mov ${value}, %{reg}"
    else:
        return f"    movabs ${value}, %{reg}"

def gen(node: Exp, out_lines):
    if isinstance(node, Const):
        out_lines.append(emit_mov_immediate("rax", node.v))
        return

    if isinstance(node, OpBin):
        gen(node.right, out_lines)
        out_lines.append("    push %rax")
        gen(node.left, out_lines)
        out_lines.append("    pop %rbx")
        if node.op == '+':
            out_lines.append("    add %rbx, %rax")
        elif node.op == '-':
            out_lines.append("    sub %rbx, %rax")
        elif node.op == '*':
            out_lines.append("    imul %rbx")
        elif node.op == '/':
            out_lines.append("    cqo")
            out_lines.append("    idiv %rbx")
        else:
            raise RuntimeError("Operador desconhecido no codegen")
        return

    raise RuntimeError("Nodo AST desconhecido no codegen")

def generate_code_lines(ast: Exp):
    lines = []
    gen(ast, lines)
    return lines

MODEL_MARKER = "## saida do compilador é inserida aqui"

def compile_expr_to_file(expr_str: str, out_path: str, modelo_path: str = "modelo.s", do_fold: bool = True):
    toks = lexer(expr_str)
    ts = TokenStream(toks)
    ast = exp_a(ts)

    if ts.peek().kind != "EOF":
        raise SyntaxError("Tokens extras após a expressão")

    if do_fold:
        ast = constant_fold(ast)

    code_lines = generate_code_lines(ast)
    code_text = "\n".join(code_lines)

    if not os.path.exists(modelo_path):
        raise FileNotFoundError(f"modelo.s não encontrado em: {modelo_path}")

    with open(modelo_path, "r") as f:
        model = f.read()

    if MODEL_MARKER not in model:
        if "call imprime_num" in model:
            model = model.replace("call imprime_num", code_text + "\n\n    call imprime_num")
            out_text = model
        else:
            raise RuntimeError("modelo.s inválido: marcador não encontrado e fallback falhou")
    else:
        out_text = model.replace(MODEL_MARKER, code_text)

    with open(out_path, "w") as f:
        f.write(out_text)

    return ast, out_text

def eval_ast(node: Exp):
    if isinstance(node, Const):
        return node.v
    if isinstance(node, OpBin):
        a = eval_ast(node.left)
        b = eval_ast(node.right)
        if node.op == '+': return a + b
        if node.op == '-': return a - b
        if node.op == '*': return a * b
        if node.op == '/': return trunc_div(a, b)
    raise RuntimeError("AST inválida para avaliação")

def exp_a(ts: TokenStream):
    #primeiro resolve o nível de maior precedência (multiplicativo)
    esq = exp_m(ts)
    
    #loop para tratar associatividade à esquerda
    while ts.peek().kind in ("SUM", "SUB"):
        tok_op = ts.next()
        op = "+" if tok_op.kind == "SUM" else "-"
        
        #analisa o próximo termo
        dir = exp_m(ts)
        
        #monta o nó da árvore mantendo o acumulado à esquerda
        esq = OpBin(esq, op, dir)
    
    return esq

def exp_m(ts: TokenStream):
    esq = prim(ts)
    
    while ts.peek().kind in ("MUL", "DIV"):
        tok_op = ts.next()
        op = "*" if tok_op.kind == "MUL" else "/"
        
        dir = prim(ts)
        esq = OpBin(esq, op, dir)
    
    return esq

def prim(ts: TokenStream):
    tok = ts.next()
    
    #se for um número, retorna o nó constante
    if tok.kind == "LITERAL":
        return Const(int(tok.lexeme))
    
    #se for um parêntese, reinicia a análise do topo (exp_a)
    if tok.kind == "OPEN_P":
        no = exp_a(ts)
        
        #garante que o parêntese foi fechado corretamente
        if ts.next().kind != "CLOSE_P":
            raise SyntaxError(f"Esperado ')' na posição {tok.position}")
        return no
        
    raise SyntaxError(f"Token inesperado: {tok.lexeme}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python ec1_compiler.py '<expressao>' out.s")
        sys.exit(1)

    expr = sys.argv[1]
    out_file = sys.argv[2]

    ast, text = compile_expr_to_file(expr, out_file, modelo_path="modelo.s", do_fold=True)
    print("AST final:", ast)
    print(f"Arquivo gerado: {out_file}")