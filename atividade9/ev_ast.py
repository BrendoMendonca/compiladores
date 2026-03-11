class Programa:
    def __init__(self, declaracoes, exp_final):
        self.declaracoes = declaracoes
        self.exp_final = exp_final

    def gen(self, code):
        # 1. Gera código para cada declaração (atribuições)
        for decl in self.declaracoes:
            decl.gen(code)
        
        # 2. Gera código para a expressão final de resultado
        self.exp_final.gen(code)

class Declaracao:
    def __init__(self, nome, exp):
        self.nome = nome
        self.exp = exp

    def gen(self, code):
        code.append(f"    # Atribuição: {self.nome}")
        self.exp.gen(code) # O resultado da expressão termina em RAX
        code.append(f"    mov %rax, {self.nome}") # Move RAX para a memória da variável

class Var:
    def __init__(self, nome):
        self.nome = nome

    def gen(self, code):
        # Carrega o valor da variável da memória para o registrador RAX
        code.append(f"    mov {self.nome}, %rax")

class Const:
    def __init__(self, v):
        self.v = v

    def gen(self, code):
        if self.v > 0x7FFFFFFF:
            code.append(f"    movabs ${self.v}, %rax")
        else:
            code.append(f"    mov ${self.v}, %rax")

class OpBin:
    def __init__(self, left, op, right):
        self.left, self.op, self.right = left, op, right

    def gen(self, code):
        # Lógica de pilha para operações binárias
        self.right.gen(code)
        code.append("    push %rax")
        self.left.gen(code)
        code.append("    pop %rbx")
        
        if self.op == '+': code.append("    add %rbx, %rax")
        elif self.op == '-': code.append("    sub %rbx, %rax")
        elif self.op == '*': code.append("    imul %rbx, %rax")
        elif self.op == '/':
            code.append("    cqo")
            code.append("    idiv %rbx")