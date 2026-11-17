# T17: Theorem 1.3 with n = 0 (edge join) for general descendible/ascendible pairs.
from splib import mkgraph, sp_critical, has_sss
def house(t): 
    c=[f'{t}c{i}' for i in range(4)]
    return [(c[i],c[(i+1)%4]) for i in range(4)]+[(f'{t}h',c[0]),(f'{t}h',c[1])], f'{t}h'
def bfly(t):
    x=f'{t}x'
    return [(f'{t}u1',f'{t}u2'),(x,f'{t}u1'),(x,f'{t}u2'),(x,f'{t}v1'),(f'{t}v1',f'{t}v2'),(f'{t}v2',f'{t}u1'),(x,f'{t}w1'),(f'{t}w1',f'{t}w2'),(f'{t}w2',f'{t}u2')], x
def pend(g,t):   # pendant vertex: flips ascendible <-> descendible (Lemma pendantvertex)
    E,h=g; return E+[(h,f'{t}z')], f'{t}z'
A1=house('A'); A2=pend(pend(house('B'),'B1'),'B2')          # ascendible
D1=bfly('C'); D2=pend(house('D'),'D')                       # descendible
def join(g1,g2): return mkgraph(g1[0]+g2[0]+[(g1[1],g2[1])])
for name,g1,g2,pred in [("asc+asc",A1,A2,True),("desc+desc",D1,D2,True),("desc+asc",D1,A1,False),("desc+asc",D2,A2,False)]:
    adj=join(g1,g2); ok=sp_critical(adj,set(adj),verbose=True)[0]
    assert ok==pred,(name,ok); print(name,"edge join: sp-critical =",ok,"| has sss:",has_sss(adj,set(adj)))
print("ALL T17 CHECKS PASSED")
