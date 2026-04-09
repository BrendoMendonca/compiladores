# Projeto Final - Compilador Linguagem Fun

Este repositório contém a implementação final do compilador para a **Linguagem Fun**, desenvolvida para a disciplina de Construção de Compiladores. A linguagem base (Atividade 11) é Turing-completa e foi expandida com diversas extensões sintáticas e semânticas.

## 🚀 Extensões Implementadas

O compilador foi estendido muito além da sua especificação original, contando com as seguintes funcionalidades:

### Extensões Simples
1. **Novos Operadores de Comparação:** Suporte a `<=` (menor ou igual), `>=` (maior ou igual) e `!=` (diferente).
2. **Operadores Lógicos:** Avaliação de curto-circuito com `and` e `or`, além do operador unário `not`.
3. **Atribuição Composta:** Sintaxe enxuta para operações matemáticas diretas na variável (`+=`, `-=`, `*=`, `/=`).

### Extensão de Complexidade Média
1. **Arrays de Inteiros (Vetores):** Suporte completo à declaração, atribuição e acesso a arrays indexados (ex: `vetor[0] = 10;`). A implementação inclui:
   - **Arrays Globais:** Alocados dinamicamente na seção `.bss` utilizando `.zero` com base no tamanho do array.
   - **Arrays Locais:** Alocados diretamente no *Stack Frame* da função, ajustando o registrador `%rsp` proporcionalmente ao número de bytes necessários.
   - Acesso à memória O(1) gerando código Assembly com *Scaled Index Addressing* (`base + índice * 8`).

---

## 📋 Pré-requisitos

Para compilar e executar os códigos em Fun, é necessário um ambiente Linux/WSL com:
- **Python 3.x**
- **GCC (GNU Compiler Collection)**

## 📁 Como Compilar e Executar

A compilação é dividida na tradução para Assembly (via Python) e a montagem/ligação (via GCC).

**1. Gere o código Assembly (`out.s`) a partir do arquivo fonte (`.ev`):**
<pre>
python3 ev_compiler.py arquivo_fonte.ev out.s 
</pre>

**2. Monte o executável**
<pre> gcc -no-pie -nostartfiles out.s -o programa </pre>

**3. Execute o Binário**
<pre> ./programa </pre>

### Exemplo de código suportado

<pre>
var vetor_global[2];
var x = 10;

main {
    
    var vetor_local[3];
    var resultado = 0;
    
    # Atribuição Simples e Arrays Locais
    vetor_local[0] = 5;
    vetor_local[1] = 10;
    
    # Atribuição Composta
    x += 5; # x vira 15
    
    # Arrays Globais
    vetor_global[0] = vetor_local[1] * 2; # 20
    
    # Operadores Lógicos e Novas Comparações
    if (x >= 15) and not (vetor_global[0] != 20) {
        resultado = vetor_local[0] + vetor_local[1] + vetor_global[0]; # 5 + 10 + 20
    } else {
        resultado = 0;
    }
    
    return resultado; # Retorna 35
}
</pre>
