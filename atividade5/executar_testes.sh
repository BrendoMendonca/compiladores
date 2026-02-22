#!/bin/bash

# Script de teste para a Atividade 05 - EC1 [cite: 1]
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
