"""t18: independent test of the exact cutvertex criterion (referee item R2),
the two examples E1, E2, and the lemma 'a non-isolated descendible or
ascendible vertex is not a cutvertex' (R3).  Pure brute force; no splib."""
import itertools, random, sys
import networkx as nx
from networkx.generators.atlas import graph_atlas_g

def all_sss(G):
    V = list(G)
    if not V: return [frozenset()]
    cl = [frozenset(c) for c in nx.find_cliques(G)]
    out = []
    def rec(i, S, forb):
        if i == len(V):
            if all(S & c for c in cl): out.append(frozenset(S))
            return
        v = V[i]
        rec(i+1, S, forb)
        if v not in forb:
            rec(i+1, S | {v}, forb | set(G[v]))
    rec(0, frozenset(), frozenset())
    return out

def has_sss(G):
    V = list(G)
    if not V: return True
    cl = [frozenset(c) for c in nx.find_cliques(G)]
    cl.sort(key=len)
    def rec(S, forb, rest):
        for c in rest:
            if not (S & c):
                for v in c:
                    if v not in forb and rec(S | {v}, forb | set(G[v]) | {v}, rest):
                        return True
                return False
        return True
    return rec(frozenset(), frozenset(), cl)

def status(G, v):
    ss = all_sss(G)
    if not ss: return 'none'
    k = sum(v in S for S in ss)
    return 'wanted' if k == len(ss) else 'unwanted' if k == 0 else 'mixed'

def strongly_perfect(G):
    V = list(G)
    return all(has_sss(G.subgraph(S)) for r in range(1, len(V)+1)
               for S in itertools.combinations(V, r))

def sub_statuses(G, v):
    """statuses of v over proper induced subgraphs containing v and a neighbour"""
    V = [u for u in G if u != v]; res = set()
    for r in range(1, len(V)):
        for S in itertools.combinations(V, r):
            if not (set(S) & set(G[v])): continue
            res.add(status(G.subgraph(S + (v,)), v))
    return res

def glue(G1, x, G2, y):
    H = nx.Graph()
    f = lambda u: 'v' if u == x else ('a', u)
    g = lambda u: 'v' if u == y else ('b', u)
    H.add_nodes_from(map(f, G1)); H.add_nodes_from(map(g, G2))
    H.add_edges_from((f(a), f(b)) for a, b in G1.edges)
    H.add_edges_from((g(a), g(b)) for a, b in G2.edges)
    return H

def sp_critical(H):
    if has_sss(H): return False
    V = list(H)
    for r in range(len(V)-1, 0, -1):
        for S in itertools.combinations(V, r):
            if not has_sss(H.subgraph(S)): return False
    return True

E1 = nx.Graph([(0,3),(0,4),(0,5),(1,4),(1,5),(1,6),(2,5),(2,6),(3,5),(3,6),(4,6),(5,6)])
E2 = nx.Graph([(0,3),(0,4),(0,5),(0,6),(0,7),(1,3),(1,5),(2,4),(2,5),(2,6),(2,7),
               (3,5),(3,6),(3,7),(4,6),(4,7),(5,7)])
HOUSE = nx.Graph([(0,1),(0,2),(1,2),(1,3),(2,4),(3,4)])   # head 0

if __name__ == '__main__':
    random.seed(1)
    # --- examples
    assert strongly_perfect(E1) and status(E1, 2) == 'unwanted'
    assert all(status(E1.subgraph(set(E1)-{u}), 2) == 'mixed' for u in E1 if u != 2)
    assert status(E1.subgraph(set(E1)-{1,3}), 2) == 'unwanted'
    for n in (0, 2):
        J = glue(E1, 2, nx.path_graph(['t0']+[('p',i) for i in range(n)]+['t1']), 't0')
        J = glue(J, ('b','t1'), HOUSE, 0)
        assert not has_sss(J) and not sp_critical(J)
    print('E1: CDS-undesirable, not ascendible, joins to a house head not sp-critical: OK')
    assert strongly_perfect(E2) and status(E2, 1) == 'wanted'
    st = sub_statuses(E2, 1); assert st == {'mixed', 'unwanted'}, st
    H = glue(E2, 1, HOUSE, 0)
    assert sp_critical(H) and list(nx.articulation_points(H)) == ['v']
    print('E2: wanted, never wanted below, sometimes unwanted; E2+house sp-critical, unique cutvertex: OK')

    # --- rooted sides
    W, U = [], []          # (G, v, statuses below)
    asc_desc_cut = 0
    for G in graph_atlas_g()[1:]:
        n = G.number_of_nodes()
        if n < 2 or n > 7 or not nx.is_connected(G): continue
        if not strongly_perfect(G): continue
        ss = all_sss(G); cuts = set(nx.articulation_points(G))
        for v in G:
            k = sum(v in S for S in ss)
            if 0 < k < len(ss): continue
            kind = 'w' if k == len(ss) else 'u'
            if n <= 6 or kind == 'w':
                st = sub_statuses(G, v)
                if st <= {'mixed'} and v in cuts: asc_desc_cut += 1
                if v in cuts: continue
                if kind == 'w': W.append((G, v, st))
                elif n <= 6: U.append((G, v, st))
    W.append((E2, 1, sub_statuses(E2, 1)))
    print('rooted sides: wanted', len(W), ' unwanted', len(U),
          ' descendible/ascendible cutvertices found:', asc_desc_cut)
    assert asc_desc_cut == 0

    def predict(sw, su):
        a = 'wanted' not in sw; b = 'unwanted' not in su
        c = not ('unwanted' in sw and 'wanted' in su)
        return a and b and c
    pairs = [(w, u) for w in W for u in U
             if w[0].number_of_nodes() + u[0].number_of_nodes() - 1 <= 12]
    pos = [p for p in pairs if predict(p[0][2], p[1][2])]
    neg = [p for p in pairs if not predict(p[0][2], p[1][2])]
    # negatives that fail only (c), or only (a), or only (b) are the informative ones
    near = [p for p in neg if sum([('wanted' in p[0][2]), ('unwanted' in p[1][2])]) <= 1]
    random.shuffle(near); random.shuffle(neg)
    test = pos + near[:150] + neg[:100]
    bad = 0
    for (G1, x, sw), (G2, y, su) in test:
        H = glue(G1, x, G2, y)
        if sp_critical(H) != predict(sw, su): bad += 1
    onlyc = sum(1 for p in pairs if 'wanted' not in p[0][2] and 'unwanted' not in p[1][2]
                and not predict(p[0][2], p[1][2]))
    print('pairs', len(pairs), ' predicted critical', len(pos), ' fail only (c):', onlyc,
          ' tested', len(test), ' disagreements', bad)
    assert bad == 0

    # --- all remaining pairs, and a direct test of condition (c)
    bad = sum(1 for (G1, x, sw), (G2, y, su) in pairs
              if ((G1, x, sw), (G2, y, su)) not in test
              and sp_critical(glue(G1, x, G2, y)) != predict(sw, su))
    print('remaining pairs tested, disagreements', bad); assert bad == 0
    # U-side: E2 with a pendant vertex z at v.  z is unwanted, never unwanted
    # below (so (b) holds), but wanted in some proper subgraph.  With W = E2,
    # (a) and (b) hold and (c) fails; with W = pendant-on-house-head
    # (descendible), all three hold.
    E2p = E2.copy(); E2p.add_edge(1, 'z')
    su = sub_statuses(E2p, 'z'); assert status(E2p, 'z') == 'unwanted' and su == {'mixed', 'wanted'}
    Hc = glue(E2, 1, E2p, 'z')
    assert not has_sss(Hc) and not sp_critical(Hc)
    print('(c) fails => not sp-critical (E2 with E2+pendant, 16 vertices): OK')
    Hp = HOUSE.copy(); Hp.add_edge(0, 'w')
    assert sub_statuses(Hp, 'w') <= {'mixed'} and status(Hp, 'w') == 'wanted'
    assert sp_critical(glue(Hp, 'w', E2p, 'z'))
    print('descendible side with half-type side E2+pendant: sp-critical (14 vertices): OK')
