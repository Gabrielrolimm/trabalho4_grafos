"""Leitura da rede social a partir de um arquivo externo (JSON)."""

import json


def carregar_rede(caminho_arquivo):
    """
    Lê o JSON e monta o grafo como lista de adjacência (dicionário).

    Retorna:
      grafo    -> {usuario: [amigos]}
      amizades -> lista de pares [a, b], como estão no arquivo
    """
    with open(caminho_arquivo, encoding="utf-8") as f:
        dados = json.load(f)

    grafo = {usuario: [] for usuario in dados["usuarios"]}
    for a, b in dados["amizades"]:
        if a not in grafo or b not in grafo:
            raise ValueError(f"Amizade com usuário inexistente: {a} - {b}")
        # amizade é via de mão dupla -> grafo não direcionado
        grafo[a].append(b)
        grafo[b].append(a)
    return grafo, dados["amizades"]