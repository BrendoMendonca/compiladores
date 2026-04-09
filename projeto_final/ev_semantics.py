class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.global_symbols = {}
        self.local_symbols = None
        self.current_fun_name = None

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        for attr in ['declaracoes', 'comandos', 'corpo', 'corpo_if', 'corpo_else', 'left', 'right', 'exp', 'condicao', 'expressao_retorno', 'retorno', 'argumentos']:
            child = getattr(node, attr, None)
            if child:
                if isinstance(child, list):
                    for c in child: self.visit(c)
                else:
                    self.visit(child)

    def visit_ProgramaNode(self, node):
        for decl in node.declaracoes:
            if hasattr(decl, 'nome') and hasattr(decl, 'parametros'):
                self.global_symbols[decl.nome] = ('fun', len(decl.parametros))
            elif hasattr(decl, 'tamanho'):
                self.global_symbols[decl.nome] = ('array', decl.tamanho) # Registra Array global
            elif hasattr(decl, 'nome'):
                self.global_symbols[decl.nome] = 'var'

        for decl in node.declaracoes:
            self.visit(decl)
        for cmd in node.comandos:
            self.visit(cmd)
        self.visit(node.expressao_retorno)

    def visit_FunDeclNode(self, node):
        self.current_fun_name = node.nome
        self.local_symbols = {}
        
        total_bytes = 0
        
        # O offset avança pelo tamanho da variável. Variável = 8 bytes. Array = Tamanho * 8 bytes.
        for local in node.locais:
            offset = total_bytes
            self.local_symbols[local.nome] = offset
            local.offset = offset
            
            if hasattr(local, 'tamanho'): # É um array!
                total_bytes += local.tamanho * 8
            else: # Variável normal
                total_bytes += 8
                self.visit(local.exp)
                
        node.total_local_bytes = total_bytes

        # Parâmetros ficam acima das variáveis locais na pilha
        for i, p_nome in enumerate(node.parametros):
            offset = total_bytes + 16 + (i * 8) 
            self.local_symbols[p_nome] = offset

        for cmd in node.comandos:
            self.visit(cmd)
        self.visit(node.retorno)
        
        self.local_symbols = None
        self.current_fun_name = None
        
    def visit_FunCallNode(self, node):
        if node.nome not in self.global_symbols or self.global_symbols[node.nome][0] != 'fun':
            raise SemanticError(f"Erro: Função '{node.nome}' não declarada.")
        
        esperado = self.global_symbols[node.nome][1]
        encontrado = len(node.argumentos)
        if esperado != encontrado:
            raise SemanticError(f"Erro: Função '{node.nome}' espera {esperado} argumentos, mas recebeu {encontrado}.")
        
        for arg in node.argumentos:
            self.visit(arg)

    def visit_IDNode(self, node):
        if self.local_symbols is not None and node.nome in self.local_symbols:
            node.offset = self.local_symbols[node.nome]
        elif node.nome in self.global_symbols:
            if self.global_symbols[node.nome] != 'var':
                raise SemanticError(f"Erro: '{node.nome}' é uma função e não pode ser usada como variável.")
            node.offset = None
        else:
            raise SemanticError(f"Erro: Variável '{node.nome}' não declarada.")

    def visit_AssignNode(self, node):
        self.visit(node.exp)
        if self.local_symbols is not None and node.nome in self.local_symbols:
            node.offset = self.local_symbols[node.nome]
        elif node.nome in self.global_symbols:
            if self.global_symbols[node.nome] != 'var':
                raise SemanticError(f"Erro: Tentativa de atribuir valor à função '{node.nome}'.")
            node.offset = None
        else:
            raise SemanticError(f"Erro: Tentativa de atribuir a '{node.nome}' não declarada.")

    def visit_ArrayDeclNode(self, node):
        # Apenas para o analisador não quebrar ao visitar a declaração
        pass

    def visit_ArrayAssignNode(self, node):
        self.visit(node.index_exp)
        self.visit(node.exp)
        # Verifica se o array é local ou global
        if self.local_symbols is not None and node.nome in self.local_symbols:
            node.offset = self.local_symbols[node.nome]
        elif node.nome in self.global_symbols:
            if isinstance(self.global_symbols[node.nome], tuple) and self.global_symbols[node.nome][0] == 'array':
                node.offset = None # None indica que é global
            else:
                raise SemanticError(f"Erro: '{node.nome}' não é um array.")
        else:
            raise SemanticError(f"Erro: Array '{node.nome}' não declarado.")

    def visit_ArrayAccessNode(self, node):
        self.visit(node.index_exp)
        if self.local_symbols is not None and node.nome in self.local_symbols:
            node.offset = self.local_symbols[node.nome]
        elif node.nome in self.global_symbols:
            if isinstance(self.global_symbols[node.nome], tuple) and self.global_symbols[node.nome][0] == 'array':
                node.offset = None
            else:
                raise SemanticError(f"Erro: '{node.nome}' não é um array.")
        else:
            raise SemanticError(f"Erro: Array '{node.nome}' não declarado.")
        
    def visit_CompoundAssignNode(self, node):
            self.visit(node.exp)
            # Mesma lógica do AssignNode: define se a variável é local ou global
            if self.local_symbols is not None and node.nome in self.local_symbols:
                node.offset = self.local_symbols[node.nome]
            elif node.nome in self.global_symbols:
                if self.global_symbols[node.nome] != 'var':
                    raise SemanticError(f"Erro: Tentativa de atribuir valor à função '{node.nome}'.")
                node.offset = None
            else:
                raise SemanticError(f"Erro: Tentativa de atribuir a '{node.nome}' não declarada.")