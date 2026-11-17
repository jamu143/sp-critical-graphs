from splib import *
from gadgets import pupa, butterfly

def join(adj1, adj2, x, y, n, pre1='L_', pre2='R_'):
    """join heads x in G1, y in G2 by path with n internal vertices"""
    E = []
    for a in adj1:
        for b in adj1[a]:
            if a < b: E.append((pre1+a, pre1+b))
    for a in adj2:
        for b in adj2[a]:
            if a < b: E.append((pre2+a, pre2+b))
    prev = pre1+x
    for i in range(1, n+1):
        E.append((prev, f'J{i}')); prev = f'J{i}'
    E.append((prev, pre2+y))
    return mkgraph(E)

def larva(k):
    E = [('x','c1'),('x','c2')]
    for i in range(1,k): E.append((f'c{i}',f'c{i+1}'))
    E.append((f'c{k}','c1'))
    return mkgraph(E)

import time
tests = [
  ("butterfly(3,2,3)+butterfly(3,2,3), n=2 (even)", butterfly(3,2,3), 'v', butterfly(3,2,3), 'v', 2, True),
  ("butterfly+butterfly, n=1 (odd)", butterfly(3,2,3), 'v', butterfly(3,2,3), 'v', 1, False),
  ("butterfly(3,2,3)+larva(4), n=1 (odd)", butterfly(3,2,3), 'v', larva(4), 'x', 1, True),
  ("butterfly+larva, n=2 (even)", butterfly(3,2,3), 'v', larva(4), 'x', 2, False),
  ("pupa(4,2)+pupa(4,2), n=2 (even)", pupa(4,2), 'v', pupa(4,2), 'v', 2, True),
  ("pupa(4,2)+larva(4), n=2 (even)", pupa(4,2), 'v', larva(4), 'x', 2, True),
  ("pupa+larva, n=1 (odd)", pupa(4,2), 'v', larva(4), 'x', 1, False),
  ("larva(4)+larva(4), n=2 (even)", larva(4), 'x', larva(4), 'x', 2, True),
]
for name, A, xa, B, yb, n, expect in tests:
    adj = join(A, B, xa, yb, n)
    verts = frozenset(adj)
    t0=time.time()
    ok, wit = sp_critical_full(adj, verts)
    flag = "OK" if ok == expect else "**MISMATCH**"
    print(f"{flag} {name}: |V|={len(verts)} sp-critical={ok} (expected {expect}) {wit or ''} [{time.time()-t0:.0f}s]", flush=True)
