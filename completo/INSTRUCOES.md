O analisador processa expressões aritméticas onde todas as operações devem estar entre parênteses

Comando básico:
No terminal Linux, execute o ec1_parser.py passando a expressão desejada entre aspas:
python3 ec1_parser.py "(10+(5*2))"
O que o programa faz:
Análise Léxica: Converte o texto em uma sequência de tokens
Análise Sintática: Constrói uma Árvore de Sintaxe Abstrata (AST)
Interpretação: Percorre a árvore recursivamente e exibe o valor calculado

Testando via Arquivo testes.txt
Para validar várias expressões de uma vez, utilize o seguinte comando no terminal:
1-dê o comanddo: nano executar_testes.sh

2-copie o código abaixo e cole no arquivo:

#!/bin/bash
ARQUIVO_TESTES="testes.txt"
echo "=== Iniciando Testes do Compilador EC1 ==="

if [ ! -f "$ARQUIVO_TESTES" ]; then
    echo "Erro: Arquivo $ARQUIVO_TESTES nao encontrado!"
    exit 1
fi

while read -r linha; do
    # Pula linhas vazias ou comentarios
    if [[ -n "$linha" && ! "$linha" =~ ^# ]]; then
        echo "---------------------------------------"
        echo "Testando entrada: $linha"
        python3 ec1_parser.py "$linha"
    fi
done < "$ARQUIVO_TESTES"

echo "---------------------------------------"
echo "Fim dos testes."

3-salve (ctrl+O, enter) e saia (ctrl+X)


4-dê permissão e execute:
chmod +x executar_testes.sh
./executar_testes.sh



