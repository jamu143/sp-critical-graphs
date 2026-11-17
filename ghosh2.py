from splib import *

def ghosh(n, i, p, q, r):
    """path v1..v2n; x ~ v1,v2,vi,vi+1,v_{2n-1},v_{2n};
       C2p contains edge vi-vi+1; C2q contains edge x-v1; C2r contains edge x-v2n."""
    E = [(f'v{j}', f'v{j+1}') for j in range(1, 2*n)]
    def cyc(a, b, size2, tag):
        prev = a
        for s in range(1, size2-1):
            E.append((prev, f'{tag}{s}')); prev = f'{tag}{s}'
        E.append((prev, b))
    cyc(f'v{i}', f'v{i+1}', 2*p, 'p')
    cyc('x', 'v1', 2*q, 'q')
    cyc('x', f'v{2*n}', 2*r, 'r')
    for z in ['v1','v2',f'v{i}',f'v{i+1}',f'v{2*n-1}',f'v{2*n}']:
        E.append(('x', z))
    return mkgraph(list(set(map(lambda e: tuple(sorted(e)), E))))

import time
results=[]
for n in [2,3]:
    for i in range(1, 2*n):
        adj = ghosh(n, i, 2, 2, 2)
        verts = frozenset(adj)
        t0=time.time()
        ok, wit = sp_critical_full(adj, verts)
        results.append((n,i,2,2,2,ok,wit))
        print(f"ghosh(n={n},i={i},p=q=r=2) |V|={len(verts)}: sp-critical={ok}  {wit or ''} [{time.time()-t0:.0f}s]", flush=True)
for (n,i,p,q,r) in [(2,2,3,2,2),(2,2,2,3,2),(2,2,2,2,3),(2,3,3,2,2),(2,3,2,3,2)]:
    adj = ghosh(n,i,p,q,r); verts=frozenset(adj)
    t0=time.time()
    ok, wit = sp_critical_full(adj, verts)
    print(f"ghosh(n={n},i={i},p={p},q={q},r={r}) |V|={len(verts)}: sp-critical={ok}  {wit or ''} [{time.time()-t0:.0f}s]", flush=True)

print("=== n=4 grid ===")
for i in range(2, 8):
    adj = ghosh(4, i, 2, 2, 2)
    verts = frozenset(adj)
    t0=time.time()
    ok, wit = sp_critical_full(adj, verts)
    print(f"ghosh(n=4,i={i}) |V|={len(verts)}: sp-critical={ok}  {wit or ''} [{time.time()-t0:.0f}s]", flush=True)
