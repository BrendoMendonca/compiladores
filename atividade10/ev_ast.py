# Contador global para gerar rótulos únicos em Assembly
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
    def __init__(self, nome):
        self.nome = nome

    def gen(self, code):
        code.append(f"    mov {self.nome}, %rax")

class ProgramaNode(Nodo):
    def __init__(self, declaracoes, comandos, expressao_retorno):
        self.declaracoes = declaracoes
        self.comandos = comandos
        self.expressao_retorno = expressao_retorno

    def gen(self, code):
        # 1. Gera código para as declarações (ESSENCIAL para o x = 42 funcionar)
        for decl in self.declaracoes:
            decl.gen(code)
            
        # 2. Gera código para os comandos (if, while, etc)
        for cmd in self.comandos:
            cmd.gen(code)
            
        # 3. Gera o código para carregar o valor do return em RAX
        self.expressao_retorno.gen(code)

class IfNode(Nodo):
    def __init__(self, condicao, corpo_if, corpo_else):
        self.condicao = condicao
        self.corpo_if = corpo_if
        self.corpo_else = corpo_else

    def gen(self, code):
        l_falso = get_new_label("Lfalso")
        l_fim = get_new_label("Lfim")

        self.condicao.gen(code)      # Resultado da condição em RAX
        code.append("    cmp $0, %rax")
        code.append(f"    jz {l_falso}") # Salta se falso (0)
        
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
        l_inicio = get_new_label("Linicio")
        l_fim = get_new_label("Lfim")

        code.append(f"{l_inicio}:")
        self.condicao.gen(code)      # Avalia condição
        code.append("    cmp $0, %rax")
        code.append(f"    jz {l_fim}")   # Sai do loop se falso
        
        for cmd in self.corpo:
            cmd.gen(code)
            
        code.append(f"    jmp {l_inicio}")
        code.append(f"{l_fim}:")

class AssignNode(Nodo):
    def __init__(self, nome, exp):
        self.nome = nome
        self.exp = exp

    def gen(self, code):
        self.exp.gen(code)           # Valor vai para RAX
        code.append(f"    mov %rax, {self.nome}") # Atualiza variável na BSS

class DeclaracaoNode(Nodo):
    def __init__(self, nome, exp):
        self.nome = nome
        self.exp = exp

    def gen(self, code):
        self.exp.gen(code) # Coloca o valor (ex: 42) em RAX
        code.append(f"    mov %rax, {self.nome}") # Salva na memória

class ComparacaoNode(Nodo):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op # '<', '>', '=='
        self.right = right

    def gen(self, code):
        self.right.gen(code)
        code.append("    push %rax")
        self.left.gen(code)
        code.append("    pop %rbx")
        code.append("    xor %rcx, %rcx")
        code.append("    cmp %rbx, %rax") # Compara RAX (esq) com RBX (dir)
        
        if self.op == '==':
            code.append("    setz %cl")   # Set if Zero
        elif self.op == '<':
            code.append("    setl %cl")   # Set if Less
        elif self.op == '>':
            code.append("    setg %cl")   # Set if Greater
            
        code.append("    mov %rcx, %rax") # Resultado (0 ou 1) em RAX

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
        if self.op == '+':
            code.append("    add %rbx, %rax")
        elif self.op == '-':
            code.append("    sub %rbx, %rax")
        elif self.op == '*':
            code.append("    imul %rbx, %rax")
        elif self.op == '/':
            code.append("    cqo")
            code.append("    idiv %rbx")

if __name__ == "__main__":
    # Simulando o programa:
    # x = 10;
    # {
    #    if x < 20 { x = 1; } else { x = 0; }
    #    return x;
    # }

    # 1. Criar os nós das expressões e comandos
    condicao = ComparacaoNode(IDNode("x"), '<', NumNode("20"))
    cmd_if = [AssignNode("x", NumNode("1"))]
    cmd_else = [AssignNode("x", NumNode("0"))]
    
    meu_if = IfNode(condicao, cmd_if, cmd_else)
    retorno = IDNode("x")

    # 2. Criar o nó raiz do Programa
    # (Passamos uma lista vazia para declarações apenas para este teste de geração)
    ast_manual = ProgramaNode([], [meu_if], retorno)

    # 3. Gerar o código Assembly
    codigo_gerado = []
    ast_manual.gen(codigo_gerado)

    # 4. Exibir o resultado
    print("--- Código Assembly Gerado Manualmente ---")
    for linha in codigo_gerado:
        print(linha)