# Compilador Linguagem Cmd - Atividade 10

Este projeto apresenta um compilador completo para a **Linguagem Cmd**, desenvolvido como parte da disciplina de Compiladores. A linguagem é uma evolução da EV, tornando-se Turing-completa ao introduzir estruturas de decisão, repetição e um sistema rigoroso de declaração de variáveis.

## 1. Estrutura do Código (.ev)

Um programa na Linguagem Cmd possui uma estrutura fixa dividida em duas partes:
1. **Área de Declarações**: Localizada no topo, onde todas as variáveis devem ser inicializadas (ex: `x = 10;`).
2. **Bloco de Execução**: Delimitado por chaves `{ ... }`, contendo a lógica do programa e terminando obrigatoriamente com a instrução `return`.

## 2. Componentes do Compilador


### 2.1. Analisador Léxico (`ev_lexer.py`)
Converte o texto em tokens. Foi atualizado para reconhecer novas palavras-chave como `if`, `else`, `while` e `return`, além de operadores de comparação (`<`, `>`, `==`) e delimitadores de bloco.

### 2.2. Analisador Sintático (`ev_parser.py`)
Constroi a Árvore de Sintaxe Abstrata (AST). Ele gerencia a precedência de operadores, garantindo que operações aritméticas sejam calculadas antes das comparações lógicas.

### 2.3. Analisador Semântico (`ev_semantics.py`)
Garante a segurança do código. Ele impede que o programador utilize ou atribua valores a variáveis que não foram declaradas previamente no topo do arquivo.

### 2.4. Gerador de Código (`ev_ast.py`)
Traduz a AST para Assembly x86-64. Utiliza um sistema de **Rótulos Únicos** (ex: `Linicio0`, `Lfalso1`) para implementar saltos condicionais e loops sem conflitos de endereçamento.

## 3. Requisitos de Ambiente

* **SO**: Linux ou Windows com WSL2.
* **Ferramentas**: Python 3.x e GCC (GNU Compiler Collection).

## 4. Como Compilar e Executar

Siga os comandos abaixo no terminal para transformar seu código fonte em um executável:

### Passo 1: Gerar o arquivo Assembly
O compilador processa o arquivo `.ev` e gera o código `.s`.
<pre>
python3 ev_compiler.py fatorial.ev out.s </pre>

### Passo2: Ligar com o Runtime e Criar o Binário
É necessário incluir o arquivo `runtime.s`, que contém a função print_int responsável por exibir os resultados no terminal
<pre> gcc -no-pie -nostartfiles out.s runtime.s -o programa </pre>

### Passo 3: Executar
<pre> ./programa <pre>

