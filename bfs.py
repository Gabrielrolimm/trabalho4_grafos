"""Algoritmo de Busca em Largura (BFS) e funções derivadas."""

from collections import deque


def busca_em_largura(grafo, origem):
    """
    BFS a partir de 'origem'.

    Retorna:
      distancias -> {usuario: nº de conexões até a origem}
      pais       -> {usuario: quem o descobriu} (para reconstruir o caminho)
      passos     -> registro de cada iteração (usado na animação)
    """
    distancias = {origem: 0}
    pais = {origem: None}
    fila = deque([origem])

    passos = [{"atual": None, "novos": [], "ignorados": [],
               "fila": list(fila), "visitados": [origem]}]

    while fila:
        atual = fila.popleft()                     # 1) tira o primeiro da fila
        novos, ignorados = [], []
        for vizinho in grafo[atual]:               # 2) olha todos os amigos dele
            if vizinho not in distancias:          # 3) ainda não visitado?
                distancias[vizinho] = distancias[atual] + 1
                pais[vizinho] = atual
                fila.append(vizinho)               # 4) entra no fim da fila
                novos.append(vizinho)
            else:
                ignorados.append(vizinho)

        passos.append({"atual": atual, "novos": novos, "ignorados": ignorados,
                       "fila": list(fila), "visitados": list(distancias)})

    return distancias, pais, passos


def reconstruir_caminho(pais, destino):
    """Volta de pai em pai, do destino até a origem. None se inalcançável."""
    if destino not in pais:
        return None
    caminho = []
    no = destino
    while no is not None:
        caminho.append(no)
        no = pais[no]
    caminho.reverse()
    return caminho


def caminho_mais_curto(grafo, origem, destino):
    """Retorna (distancia, caminho) ou (None, None) se não houver ligação."""
    distancias, pais, _ = busca_em_largura(grafo, origem)
    if destino not in distancias:
        return None, None
    return distancias[destino], reconstruir_caminho(pais, destino)


def usuarios_mais_distantes(grafo):
    """Roda a BFS a partir de cada usuário e guarda o par com maior distância."""
    maior = -1
    par = None
    for usuario in grafo:
        distancias, _, _ = busca_em_largura(grafo, usuario)
        for outro, d in distancias.items():
            if d > maior:
                maior = d
                par = (usuario, outro)
    return maior, par