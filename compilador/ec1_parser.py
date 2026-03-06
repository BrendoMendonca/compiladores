from ec1_lexer import Lexer, TipoToken
import sys

#definição da Árvore de Sintaxe Abstrata(AST)
class Exp: pass

class Const(Exp):
    def __init__(self, valor):
        self.valor = valor
    
    def exibir(self, nivel=0):
        print("  " * nivel + f"Const({self.valor})")

class OpBin(Exp):
    def __init__(self, operador, opEsq, opDir):
        self.operador = operador
        self.opEsq = opEsq
        self.opDir = opDir
    
    def exibir(self, nivel=0):
        print("  " * nivel + f"OpBin({self.operador})")
        self.opEsq.exibir(nivel + 1)
        self.opDir.exibir(nivel + 1)

#analisador sintático
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def proximo_token(self):
        if self.pos < len(self.tokens):
            tok = self.tokens[self.pos]
            self.pos += 1
            return tok
        return None

    def espiar(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def erro(self, mensagem):
        raise SyntaxError(f"Erro Sintático: {mensagem}")

    def analisaOperador(self):
        tok = self.proximo_token()

        if tok and tok.tipo in [TipoToken.SOMA, TipoToken.SUB, TipoToken.MULT, TipoToken.DIV]:
            return tok.lexema
        self.erro("Esperado um operador (+, -, *, /)")

    def analisaExp(self):
        tok_atual = self.espiar()
        if tok_atual is None:
            self.erro("Fim de entrada inesperado")

        # Ajustado para TipoToken.NUMERO de acordo com o Lexer
        if tok_atual.tipo == TipoToken.NUMERO:
            tok = self.proximo_token()
            return Const(int(tok.lexema))

        #justado para TipoToken.PAREN_ESQ de acordo com o Lexer
        elif tok_atual.tipo == TipoToken.PAREN_ESQ:
            self.proximo_token() # Consome '('
            esq = self.analisaExp()
            operador = self.analisaOperador()
            dir = self.analisaExp()
            
            tok_fecha = self.proximo_token()
            if not tok_fecha or tok_fecha.tipo != TipoToken.PAREN_DIR:
                self.erro("Esperado ')' para fechar a expressão")
            return OpBin(operador, esq, dir)
        else:
            self.erro(f"Token inesperado: {tok_atual.lexema}")

# interpretador-Tree-walking
def avaliar(no):
    if isinstance(no, Const):
        return no.valor
    if isinstance(no, OpBin):
        esq = avaliar(no.opEsq)
        dir = avaliar(no.opDir)
        if no.operador == '+': return esq + dir
        if no.operador == '-': return esq - dir
        if no.operador == '*': return esq * dir
        if no.operador == '/': return esq // dir
    return 0


#função principal de execução
def main():
    if len(sys.argv) < 2:
        print("Uso: python3 ec1_parser.py '<expressao>'")
        return

    entrada = sys.argv[1]
    try:
        lexer = Lexer(entrada)
        tokens = []
        while True:
            token = lexer.proximo_token()
            tokens.append(token)
            if token.tipo == TipoToken.EOF:
                break
        
        parser = Parser(tokens)
        ast = parser.analisaExp()

        print("Estrutura da Árvore Sintática:")
        ast.exibir()

        proximo = parser.espiar()
        if proximo and proximo.tipo != TipoToken.EOF:
            parser.erro(f"Tokens extras encontrados após o fim da expressão: '{proximo.lexema}'")
        
        resultado = avaliar(ast)
        print(f"Resultado: {resultado}")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()