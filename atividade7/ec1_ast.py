# ec1_ast.py - Árvore de Sintaxe Abstrata para EC1

class Exp: pass

class Const(Exp):
    def __init__(self, v: int):
        self.v = v
    
    def gen(self, out_lines):
        # Gera instrução mov para a constante
        if -2**31 <= self.v <= 2**31 - 1:
            out_lines.append(f"    mov ${self.v}, %rax")
        else:
            out_lines.append(f"    movabs ${self.v}, %rax")

class OpBin(Exp):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def gen(self, out_lines):
        # Modelo de tradução usando a pilha para EC1
        self.right.gen(out_lines)     # Gera operando direito primeiro
        out_lines.append("    push %rax") # Salva resultado na pilha
        self.left.gen(out_lines)      # Gera operando esquerdo
        out_lines.append("    pop %rbx")  # Recupera o direito em RBX
        
        if self.op == '+': out_lines.append("    add %rbx, %rax")
        elif self.op == '-': out_lines.append("    sub %rbx, %rax")
        elif self.op == '*': out_lines.append("    imul %rbx")
        elif self.op == '/':
            out_lines.append("    cqo") # Extensão de sinal para divisão
            out_lines.append("    idiv %rbx")