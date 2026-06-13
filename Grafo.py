# Práctica 3 — Teoría de Grafos | Matemática Discreta
# Ing. Miriam Ávila P. | Software PAO 3
#Integrantes : Quispillo John, Melendrez Camila, Casa Gabriel

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import deque

COLORS = ['#C63B3B','#2472A4','#1D8A55','#C87A1A','#7C4BC4','#1A8FA0','#A03A7A','#5A7A2A']
COLOR_NAMES = ['Rojo','Azul','Verde','Naranja','Morado','Cyan','Rosa','Oliva']


# ACTIVIDAD 1 — Multigrafo
def actividad1():
    print("\nACT. 1 — MULTIGRAFO CON 6 VÉRTICES")

    MG = nx.MultiGraph()
    MG.add_edges_from([(1,3),(2,4),(3,4),(5,6),(3,6),(2,5)])
    for par in [(1,2),(4,5)]:
        MG.add_edge(*par, key=0)
        MG.add_edge(*par, key=1)

    grados = dict(MG.degree())
    impares = [v for v, d in grados.items() if d % 2 != 0]

    print(f"  |V|={MG.number_of_nodes()}  |E|={MG.number_of_edges()}")
    print(f"  Grados: { {f'v{v}': d for v, d in grados.items()} }")
    print(f"  Grado impar en: {impares or 'ninguno'}")
    if   len(impares) == 0: print("  → Circuito Euleriano: SÍ")
    elif len(impares) == 2: print(f"  → Camino Euleriano entre {impares[0]} y {impares[1]}")
    else:                   print("  → Sin circuito ni camino euleriano")

    pos = {1:(1,3), 2:(3,3), 3:(0,1.5), 4:(2,1.5), 5:(4,1.5), 6:(2,0)}
    plt.figure(figsize=(7,5))
    plt.title("Act. 1 — Multigrafo (6 vértices)", fontsize=13)
    nx.draw_networkx_nodes(MG, pos, node_color='#2472A4', node_size=700)
    nx.draw_networkx_labels(MG, pos, font_color='white', font_size=13, font_weight='bold')
    nx.draw_networkx_edges(MG, pos, edge_color='#888', width=1.8, connectionstyle='arc3,rad=0.15')
    nx.draw_networkx_labels(MG, pos, labels={v: f"  d={d}" for v,d in grados.items()},
                            font_size=9, font_color='#555')
    plt.axis('off'); plt.tight_layout()
    plt.savefig('act1_multigrafo.png', dpi=150, bbox_inches='tight')
    plt.show()


# ACTIVIDAD 2 — BFS y DFS manuales
def bfs_manual(adj, src):
    visited, cola, orden, arbol, dist = {src}, deque([src]), [], [], {src: 0}
    while cola:
        v = cola.popleft(); orden.append(v)
        for u in sorted(adj[v]):
            if u not in visited:
                visited.add(u); cola.append(u)
                arbol.append((v,u)); dist[u] = dist[v]+1
    return orden, arbol, dist

def dfs_manual(adj, nodos):
    visited, orden, arbol, tiempo, disc, fin = set(), [], [], [0], {}, {}
    def visit(v):
        visited.add(v); tiempo[0]+=1; disc[v]=tiempo[0]; orden.append(v)
        for u in sorted(adj[v]):
            if u not in visited:
                arbol.append((v,u)); visit(u)
        tiempo[0]+=1; fin[v]=tiempo[0]
    for v in sorted(nodos):
        if v not in visited: visit(v)
    return orden, arbol, disc, fin

def actividad2():
    print("\nACT. 2 — BFS Y DFS MANUALES")

    G = nx.Graph()
    G.add_edges_from([(1,2),(1,3),(2,4),(3,4),(4,5),(2,5),(3,5)])
    adj = {v: list(G.neighbors(v)) for v in G.nodes()}

    orden_bfs, arbol_bfs, dist = bfs_manual(adj, 1)
    orden_dfs, arbol_dfs, disc, fin = dfs_manual(adj, G.nodes())

    print(f"  BFS desde 1 → visita: {orden_bfs}")
    print(f"  BFS árbol  : {arbol_bfs}")
    print(f"  BFS dist   : {dist}")
    print(f"  DFS visita : {orden_dfs}")
    print(f"  DFS árbol  : {arbol_dfs}")
    print(f"  DFS tiempos: { {v:(disc[v],fin[v]) for v in sorted(disc)} }")

    pos = nx.spring_layout(G, seed=7)
    fig, axes = plt.subplots(1, 2, figsize=(12,5))
    fig.suptitle("Act. 2 — BFS vs DFS (implementación manual)", fontsize=13)
    for ax, arbol, titulo, color in [
        (axes[0], arbol_bfs, "BFS desde nodo 1", '#1D8A55'),
        (axes[1], arbol_dfs, "DFS completo",     '#C63B3B'),
    ]:
        tree_set = set(map(frozenset, arbol))
        nx.draw(G, pos, ax=ax, with_labels=True, node_color='#2472A4',
                node_size=700, font_color='white', font_size=13, font_weight='bold',
                edge_color=[color if frozenset(e) in tree_set else '#ccc' for e in G.edges()],
                width=[3 if frozenset(e) in tree_set else 1 for e in G.edges()])
        ax.set_title(titulo, fontsize=11)
    plt.tight_layout()
    plt.savefig('act2_bfs_dfs.png', dpi=150, bbox_inches='tight')
    plt.show()


# ACTIVIDAD 3 — Coloreo K4, K5, C6 
def actividad3():
    print("\nACT. 3 — COLOREO DE K4, K5 Y C6")

    grafos = {
        'K4': (nx.complete_graph(4), 4, 'Kₙ → χ = n'),
        'K5': (nx.complete_graph(5), 5, 'Kₙ → χ = n'),
        'C6': (nx.cycle_graph(6),    2, 'Ciclo par → χ = 2'),
    }
    fig, axes = plt.subplots(1, 3, figsize=(14,5))
    fig.suptitle("Act. 3 — Coloreo Greedy: K4, K5 y C6", fontsize=13)

    for ax, (nombre, (G, chi_t, regla)) in zip(axes, grafos.items()):
        col = nx.coloring.greedy_color(G, strategy='largest_first')
        n   = max(col.values()) + 1
        ok  = '✓' if n == chi_t else '✗'
        print(f"  {nombre}: χ calculado={n}  χ teórico={chi_t}  {ok}  ({regla})")
        nx.draw(G, nx.circular_layout(G), ax=ax,
                node_color=[COLORS[col[v] % len(COLORS)] for v in G.nodes()],
                with_labels=True, node_size=700, font_color='white',
                font_size=13, font_weight='bold', edge_color='#888', width=1.5)
        ax.set_title(f"{nombre}  χ={n} (teórico={chi_t}) {ok}\n{regla}", fontsize=10)
        ax.legend(handles=[mpatches.Patch(color=COLORS[c % len(COLORS)],
                  label=f"{COLOR_NAMES[c]}") for c in range(n)],
                  fontsize=8, loc='lower center', bbox_to_anchor=(0.5,-0.18), ncol=n)

    plt.tight_layout()
    plt.savefig('act3_coloreo.png', dpi=150, bbox_inches='tight')
    plt.show()


#  ACTIVIDAD 4 — Dígrafo + SCCs
def actividad4():
    print("\nACT. 4 — DÍGRAFO 7 NODOS + SCCs")

    D = nx.DiGraph()
    D.add_edges_from([(1,2),(2,3),(3,1),(3,5),(5,4),(4,3),(5,6),(6,7),(7,5)])

    sccs = sorted(nx.strongly_connected_components(D), key=min)
    scc_map = {v: i for i, s in enumerate(sccs) for v in s}

    print(f"  Es DAG: {nx.is_directed_acyclic_graph(D)}")
    print(f"  Grados: { {v: (D.out_degree(v), D.in_degree(v)) for v in D.nodes()} }")
    for i, s in enumerate(sccs, 1):
        print(f"  SCC {i}: {sorted(s)}")

    cond = nx.condensation(D)
    fig, axes = plt.subplots(1, 2, figsize=(13,5))
    fig.suptitle("Act. 4 — Dígrafo y Grafo Condensado", fontsize=13)

    pos = {1:(1,3),2:(3,3),3:(2,2),4:(0,1),5:(2,1),6:(4,1),7:(3,0)}
    nx.draw(D, pos, ax=axes[0], with_labels=True,
            node_color=[COLORS[scc_map[v] % len(COLORS)] for v in D.nodes()],
            node_size=700, font_color='white', font_size=13, font_weight='bold',
            edge_color='#666', width=1.8, arrows=True,
            arrowstyle='->', arrowsize=18, connectionstyle='arc3,rad=0.12')
    axes[0].legend(handles=[mpatches.Patch(color=COLORS[i % len(COLORS)],
                   label=f"SCC {i+1}: {sorted(sccs[i])}") for i in range(len(sccs))],
                   fontsize=9, loc='lower right')
    axes[0].set_title("Dígrafo original (coloreado por SCC)", fontsize=10)

    nx.draw(cond, nx.spring_layout(cond, seed=1), ax=axes[1],
            labels={i: f"S{i+1}\n{sorted(cond.nodes[i]['members'])}" for i in cond.nodes()},
            node_color=[COLORS[i % len(COLORS)] for i in cond.nodes()],
            node_size=1800, font_color='white', font_size=8, font_weight='bold',
            edge_color='#444', width=2, arrows=True, arrowstyle='->', arrowsize=18)
    axes[1].set_title("Grafo condensado (un nodo por SCC)", fontsize=10)

    plt.tight_layout()
    plt.savefig('act4_digrafo_sccs.png', dpi=150, bbox_inches='tight')
    plt.show()


#  ACTIVIDAD 5 — Red de servidores
def actividad5():
    print("\nACT. 5 — RED DE 5 SERVIDORES")

    D = nx.DiGraph()
    D.add_edges_from([('DB','Auth'),('Auth','API'),('API','Cache'),('API','UI')])

    es_dag = nx.is_directed_acyclic_graph(D)
    orden  = list(nx.topological_sort(D)) if es_dag else []

    print(f"  Es DAG: {es_dag}")
    print(f"  Grados: { {v: (D.out_degree(v), D.in_degree(v)) for v in D.nodes()} }")
    if orden:
        print(f"  Orden de despliegue: {' → '.join(orden)}")

    pos = {'DB':(0,1.5),'Auth':(2,2.5),'API':(4,1.5),'Cache':(6,2.5),'UI':(6,0.5)}
    plt.figure(figsize=(10,5))
    plt.title("Act. 5 — Red de Servidores (DAG)", fontsize=13)
    nx.draw_networkx_nodes(D, pos, node_color=[COLORS[i] for i in range(D.number_of_nodes())],
                           node_size=1400, alpha=0.95)
    nx.draw_networkx_labels(D, pos, font_color='white', font_size=12, font_weight='bold')
    nx.draw_networkx_edges(D, pos, edge_color='#555', width=2.2, arrows=True,
                           arrowstyle='->', arrowsize=22,
                           connectionstyle='arc3,rad=0.08',
                           min_source_margin=30, min_target_margin=30)
    if orden:
        pasos = {v: f"Paso {i+1}" for i, v in enumerate(orden)}
        for srv, (x,y) in pos.items():
            plt.text(x, y-0.35, pasos[srv], ha='center', va='top', fontsize=9,
                     color='#333', bbox=dict(boxstyle='round,pad=0.2',
                     fc='#f0f0f0', ec='#bbb', lw=0.8))
    plt.axis('off'); plt.tight_layout()
    plt.savefig('act5_servidores.png', dpi=150, bbox_inches='tight')
    plt.show()


# MAIN 
if __name__ == '__main__':
    print("Práctica 3 — Teoría de Grafos | Matemática Discreta")
    actividad1()
    actividad2()
    actividad3()
    actividad4()
    actividad5()
    print("\nListo. Imágenes guardadas: act1..act5.png")