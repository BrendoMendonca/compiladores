import sys

#definição dos Tipos de Tokens (Classes Léxicas)
class TipoToken:
    # Literais
    NUMERO = 'NUMERO'
    # Pontuação / Delimitadores
    PAREN_ESQ = 'PAREN_ESQ'
    PAREN_DIR = 'PAREN_DIR'
    # Operadores
    SOMA = 'SOMA'
    SUB = 'SUB'
    MULT = 'MULT'
    DIV = 'DIV'
    # Fim de Arquivo
    EOF = 'EOF'

#Estrutura de Dados do Token 
class Token:
    def __init__(self, tipo, lexema, posicao):
        self.tipo = tipo
        self.lexema = lexema
        self.posicao = posicao

    def __repr__(self):
        # Formato de saída para visualização: <Tipo, Lexema, Posicao> 
        return f"<{self.tipo}, \"{self.lexema}\", {self.posicao}>"

#Analisador Léxico (Lexer)
class Lexer:
    def __init__(self, codigo_fonte):
        self.codigo = codigo_fonte
        self.cursor = 0   # Posição atual no código

    def _avancar(self):
        """Avança o cursor e retorna o caractere atual."""
        self.cursor += 1
        
    def _peek(self):
        """Olha o próximo caractere sem avançar o cursor."""
        if self.cursor >= len(self.codigo):
            return None
        return self.codigo[self.cursor]

    def _ignorar_espacos(self):
        """Pula espaços em branco, tabs e quebras de linha."""
        while self.cursor < len(self.codigo) and self._peek().isspace():
            self.cursor += 1

    def _identificar_numero(self):
        """Identifica uma sequência de dígitos (literal inteiro)"""
        lexema = ""
        pos_inicial = self.cursor
        
        while self.cursor < len(self.codigo) and self._peek().isdigit():
            lexema += self._peek()
            self._avancar()
        
        return Token(TipoToken.NUMERO, lexema, pos_inicial)

    def _identificar_simbolo(self, char):
        """Identifica operadores e pontuação."""
        pos_inicial = self.cursor
        self._avancar() # Avança para consumir o símbolo

        if char == '(':
            return Token(TipoToken.PAREN_ESQ, '(', pos_inicial)
        if char == ')':
            return Token(TipoToken.PAREN_DIR, ')', pos_inicial)
        if char == '+':
            return Token(TipoToken.SOMA, '+', pos_inicial)
        if char == '-':
            return Token(TipoToken.SUB, '-', pos_inicial)
        if char == '*':
            return Token(TipoToken.MULT, '*', pos_inicial)
        if char == '/':
            return Token(TipoToken.DIV, '/', pos_inicial)
        
        #Tratamento de Erro Léxico
        # Se chegou, é um caractere fora do conjunto EC1 (parênteses, operadores e dígitos).
        print(f"Erro léxico na posição {pos_inicial}: Caractere não reconhecido '{char}'", file=sys.stderr)
        sys.exit(1)


    def proximo_token(self):
        """Função principal que retorna o próximo token da entrada."""
        self._ignorar_espacos()

        if self.cursor >= len(self.codigo):
            return Token(TipoToken.EOF, "", self.cursor)

        char = self._peek()
        
        # Prioridade 1: Identificar números (podem ter vários dígitos)
        if char.isdigit():
            return self._identificar_numero()

        # Prioridade 2: Identificar símbolos (parênteses e operadores)
        if char in "()+-*/":
            return self._identificar_simbolo(char)
        
        # Prioridade 3: Erro Léxico
        print(f"Erro léxico na posição {self.cursor}: Caractere inválido '{char}'", file=sys.stderr)
        sys.exit(1)

#Execução do Analisador Léxico
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: {sys.argv[0]} <arquivo_de_entrada.ec1>", file=sys.stderr)
        sys.exit(1)

    nome_arquivo = sys.argv[1]
    
    try:
        with open(nome_arquivo, 'r') as f:
            codigo_fonte = f.read()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.", file=sys.stderr)
        sys.exit(1)

    # Cria o analisador e gera a sequência de tokens (todos de uma vez, interface 2
    lexer = Lexer(codigo_fonte)
    tokens = []
    
    # Exemplo: (33 + (912 * 11))
    print(f"--- Análise Léxica para: {nome_arquivo} ---")
    
    while True:
        token = lexer.proximo_token()
        tokens.append(token)
        print(token)
        
        if token.tipo == TipoToken.EOF:
            break