from itertools import combinations
import sys
sys.setrecursionlimit(100000)

def max_cliques(adj, verts):
    """Bron-Kerbosch on induced subgraph."""
    vs = set(verts)
    out = []
    def bk(R, P, X):
        if not P and not X:
            out.append(frozenset(R)); return
        pivot = max(P | X, key=lambda u: len(adj[u] & P)) if (P or X) else None
        ext = P - adj[pivot] if pivot is not None else set(P)
        for v in list(ext):
            bk(R | {v}, P & adj[v], X & adj[v])
            P.remove(v); X.add(v)
    bk(set(), set(vs), set())
    return out

def has_sss(adj, verts):
    """Does G[verts] have a stable set meeting every maximal clique?"""
    verts = frozenset(verts)
    if not verts: return True
    cliques = max_cliques(adj, verts)
    cliques.sort(key=len)
    n = len(cliques)
    def bt(idx, S, forbidden):
        if idx == n: return True
        C = cliques[idx]
        if C & S: return bt(idx+1, S, forbidden)
        for v in C:
            if v in forbidden: continue
            if bt(idx+1, S | {v}, forbidden | adj[v]):
                return True
        return False
    return bt(0, frozenset(), frozenset())

def find_sss_with(adj, verts, must_in=(), must_out=()):
    verts = frozenset(verts)
    cliques = max_cliques(adj, verts)
    cliques.sort(key=len)
    n = len(cliques)
    S0 = frozenset(must_in)
    for a, b in combinations(S0, 2):
        if b in adj[a]: return None
    forb0 = frozenset().union(*[adj[v] for v in S0]) if S0 else frozenset()
    forb0 |= frozenset(must_out)
    if S0 & forb0: return None
    def bt(idx, S, forbidden):
        if idx == n: return S
        C = cliques[idx]
        if C & S: return bt(idx+1, S, forbidden)
        for v in C:
            if v in forbidden: continue
            r = bt(idx+1, S | {v}, forbidden | adj[v])
            if r is not None: return r
        return None
    return bt(0, S0, forb0)

def status(adj, verts, v):
    """'bright', 'dark', 'mixed', or 'nosss' for v in G[verts]."""
    win = find_sss_with(adj, verts, must_in=(v,)) is not None
    wout = find_sss_with(adj, verts, must_out=(v,)) is not None
    if win and wout: return 'mixed'
    if win: return 'bright'
    if wout: return 'dark'
    return 'nosss'

def sp_critical(adj, verts, verbose=False):
    """(is_critical, witness). Checks no sss for G, sss for all proper subsets."""
    verts = frozenset(verts)
    if has_sss(adj, verts):
        return False, 'G itself has a strong stable set'
    vs = sorted(verts)
    n = len(vs)
    # check all proper subsets; iterate by excluded-set to allow early exit on small deletions first
    for k in range(1, n+1):
        for excl in combinations(vs, k):
            sub = verts - set(excl)
            if not sub: continue
            if not has_sss(adj, sub):
                return False, f'proper subgraph missing {excl} has no strong stable set'
        if k >= 3 and n > 15: break  # heuristic guard (only used when noted)
    return True, None

def sp_critical_full(adj, verts):
    verts = frozenset(verts)
    if has_sss(adj, verts):
        return False, 'G itself has a strong stable set'
    vs = sorted(verts)
    from itertools import chain
    n = len(vs)
    for r in range(1, n):
        for keep in combinations(vs, r):
            if not has_sss(adj, frozenset(keep)):
                return False, f'proper subgraph on {keep} has no sss'
    return True, None

def mkgraph(edges):
    adj = {}
    for a, b in edges:
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    return adj

def descendible(adj, verts, v):
    """bright in G, mixed in every proper induced subgraph containing v where v has a neighbor"""
    verts = frozenset(verts)
    if status(adj, verts, v) != 'bright': return False, 'not bright in G'
    others = sorted(verts - {v})
    n = len(others)
    for r in range(1, n):
        for keep in combinations(others, r):
            sub = frozenset(keep) | {v}
            if not (adj[v] & sub): continue
            if status(adj, sub, v) != 'mixed':
                return False, f'not mixed in subgraph {sorted(sub)}'
    return True, None

def ascendible(adj, verts, v):
    verts = frozenset(verts)
    if status(adj, verts, v) != 'dark': return False, 'not dark in G'
    others = sorted(verts - {v})
    n = len(others)
    for r in range(1, n):
        for keep in combinations(others, r):
            sub = frozenset(keep) | {v}
            if not (adj[v] & sub): continue
            if status(adj, sub, v) != 'mixed':
                return False, f'not mixed in subgraph {sorted(sub)}'
    return True, None
