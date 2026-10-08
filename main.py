"""
Trabalho - Busca em Largura (BFS)
Encontra o caminho mais curto entre dois usuários de uma rede social.

A rede é lida de um arquivo em outro diretório (por padrão, dados/rede.json).

Uso:
    python main.py                                  -> pergunta origem e destino
    python main.py Gabriel Paula                    -> já informa origem e destino
    python main.py Gabriel Paula --rede /outra/pasta/rede.json   (opcional; o padrão vem da variável CAMINHO_REDE)
"""

import argparse
import webbrowser
from pathlib import Path

from bfs import caminho_mais_curto, usuarios_mais_distantes
from rede import carregar_rede
from visualizacao import gerar_html, montar_dados

# ===========================================================================
# CONFIGURAÇÃO: caminho do arquivo da rede
#   - relativo (ex.: "dados/rede.json") -> contado a partir da pasta deste main.py
#   - absoluto (ex.: "/home/gabriel/Desktop/redes/turma.json")
# ===========================================================================
CAMINHO_REDE = "/home/gabriel/Desktop/Gabriel/trabalho4_grafos/trabalho4_grafos/dados/rede.json"


def resolver_caminho(caminho):
    """Converte o texto do caminho num Path absoluto."""
    p = Path(caminho).expanduser()          # entende "~" como a pasta do usuário
    if not p.is_absolute():
        p = Path(__file__).parent / p       # relativo à pasta do main.py
    return p


def ler_argumentos():
    parser = argparse.ArgumentParser(description="Caminho mais curto numa rede social (BFS)")
    parser.add_argument("origem", nargs="?", help="usuário de partida")
    parser.add_argument("destino", nargs="?", help="usuário de chegada")
    parser.add_argument("--rede", default=CAMINHO_REDE,
                        help=f"arquivo JSON da rede (padrão: {CAMINHO_REDE})")
    return parser.parse_args()


def main():
    args = ler_argumentos()

    arquivo_rede = resolver_caminho(args.rede)
    if not arquivo_rede.exists():
        print(f"Arquivo da rede não encontrado: {arquivo_rede}")
        return
    grafo, amizades = carregar_rede(arquivo_rede)
    print(f"Rede lida de: {arquivo_rede}")

    print("Usuários da rede:", ", ".join(grafo))
    origem = args.origem or input("Usuário de partida: ").strip()
    destino = args.destino or input("Usuário de chegada: ").strip()

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