from ev_ast import Programa, Declaracao, Var, OpBin, Const

class SemanticError(Exception):
    """Exceção para erros de variáveis não declaradas."""
    pass

class SemanticAnalyzer:
    def __init__(self):
        # Tabela de Símbolos: armazena nomes de variáveis declaradas
        self.symbol_table = set()

    def visit(self, node):
        """Método despachante para percorrer a AST recursivamente."""
        if isinstance(node, Programa):
            return self.visit_Programa(node)
        elif isinstance(node, Declaracao):
            return self.visit_Declaracao(node)
        elif isinstance(node, Var):
            return self.visit_Var(node)
        elif isinstance(node, OpBin):
            return self.visit_OpBin(node)
        elif isinstance(node, Const):
            return None # Constantes não precisam de verificação
        else:
            raise RuntimeError(f"Nó desconhecido: {type(node)}")

    def visit_Programa(self, node):
        # 1. Analisa cada declaração na ordem em que aparecem
        for decl in node.declaracoes:
            self.visit(decl)
        
        # 2. Analisa a expressão final de resultado 
        self.visit(node.exp_final)
        print("Análise Semântica concluída: Todas as variáveis foram declaradas corretamente.")

    def visit_Declaracao(self, node):
        # Primeiro verifica a expressão da direita antes de declarar a variável
        self.visit(node.exp)
        # Se a expressão for válida, adiciona o nome à tabela
        self.symbol_table.add(node.nome)

    def visit_OpBin(self, node):
        # Verifica recursivamente os dois lados da operação 
        self.visit(node.left)
        self.visit(node.right)

    def visit_Var(self, node):
        # O ponto crítico: verifica se o nome existe na tabela
        if node.nome not in self.symbol_table:
            raise SemanticError(f"Erro Semântico: Variável '{node.nome}' usada antes de ser declarada.")