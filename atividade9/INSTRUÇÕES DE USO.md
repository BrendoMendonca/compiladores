# Compilador EV (Expressões com Variáveis) - Atividade 09

Implementação do compilador para a linguagem **EV**
A linguagem evoluiu para suportar a declaração de variáveis de 64 bits, persistência em memória e verificação semântica rigorosa.

## 🚀 Visão Geral
O compilador transforma código fonte `.ev` em executáveis binários para Linux x86-64. O diferencial desta versão é a introdução de uma **Tabela de Símbolos**, que impede erros comuns de programação, como o uso de variáveis não declaradas.

---

## 🛠️ Arquitetura do Compilador
O pipeline de compilação segue as seguintes etapas:
1. **Análise Léxica**: Identificação de tokens como números, identificadores, operadores e símbolos (`;`, `=`).
2. **Análise Sintática**: Construção da Árvore de Sintaxe Abstrata (AST).
3. **Análise Semântica**: Verificação de escopo e declaração de variáveis.
4. **Geração de Código**: Tradução da AST para Assembly x86-64, com reserva de memória na seção `.bss`.



---

## 📝 Instruções de Uso

### 1. Testes Manuais

#### Caso de Sucesso (`teste.ev`)

### 1. Gerar o código Assembly
<pre> python3 ev_compiler.py teste.ev out.s  </pre>

### 2. Montar o executável com GCC
<pre> gcc -no-pie -nostartfiles out.s -o prog </pre>

### 3. Executar o programa
<pre> ./prog </pre>
Resultado esperado: 150

### Caso de Fracasso (`teste_erro.ev`)

comando:
<pre> python3 ev_compiler.py teste_erro.ev out.s </pre>

## Testes Automatizados

Para facilitar a correção e garantir que todas as regras da gramática estão sendo seguidas, utilize o script de teste automatizado. Ele valida 6 cenários distintos

comando:
<pre> python3 test_runner.py </pre>