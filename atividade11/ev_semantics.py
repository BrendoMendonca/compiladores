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
        
        num_locais = len(node.locais)
        
        # Mapear parâmetros: Como RBP está no fundo das variáveis locais, a fórmula é:
        # Offsets = (Qtd de Locais * 8) + 16(RBP antigo + Endereço Retorno) + (i * 8)
        for i, p_nome in enumerate(node.parametros):
            offset = (num_locais * 8) + 16 + (i * 8) 
            self.local_symbols[p_nome] = offset

        # Mapear variáveis locais (0(%rbp), 8(%rbp)...)
        for i, local in enumerate(node.locais):
            offset = i * 8
            self.local_symbols[local.nome] = offset
            local.offset = offset
            self.visit(local.exp)

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