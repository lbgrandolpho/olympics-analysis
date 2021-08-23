import pandas as pd
from collections import Counter
import networkx as nx
import matplotlib.pyplot as plt
from igraph import Graph
import matplotlib.pyplot as plot

# TAMANHO DOS PLOTS
TAM_VERT = 200
FONT = 10


# %%
MEDAL_IND = 0
HAPPY_IND = 1
weights = {'Gold': 2, 'Silver': 1.5, 'Bronze': 1}


# %%
translation = pd.read_csv("noc_regions.csv")
table = {row[1][0]: row[1][1] for row in translation.iterrows()}


# %%
athletes = pd.read_csv("athlete_events.csv")
columns = list(athletes.columns)
NOC = columns.index('NOC')
MEDAL = columns.index('Medal')


# %%
medal_counter = Counter()
for ind, row in athletes.iterrows():
    if type(row[MEDAL]) is str:
        medal_counter[table[row[NOC]]] += weights[row[MEDAL]]


# %%
happy = pd.read_csv("2019.csv")
columns = list(happy.columns)
COUNTRY = columns.index('Country or region')
SCORE = columns.index('Score')
happy_dict = {row[COUNTRY]: row[SCORE] for ind, row in happy.iterrows()}

# %%
union = {k: (v, happy_dict[k]) for k, v in medal_counter.items() if k in happy_dict.keys()}
mid = [(name, tup[0]) for name, tup in union.items()]
mid.sort(key=lambda i: i[1])

order = [i[0] for i in mid]

# %%
g = nx.Graph()
DELTA = 0.05
for name in order:
    g.add_node(
        name, label=name, size=15,
        medal=union[name][MEDAL_IND], happy=union[name][HAPPY_IND]
    )

for c1 in range(len(order)):
    for c2 in range(c1+1, len(order)):
        n1, n2 = order[c1], order[c2]
        if (diff := abs(union[n1][HAPPY_IND] - union[n2][HAPPY_IND])) <= DELTA:
            g.add_edge(n1, n2)

# A FUNÇÃO ABAIXO SÓ FUNCIONA NA VERSÃO MAIS RECENTE DO PYTHON-IGRAPH
# FAVOR ATUALIZAR A VERSÃO INSTALADA CASO OCORRA UM ERRO
ig = Graph.from_networkx(g)
print(f'\n\tAnálise do Grafo\n')
print(f'Número de vértices: {ig.vcount()}')
print(f'Número de arestas: {ig.ecount()}')
print(f'Densidade: {ig.density()}')
print(f'Grau médio: {(sum(v.degree() for v in ig.vs())) / ig.vcount()}')
print(f'Coeficiente de clusterização médio: {ig.transitivity_undirected()}')

#Distribuição de graus
vdeg = [v for v in ig.vs()]
vdeg.sort(key=lambda v: v.degree(), reverse=True)

fig = plot.figure(figsize=(15,15))
plot.title('Distribuição de Graus', fontsize=24)
plot.xticks(ticks=range(ig.vcount()), labels=[v['label'] for v in vdeg], 
    rotation=-90, fontsize=6)
ax = fig.gca()
ax.plot(range(ig.vcount()), [v.degree() for v in vdeg])
plot.show()


# %%
plt.figure(121)
# with_labels=True, font_size=9
nx.draw(
    g, pos=nx.fruchterman_reingold_layout(g, k=.24),
    node_size=TAM_VERT, cmap='cividis', node_color=range(len(union)),
    with_labels=True, font_size=FONT
)
plt.show()


# %%



