class Exp:
    """Classe base para todas as expressões."""
    pass

class Const(Exp):
    """Representa um literal inteiro."""
    def __init__(self, valor):
        self.valor = valor

class OpBin(Exp):
    """Representa uma operação binária (+, -, *, /)."""
    def __init__(self, operador, opEsq, opDir):
        self.operador = operador
        self.opEsq = opEsq
        self.opDir = opDir