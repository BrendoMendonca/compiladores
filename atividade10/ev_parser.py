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
    # <programa> ::= <decl>* '{' <cmd>* 'return' <exp> ';' '}'
    declaracoes = []
    # Enquanto o próximo não for '{', tratamos como declaração [cite: 117, 118]
    while ts.peek() and ts.peek().type != 'LBRACE':
        declaracoes.append(parse_decl(ts))
    
    ts.consume('LBRACE') # [cite: 62]
    
    comandos = []
    # Enquanto o próximo não for 'return', tratamos como comando [cite: 121]
    while ts.peek() and ts.peek().type != 'RETURN':
        comandos.append(parse_comando(ts))
    
    ts.consume('RETURN')
    exp_retorno = parse_exp(ts)
    ts.consume('SEMI')
    ts.consume('RBRACE')
    
    return ProgramaNode(declaracoes, comandos, exp_retorno)

def parse_decl(ts):
    # <decl> ::= <var> '=' <exp> ';' [cite: 64]
    var_token = ts.consume('ID')
    ts.consume('ASSIGN')
    expressao = parse_exp(ts)
    ts.consume('SEMI')
    return DeclaracaoNode(var_token.value, expressao)

def parse_comando(ts):
    # <cmd> ::= <if> | <while> | <atrib> [cite: 68]
    token = ts.peek()
    if token.type == 'IF':
        return parse_if(ts)
    elif token.type == 'WHILE':
        return parse_while(ts)
    elif token.type == 'ID':
        return parse_atrib(ts)
    else:
        raise SyntaxError(f"Comando inválido: {token.value}")

def parse_if(ts):
    # <if> ::= 'if' <exp> '{' <cmd>* '}' 'else' '{' <cmd>* '}' [cite: 70]
    ts.consume('IF')
    condicao = parse_exp(ts)
    
    ts.consume('LBRACE')
    corpo_if = []
    while ts.peek().type != 'RBRACE':
        corpo_if.append(parse_comando(ts))
    ts.consume('RBRACE')
    
    ts.consume('ELSE') # Na linguagem Cmd, o else é obrigatório [cite: 44]
    ts.consume('LBRACE')
    corpo_else = []
    while ts.peek().type != 'RBRACE':
        corpo_else.append(parse_comando(ts))
    ts.consume('RBRACE')
    
    return IfNode(condicao, corpo_if, corpo_else)

def parse_while(ts):
    # <while> ::= 'while' <exp> '{' <cmd>* '}' [cite: 72]
    ts.consume('WHILE')
    condicao = parse_exp(ts)
    ts.consume('LBRACE')
    corpo = []
    while ts.peek().type != 'RBRACE':
        corpo.append(parse_comando(ts))
    ts.consume('RBRACE')
    return WhileNode(condicao, corpo)

def parse_atrib(ts):
    # <atrib> ::= <var> '=' <exp> ';'
    var_token = ts.consume('ID')
    ts.consume('ASSIGN')
    expressao = parse_exp(ts)
    ts.consume('SEMI')
    return AssignNode(var_token.value, expressao)

# --- Hierarquia de Expressões com Comparação ---

def parse_exp(ts):
    # Nível mais baixo: Comparações (<, >, ==) [cite: 22, 122]
    node = parse_exp_aritmetica(ts)
    while ts.peek() and ts.peek().type in ('LT', 'GT', 'EQ'):
        op = ts.consume().value
        right = parse_exp_aritmetica(ts)
        node = ComparacaoNode(node, op, right)
    return node

def parse_exp_aritmetica(ts):
    # Soma e Subtração
    node = parse_term(ts)
    while ts.peek() and ts.peek().type in ('PLUS', 'MINUS'):
        op = ts.consume().value
        right = parse_term(ts)
        node = BinOpNode(node, op, right)
    return node

def parse_term(ts):
    # Multiplicação e Divisão
    node = parse_factor(ts)
    while ts.peek() and ts.peek().type in ('MUL', 'DIV'):
        op = ts.consume().value
        right = parse_factor(ts)
        node = BinOpNode(node, op, right)
    return node

def parse_factor(ts):
    token = ts.consume()
    if token.type == 'NUM':
        return NumNode(token.value)
    elif token.type == 'ID':
        return IDNode(token.value)
    elif token.type == 'LPAREN':
        node = parse_exp(ts)
        ts.consume('RPAREN')
        return node