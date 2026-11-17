"""t19: sp-critical graphs on 10 vertices with no clique cutset that are not
odd holes, antiholes or odd prisms (cf. the closing question of CDS21).
Brute force via t18tests; graphs taken from the referees' census."""
import networkx as nx
from t18tests import sp_critical
L = ['I?ouVAxNO', 'ICpfvp{^_', 'I?r@dawJW', 'I?r@dawZW', 'I?r@dayZW',
     'I?r@dqqJW', 'I?r@dqqZW', 'ICperzw^G']
for g in L:
    G = nx.from_graph6_bytes(g.encode())
    assert sp_critical(G)
    for K in nx.enumerate_all_cliques(G):          # every nonempty clique
        H = G.copy(); H.remove_nodes_from(K)
        assert H.number_of_nodes() == 0 or nx.is_connected(H)
    assert nx.is_connected(G)
    tri = sum(nx.triangles(G).values()) // 3
    assert tri >= 4                                 # holes have 0, odd prisms 2
    assert not all(d == 7 for _, d in G.degree())   # not the antihole
    print(g, 'sp-critical, no clique cutset;', G.number_of_edges(), 'edges,', tri, 'triangles')

# the graph W as described in the paper: C_10 plus eight chords
W = nx.cycle_graph(range(1, 11))
W.add_edges_from([(1,4),(1,6),(2,5),(2,10),(5,7),(5,10),(6,9),(7,10)])
assert nx.is_isomorphic(W, nx.from_graph6_bytes(b'I?r@dawJW')) and sp_critical(W)
import itertools
T = [t for t in itertools.combinations(range(1, 11), 3)
     if all(W.has_edge(a, b) for a, b in itertools.combinations(t, 2))]
assert T == [(1,2,10), (2,5,10), (5,6,7), (5,7,10)], T
print('W = C10 + 8 chords: isomorphic to I?r@dawJW, sp-critical, four triangles as stated')
