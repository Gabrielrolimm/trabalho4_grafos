"""Geração da página HTML de visualização (biblioteca vis-network)."""

import json
from pathlib import Path

from bfs import busca_em_largura, reconstruir_caminho, usuarios_mais_distantes

PASTA = Path(__file__).parent


def montar_dados(grafo, amizades, origem, destino):
    """Roda a BFS a partir de cada usuário e junta tudo o que a página exibe."""
    bfs = {}
    for usuario in grafo:
        distancias, pais, passos = busca_em_largura(grafo, usuario)
        bfs[usuario] = {
            "distancias": distancias,
            "pais": pais,
            "passos": passos,
            "caminhos": {d: reconstruir_caminho(pais, d) for d in distancias},
        }

    dist_max, par = usuarios_mais_distantes(grafo)
    graus = {u: len(amigos) for u, amigos in grafo.items()}
    mais_popular = max(graus, key=graus.get)

    return {
        "usuarios": list(grafo),
        "amizades": amizades,
        "bfs": bfs,
        "inicial": {"origem": origem, "destino": destino},
        "mais_distantes": {
            "distancia": dist_max,
            "par": par,
            "caminho": bfs[par[0]]["caminhos"][par[1]],
        },
        "estatisticas": {
            "usuarios": len(grafo),
            "amizades": len(amizades),
            "grau_medio": round(sum(graus.values()) / len(grafo), 2),
            "mais_popular": mais_popular,
            "grau_max": graus[mais_popular],
        },
    }


def gerar_html(dados, saida=PASTA / "resultado.html"):
    """Insere os dados no template.html e grava a página final."""
    modelo = (PASTA / "template.html").read_text(encoding="utf-8")
    html = modelo.replace("/*DADOS*/", json.dumps(dados, ensure_ascii=False))
    Path(saida).write_text(html, encoding="utf-8")
    return Path(saida)