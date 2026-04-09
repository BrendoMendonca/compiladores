from ev_ast import *

class TokenStream:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def consume(self, expected_type=None):
        token = self.peek()
        if expected_type and (not token or token.type != expected_type):
            raise SyntaxError(f"Esperado {expected_type}, encontrado {token}")
        self.pos += 1
        return token

def parse_programa(ts):
    # <programa> ::= <decl>* 'main' '{' <cmd>* 'return' <exp>';' '}'
    declaracoes = []
    
    #reconhece variáveis globais e funções antes do 'main'
    while ts.peek() and ts.peek().type in ('VAR', 'FUN'):
        if ts.peek().type == 'VAR':
            declaracoes.append(parse_vardecl(ts))
        else:
            declaracoes.append(parse_fundecl(ts))
    
    ts.consume('MAIN') #palavra-chave obrigatória na Atividade 11
    ts.consume('LBRACE')
    
    comandos = []
    while ts.peek() and ts.peek().type != 'RETURN':
        comandos.append(parse_comando(ts))
    
    ts.consume('RETURN')
    exp_retorno = parse_exp(ts)
    ts.consume('SEMI')
    ts.consume('RBRACE')
    
    return ProgramaNode(declaracoes, comandos, exp_retorno)

def parse_fundecl(ts):
    # <fundecl> ::= 'fun' <ident> '(' <arglist>? ')' '{' <vardecl>* <cmd>* 'return' <exp> ';' '}'
    ts.consume('FUN')
    nome_func = ts.consume('ID').value
    ts.consume('LPAREN')
    
    #lista de parâmetros formais (x, y, z) 
    parametros = []
    if ts.peek() and ts.peek().type == 'ID':
        parametros.append(ts.consume('ID').value)
        while ts.peek() and ts.peek().type == 'COMMA':
            ts.consume('COMMA')
            parametros.append(ts.consume('ID').value)
    
    ts.consume('RPAREN')
    ts.consume('LBRACE')
    
    #variáveis locais da função
    locais = []
    while ts.peek() and ts.peek().type == 'VAR':
        locais.append(parse_vardecl(ts))
        
    comandos = []
    while ts.peek() and ts.peek().type != 'RETURN':
        comandos.append(parse_comando(ts))
        
    ts.consume('RETURN')
    retorno_func = parse_exp(ts)
    ts.consume('SEMI')
    ts.consume('RBRACE')
    
    return FunDeclNode(nome_func, parametros, locais, comandos, retorno_func)

def parse_vardecl(ts):
    ts.consume('VAR')
    var_token = ts.consume('ID')
    
    # Se tiver um '[', é declaração de Array!
    if ts.peek() and ts.peek().type == 'LBRACKET':
        ts.consume('LBRACKET')
        tamanho = ts.consume('NUM').value
        ts.consume('RBRACKET')
        ts.consume('SEMI')
        return ArrayDeclNode(var_token.value, tamanho)
        
    ts.consume('ASSIGN')
    expressao = parse_exp(ts)
    ts.consume('SEMI')
    return DeclaracaoNode(var_token.value, expressao)

def parse_comando(ts):
    token = ts.peek()
    if token.type == 'IF':
        return parse_if(ts)
    elif token.type == 'WHILE':
        return parse_while(ts)
    elif token.type == 'VAR': 
        return parse_vardecl(ts)
    elif token.type == 'ID':
        return parse_atrib(ts)
    else:
        raise SyntaxError(f"Comando inválido: {token.value}")

def parse_if(ts):
    ts.consume('IF')
    condicao = parse_exp(ts)
    ts.consume('LBRACE')
    corpo_if = []
    while ts.peek().type != 'RBRACE':
        corpo_if.append(parse_comando(ts))
    ts.consume('RBRACE')
    ts.consume('ELSE')
    ts.consume('LBRACE')
    corpo_else = []
    while ts.peek().type != 'RBRACE':
        corpo_else.append(parse_comando(ts))
    ts.consume('RBRACE')
    return IfNode(condicao, corpo_if, corpo_else)

def parse_while(ts):
    ts.consume('WHILE')
    condicao = parse_exp(ts)
    ts.consume('LBRACE')
    corpo = []
    while ts.peek().type != 'RBRACE':
        corpo.append(parse_comando(ts))
    ts.consume('RBRACE')
    return WhileNode(condicao, corpo)

def parse_atrib(ts):
    var_token = ts.consume('ID')
    
    # Se tiver um '[', é atribuição em uma posição do Array!
    if ts.peek() and ts.peek().type == 'LBRACKET':
        ts.consume('LBRACKET')
        index_exp = parse_exp(ts)
        ts.consume('RBRACKET')
        ts.consume('ASSIGN')
        expressao = parse_exp(ts)
        ts.consume('SEMI')
        return ArrayAssignNode(var_token.value, index_exp, expressao)
        
    # Atribuição normal (já suporta compostos do passo anterior)
    if ts.peek() and ts.peek().type in ('ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'MUL_ASSIGN', 'DIV_ASSIGN'):
        op_token = ts.consume()
        expressao = parse_exp(ts)
        ts.consume('SEMI')
        if op_token.type == 'ASSIGN':
            return AssignNode(var_token.value, expressao)
        else:
            base_op = op_token.value[0]
            return CompoundAssignNode(var_token.value, base_op, expressao)
    else:
        raise SyntaxError(f"Esperado '=' após a variável {var_token.value}")

#hierarquia de Expressões


def parse_exp(ts):
    # OR tem a menor precedência
    node = parse_and_exp(ts)
    while ts.peek() and ts.peek().type == 'OR':
        ts.consume('OR')
        right = parse_and_exp(ts)
        node = LogicoNode(node, 'or', right)
    return node

def parse_and_exp(ts):
    # AND vem antes do OR
    node = parse_comparacao(ts)
    while ts.peek() and ts.peek().type == 'AND':
        ts.consume('AND')
        right = parse_comparacao(ts)
        node = LogicoNode(node, 'and', right)
    return node

def parse_comparacao(ts):
    # COMPARAÇÃO (incluindo os novos operadores <=, >=, !=)
    node = parse_exp_aritmetica(ts)
    while ts.peek() and ts.peek().type in ('LT', 'GT', 'EQ', 'LE', 'GE', 'NEQ'):
        op = ts.consume().value
        right = parse_exp_aritmetica(ts)
        node = ComparacaoNode(node, op, right)
    return node

def parse_exp_aritmetica(ts):
    node = parse_term(ts)
    while ts.peek() and ts.peek().type in ('PLUS', 'MINUS'):
        op = ts.consume().value
        right = parse_term(ts)
        node = BinOpNode(node, op, right)
    return node

def parse_term(ts):
    # Aqui chamamos parse_unary em vez de parse_factor
    node = parse_unary(ts)
    while ts.peek() and ts.peek().type in ('MUL', 'DIV'):
        op = ts.consume().value
        right = parse_unary(ts)
        node = BinOpNode(node, op, right)
    return node

def parse_unary(ts):
    # Trata o operador 'not'
    if ts.peek() and ts.peek().type == 'NOT':
        ts.consume('NOT')
        return NotNode(parse_unary(ts)) # Recursivo para permitir "not not x"
    return parse_factor(ts)

def parse_factor(ts):
    token = ts.consume()
    if token.type == 'NUM':
        return NumNode(token.value)
    elif token.type == 'ID':
        # Se tiver '[', é leitura de uma posição do Array!
        if ts.peek() and ts.peek().type == 'LBRACKET':
            ts.consume('LBRACKET')
            index_exp = parse_exp(ts)
            ts.consume('RBRACKET')
            return ArrayAccessNode(token.value, index_exp)
            
        if ts.peek() and ts.peek().type == 'LPAREN':
            # ... mantém o código original da chamada de função (FunCallNode) ...
            ts.consume('LPAREN')
            args = []
            if ts.peek() and ts.peek().type != 'RPAREN':
                args.append(parse_exp(ts))
                while ts.peek() and ts.peek().type == 'COMMA':
                    ts.consume('COMMA')
                    args.append(parse_exp(ts))
            ts.consume('RPAREN')
            return FunCallNode(token.value, args)
        return IDNode(token.value)
    elif token.type == 'LPAREN':
        node = parse_exp(ts)
        ts.consume('RPAREN')
        return node
    raise SyntaxError(f"Fator inesperado: {token}")