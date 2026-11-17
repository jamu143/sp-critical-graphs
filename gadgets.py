from splib import *

def pupa(k, t):
    """even hole c1..ck; odd path v-p1-...-pt-c1 (t even>=2); c2 complete to {v,p1..pt,c1}"""
    E = []
    for i in range(1, k): E.append((f'c{i}', f'c{i+1}'))
    E.append((f'c{k}', 'c1'))
    prev = 'v'
    for i in range(1, t+1):
        E.append((prev, f'p{i}')); prev = f'p{i}'
    E.append((prev, 'c1'))
    for z in ['v'] + [f'p{i}' for i in range(1, t+1)] + ['c1']:
        if z != 'c2': E.append(('c2', z))
    return mkgraph(list(set(map(lambda e: tuple(sorted(e)), E))))

def butterfly(k, l, m):
    """P1=a1..ak even path (k odd), P2=b1..bl odd (l even), P3=c1..cm even (m odd);
       ak=b1, bl=c1; v complete to {b1..bl, a1, cm}"""
    names = [f'a{i}' for i in range(1, k+1)] + [f'b{i}' for i in range(2, l+1)] + [f'c{i}' for i in range(2, m+1)]
    E = [(names[i], names[i+1]) for i in range(len(names)-1)]
    bs = [f'a{k}'] + [f'b{i}' for i in range(2, l+1)]  # b1..bl
    for z in bs + ['a1', f'c{m}' if m > 1 else f'a{k}']:
        E.append(('v', z))
    return mkgraph(list(set(map(lambda e: tuple(sorted(e)), E))))

print("== pupa heads ==")
for (k,t) in [(4,2),(6,2),(4,4)]:
    adj = pupa(k,t); verts = frozenset(adj)
    print(f"pupa(k={k},t={t}) |V|={len(verts)} status(v)={status(adj,verts,'v')}", end=' ')
    ok, wit = ascendible(adj, verts, 'v')
    print(f"ascendible={ok} {wit or ''}")

print("== butterfly heads ==")
for (k,l,m) in [(3,2,3),(5,2,3),(3,4,3),(3,2,5),(5,4,3)]:
    adj = butterfly(k,l,m); verts = frozenset(adj)
    print(f"butterfly(k={k},l={l},m={m}) |V|={len(verts)} status(v)={status(adj,verts,'v')}", end=' ')
    ok, wit = descendible(adj, verts, 'v')
    print(f"descendible={ok} {wit or ''}")

print("== larva head (sanity) ==")
adjL = mkgraph([('x','c1'),('x','c2'),('c1','c2'),('c2','c3'),('c3','c4'),('c4','c1')])
print("larva C4:", ascendible(adjL, frozenset(adjL), 'x'))
