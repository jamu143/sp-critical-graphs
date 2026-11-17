# T15 (17 Nov 2026): the moon graph as drawn (3-sun with three ears).
# Triangle x1x2x3; u~x1,x2; v~x2,x3; w~x3,x1; odd paths P2: x1-a1..ap-u,
# P3: x2-b1..bq-v, P1: x3-c1..cr-w with p,q,r >= 2 even; no other edges.
import itertools
from splib import mkgraph, has_sss, sp_critical, max_cliques
def moon(p,q,r):
    E=[('x1','x2'),('x2','x3'),('x3','x1'),('u','x1'),('u','x2'),('v','x2'),('v','x3'),('w','x3'),('w','x1')]
    def ear(s,t,k,tag):
        P=[s]+[f'{tag}{i}' for i in range(1,k+1)]+[t]; return [(P[i],P[i+1]) for i in range(len(P)-1)]
    return mkgraph(E+ear('x1','u',p,'a')+ear('x2','v',q,'b')+ear('x3','w',r,'c'))
def simp(adj,S,v):
    N=adj[v]&S; return all(y in adj[x] for x in N for y in N if x!=y)
def strong(adj,V,S):
    return all(y not in adj[x] for x in S for y in S) and all(set(K)&S for K in max_cliques(adj,V))
if __name__=='__main__':
    for (p,q,r) in [(2,2,2),(2,2,4),(2,4,4),(4,4,4),(2,4,6)]:
        adj=moon(p,q,r); V=set(adj)
        if len(V)<=16:
            assert sp_critical(adj,V,verbose=True)[0]
        assert not has_sss(adj,V)
        # the two-ear subgraphs (ears A,B; with and without x3) and the stated set
        A={f'a{i}' for i in range(1,p+1)}; B={f'b{i}' for i in range(1,q+1)}
        S={'x1','v'}|{f'a{i}' for i in range(2,p+1,2)}|{f'b{i}' for i in range(1,q+1,2)}
        for J in ({'x1','x2','u','v'}|A|B, {'x1','x2','x3','u','v'}|A|B):
            assert all(not simp(adj,J,z) for z in J)
            assert strong(adj,J,S)
        print((p,q,r),"n =",len(V),"ok")
    # classification on (2,2,2) and (2,2,4): nonempty proper simplicial-free induced subgraphs
    for prm in [(2,2,2),(2,2,4)]:
        adj=moon(*prm); V=sorted(adj); found=[]
        for k in range(1,len(V)):
            for T in itertools.combinations(V,k):
                S=set(T)
                if all(not simp(adj,S,z) for z in S): found.append(S)
        print(prm,"simplicial-free proper nonempty subgraphs:",len(found),"sizes",sorted(len(s) for s in found))
    # parity: an even path (odd cycle) gives a non-critical graph
    for prm in [(3,2,2),(3,3,3)]:
        adj=moon(*prm); print(prm,"sp-critical:",sp_critical(adj,set(adj),verbose=True)[0])
    print("ALL T15 CHECKS PASSED")
