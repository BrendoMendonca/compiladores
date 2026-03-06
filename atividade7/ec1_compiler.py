import sys
import os

from ec1_lexer import lexer
from ec1_parser import TokenStream, parse_expression
from ec1_ast import Const, OpBin

#funções Utilitárias de Otimização e Cálculo

def trunc_div(a: int, b: int) -> int:
    if b == 0:
        raise ZeroDivisionError("Divisão por zero em tempo de compilação/execução")
    q = abs(a) // abs(b)
    return q if a * b >= 0 else -q

def constant_fold(node):
    """Realiza a propagação de constantes"""
    if isinstance(node, Const):
        return node

    if isinstance(node, OpBin):
        L = constant_fold(node.left)
        R = constant_fold(node.right)

        if isinstance(L, Const) and isinstance(R, Const):
            a, b = L.v, R.v
            if node.op == '+': return Const(a + b)
            if node.op == '-': return Const(a - b)
            if node.op == '*': return Const(a * b)
            if node.op == '/': return Const(trunc_div(a, b))

        return OpBin(L, node.op, R)
    return node

def eval_ast(node):
    """Avalia o resultado matemático da AST para conferência"""
    if isinstance(node, Const):
        return node.v
    if isinstance(node, OpBin):
        a = eval_ast(node.left)
        b = eval_ast(node.right)
        if node.op == '+': return a + b
        if node.op == '-': return a - b
        if node.op == '*': return a * b
        if node.op == '/': return trunc_div(a, b)
    raise RuntimeError("AST inválida")

#coordenação da Compilação

#marcador exato do seu arquivo modelo.s 
MODEL_MARKER = '## saida do compilador deve ser inserida aqui'

def compile_expr_to_file(expr_str: str, out_path: str, modelo_path: str = "modelo.s", do_fold: bool = True):
    #fluxo: Lexer -> Parser
    toks = lexer(expr_str)
    ts = TokenStream(toks)
    ast = parse_expression(ts)

    #verifica se sobraram tokens
    if ts.peek().kind != "EOF":
        raise SyntaxError("Tokens extras após a expressão")

    if do_fold:
        ast = constant_fold(ast)

    #geração de código Assembly
    code_lines = []
    ast.gen(code_lines)
    code_text = "\n".join(code_lines)

    #integração com o modelo.s
    if not os.path.exists(modelo_path):
        raise FileNotFoundError(f"modelo.s não encontrado")

    with open(modelo_path, "r") as f:
        model = f.read()

    if MODEL_MARKER not in model:
        raise RuntimeError("Marcador não encontrado no modelo.s")
    
    out_text = model.replace(MODEL_MARKER, code_text)

    with open(out_path, "w") as f:
        f.write(out_text)

    return ast, out_text

#ponto de Entrada

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python3 ec1_compiler.py '<expressao>' out.s")
        sys.exit(1)

    expr = sys.argv[1]
    out_file = sys.argv[2]

    try:
        ast, text = compile_expr_to_file(expr, out_file, do_fold=True)
        print(f"AST Gerada: {ast}")
        print(f"Sucesso! Arquivo '{out_file}' gerado.")
    except Exception as e:
        print(f"Erro: {e}")
        sys.exit(1)