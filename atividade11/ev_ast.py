#contador global para gerar rótulos únicos em Assembly
label_count = 0

def get_new_label(prefix):
    global label_count
    label = f"{prefix}{label_count}"
    label_count += 1
    return label

class Nodo:
    def gen(self, code):
        pass

class NumNode(Nodo):
    def __init__(self, value):
        self.value = value

    def gen(self, code):
        code.append(f"    mov ${self.value}, %rax")

class IDNode(Nodo):
    def __init__(self, nome, offset=None):
        self.nome = nome
        self.offset = offset

    def gen(self, code):
        if self.offset is None:
            code.append(f"    mov {self.nome}, %rax")
        else:
            code.append(f"    mov {self.offset}(%rbp), %rax")

class ProgramaNode(Nodo):
    def __init__(self, declaracoes, comandos, expressao_retorno):
        self.declaracoes = declaracoes
        self.comandos = comandos
        self.expressao_retorno = expressao_retorno

    def gen(self, code):
        funcoes = [d for d in self.declaracoes if isinstance(d, FunDeclNode)]
        globais = [d for d in self.declaracoes if not isinstance(d, FunDeclNode)]

        for f in funcoes:
            f.gen(code)

        code.append("\n_start:")
        for g in globais:
            g.gen(code)
        for cmd in self.comandos:
            cmd.gen(code)
            
        self.expressao_retorno.gen(code)

class FunDeclNode(Nodo):
    def __init__(self, nome, parametros, locais, comandos, retorno):
        self.nome = nome
        self.parametros = parametros
        self.locais = locais
        self.comandos = comandos
        self.retorno = retorno

    def gen(self, code):
        code.append(f"\n{self.nome}:")
        
        # 1. Salva RBP antigo
        code.append("    push %rbp")
        
        # 2. Aloca espaço (SUB) antes de configurar o RBP (Regra do Guia)
        num_locais = len(self.locais)
        if num_locais > 0:
            code.append(f"    sub ${num_locais * 8}, %rsp")
            
        # 3. RBP agora aponta para o início das variáveis locais
        code.append("    mov %rsp, %rbp")
        
        for local in self.locais:
            local.gen(code)
        for cmd in self.comandos:
            cmd.gen(code)
            
        self.retorno.gen(code)
        
        # Epílogo: Restaura a pilha (RSP volta ao que era antes do sub)
        if num_locais > 0:
            code.append(f"    add ${num_locais * 8}, %rsp")
        code.append("    pop %rbp")
        code.append("    ret")

class FunCallNode(Nodo):
    def __init__(self, nome, argumentos):
        self.nome = nome
        self.argumentos = argumentos

    def gen(self, code):
        for arg in reversed(self.argumentos):
            arg.gen(code)
            code.append("    push %rax")
            
        code.append(f"    call {self.nome}")
        
        num_args = len(self.argumentos)
        if num_args > 0:
            code.append(f"    add ${num_args * 8}, %rsp")

class IfNode(Nodo):
    def __init__(self, condicao, corpo_if, corpo_else):
        self.condicao = condicao
        self.corpo_if = corpo_if
        self.corpo_else = corpo_else

    def gen(self, code):
        l_falso = get_new_label("Lfalso")
        l_fim = get_new_label("Lfim")
        self.condicao.gen(code)
        code.append("    cmp $0, %rax")
        code.append(f"    jz {l_falso}")
        for cmd in self.corpo_if:
            cmd.gen(code)
        code.append(f"    jmp {l_fim}")
        code.append(f"{l_falso}:")
        for cmd in self.corpo_else:
            cmd.gen(code)
        code.append(f"{l_fim}:")

class WhileNode(Nodo):
    def __init__(self, condicao, corpo):
        self.condicao = condicao
        self.corpo = corpo

    def gen(self, code):
        l_inic = get_new_label("Linicio")
        l_fim = get_new_label("Lfim")
        code.append(f"{l_inic}:")
        self.condicao.gen(code)
        code.append("    cmp $0, %rax")
        code.append(f"    jz {l_fim}")
        for cmd in self.corpo:
            cmd.gen(code)
        code.append(f"    jmp {l_inic}")
        code.append(f"{l_fim}:")

class AssignNode(Nodo):
    def __init__(self, nome, exp, offset=None):
        self.nome = nome
        self.exp = exp
        self.offset = offset

    def gen(self, code):
        self.exp.gen(code)
        if self.offset is None:
            code.append(f"    mov %rax, {self.nome}")
        else:
            code.append(f"    mov %rax, {self.offset}(%rbp)")

class DeclaracaoNode(Nodo):
    def __init__(self, nome, exp, offset=None):
        self.nome = nome
        self.exp = exp
        self.offset = offset

    def gen(self, code):
        self.exp.gen(code)
        if self.offset is None:
            code.append(f"    mov %rax, {self.nome}")
        else:
            code.append(f"    mov %rax, {self.offset}(%rbp)")

class ComparacaoNode(Nodo):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def gen(self, code):
        self.right.gen(code)
        code.append("    push %rax")
        self.left.gen(code)
        code.append("    pop %rbx")
        code.append("    xor %rcx, %rcx")
        code.append("    cmp %rbx, %rax")
        if self.op == '==': code.append("    setz %cl")
        elif self.op == '<': code.append("    setl %cl")
        elif self.op == '>': code.append("    setg %cl")
        code.append("    mov %rcx, %rax")

class BinOpNode(Nodo):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def gen(self, code):
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