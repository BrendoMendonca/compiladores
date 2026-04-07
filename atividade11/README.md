# Compilador - Linguagem Fun (Atividade 11)

Este repositório contém a implementação do compilador para a **Linguagem Fun**, desenvolvida para a disciplina de Construção de Compiladores. A linguagem suporta declaração de variáveis globais e locais, estruturas de controle (`if`, `while`), funções com passagem de parâmetros e recursividade.

## 📋 Pré-requisitos

Para executar o compilador e os programas gerados, você precisará ter instalado em ambiente Linux (ou WSL):
- **Python 3.x** (para rodar o compilador).
- **GCC (GNU Compiler Collection)** (para montagem e ligação do código Assembly).

## 📁 Estrutura de Arquivos Necessária

Certifique-se de que todos os arquivos abaixo estão no mesmo diretório:
- `ev_lexer.py`: Analisador léxico.
- `ev_parser.py`: Analisador sintático.
- `ev_ast.py`: Árvore de Sintaxe Abstrata e geração de código x86-64.
- `ev_semantics.py`: Analisador semântico (escopos e offsets de pilha).
- `ev_compiler.py`: Orquestrador do compilador.
- `runtime.s`: Código Assembly de suporte (contém a função `print_int` para exibir resultados na tela).

---

## 🚀 Como Compilar e Executar um Programa

### Passo 1: Criar o arquivo fonte (`.ev`)
Crie um arquivo contendo o código na linguagem Fun. Exemplo (`fib.ev`) que calcula o 5º número da sequência de Fibonacci recursivamente:

<pre>
var x = 0;

fun fib(n) {
    var res = 0;
    if n < 2 {
        res = 1;
    } else {
        res = fib(n - 1) + fib(n - 2);
    }
    return res;
}

main {
    x = fib(5);
    return x;
}
</pre>


### Passo 2: Gerar o código Assembly (.s)

<pre> python3 ev_compiler.py fib.ev out.s </pre>

### Passo 3: Montar o Executável
<pre> gcc -no-pie -nostartfiles out.s -o programa </pre>

### Passo 4: Executar o Programa

<pre>./programa</pre>