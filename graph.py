import networkx as nx

# Defina os vértices e as arestas
vértices = [0, 1, 2, 3, 4, 5]
arestas = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 3), (1, 4), (1, 5), (2, 3), (2, 4), (2, 5),(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (2, 1), (3, 1), (4, 1), (5, 1), (3, 2), (4, 2), (5, 2), (4, 5), (5, 4)]

# Crie um grafo direcionado a partir dos vértices e arestas
G = nx.DiGraph()
G.add_nodes_from(vértices)
G.add_edges_from(arestas)

# Calcule o coeficiente de agrupamento médio
clustering_coefficient = nx.average_clustering(G)
print(f'Coeficiente de Agrupamento Médio: {clustering_coefficient}')
# Calcule a distância média apenas se o grafo estiver conectado
if nx.is_strongly_connected(G):
    average_shortest_path_length = nx.average_shortest_path_length(G)
    print(f'Distância Média: {average_shortest_path_length}')
else:
    print('O grafo não é fortemente conectado. Não é possível calcular a distância média.')