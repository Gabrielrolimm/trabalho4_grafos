"""
Trabalho - Busca em Largura (BFS)
Encontra o caminho mais curto entre dois usuários de uma rede social.

Uso:
    python main.py                      -> pergunta origem e destino
    python main.py Gabriel Paula        -> já informa origem e destino
    python main.py Gabriel Paula outra_rede.json
"""

import sys
import webbrowser
from pathlib import Path

from bfs import caminho_mais_curto, usuarios_mais_distantes
from rede import carregar_rede
from visualizacao import gerar_html, montar_dados


def main():
    arquivo_rede = sys.argv[3] if len(sys.argv) > 3 else Path(__file__).parent / "rede.json"
    grafo, amizades = carregar_rede(arquivo_rede)

    print("Usuários da rede:", ", ".join(grafo))
    if len(sys.argv) >= 3:
        origem, destino = sys.argv[1], sys.argv[2]
    else:
        origem = input("Usuário de partida: ").strip()
        destino = input("Usuário de chegada: ").strip()

    for nome in (origem, destino):
        if nome not in grafo:
            print(f"Usuário '{nome}' não existe na rede.")
            return

    # 1) distância e caminho mais curto
    distancia, caminho = caminho_mais_curto(grafo, origem, destino)
    print()
    if caminho:
        print(f"Distância entre {origem} e {destino}: {distancia} conexões")
        print("Caminho mais curto:", " -> ".join(caminho))
    else:
        print(f"Não existe caminho entre {origem} e {destino}.")

    # 2) usuários mais distantes
    dist_max, par = usuarios_mais_distantes(grafo)
    print(f"Usuários mais distantes: {par[0]} e {par[1]} ({dist_max} conexões)")

    # 3) visualização
    saida = gerar_html(montar_dados(grafo, amizades, origem, destino))
    print(f"\nVisualização gerada em: {saida}")
    webbrowser.open(saida.resolve().as_uri())


if __name__ == "__main__":
    main()