class SemanticError(Exception):
    pass

class SemanticAnalyzer:
    def __init__(self):
        self.symbol_table = set()

    def visit(self, node):
        method_name = f'visit_{type(node).__name__}'
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        # Para nós com múltiplos comandos (Programa, If, While)
        if hasattr(node, 'declaracoes'):
            for d in node.declaracoes: self.visit(d)
        if hasattr(node, 'comandos'):
            for c in node.comandos: self.visit(c)
        if hasattr(node, 'expressao_retorno'):
            self.visit(node.expressao_retorno)
        
        # Para nós binários ou com expressões únicas
        for attr in ['left', 'right', 'exp', 'condicao']:
            child = getattr(node, attr, None)
            if child:
                if isinstance(child, list):
                    for c in child: self.visit(c)
                else:
                    self.visit(child)

    def visit_DeclaracaoNode(self, node):
        # 1. Analisa a expressão inicial
        self.visit(node.exp)
        # 2. Adiciona a variável à tabela (único lugar onde isso ocorre) [cite: 130]
        self.symbol_table.add(node.nome)

    def visit_AssignNode(self, node):
        # 1. Verifica o valor (lado direito) [cite: 127]
        self.visit(node.exp)
        # 2. Verifica se a variável de destino existe (lado esquerdo) [cite: 128, 129]
        if node.nome not in self.symbol_table:
            raise SemanticError(f"Erro: Tentativa de atribuir valor à variável '{node.nome}' não declarada.")

    def visit_IDNode(self, node):
        if node.nome not in self.symbol_table:
            raise SemanticError(f"Erro: Variável '{node.nome}' usada antes de ser declarada.")
            
    # O if e while usam o generic_visit para checar as expressões e blocos internos