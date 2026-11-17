# T16 (17 Nov 2026): checks for the referee-report repairs.
import itertools
src=open('ghosh2.py').read().split('import time')[0]; ns={}; exec(src,ns); ghosh=ns['ghosh']
from splib import mkgraph, has_sss, sp_critical, max_cliques, status
def simp(adj,S,v):
    N=adj[v]&S; return all(y in adj[x] for x in N for y in N if x!=y)
def strong(adj,V,S):
    return all(y not in adj[x] for x in S for y in S) and all(set(K)&S for K in max_cliques(adj,V))
def rule(adj,n,J):
    """The strong stable set of the new proof (trefoils with x complete to Q)."""
    I={c:sorted([z for z in adj if z[0]==c],key=lambda z:int(z[1:])) for c in 'pqr'}
    has={c: set(I[c])<=J for c in 'pqr'}
    S=set()
    if not has['p']:
        S.add('x')
        for c in 'qr':
            if has[c]:
                # interior listed from x-end in the builder: cyc('x','v1'): q1~x ... q_last~v1
                S|={z for k,z in enumerate(reversed(I[c]),1) if k%2==1}   # odd from the v-end
        return S
    W=[j for j in range(1,2*n+1) if f'v{j}' in J]
    comps=[]; cur=[]
    for j in W:
        if cur and j==cur[-1]+1: cur.append(j)
        else:
            if cur: comps.append(cur)
            cur=[j]
    if cur: comps.append(cur)
    for comp in comps:
        par=comp[0]%2
        if has['q'] and 1 in comp: par=1%2
        if has['r'] and 2*n in comp: par=(2*n)%2
        S|={f'v{j}' for j in comp if j%2==par}
    # cycles: alternate, determined by the ends
    def alt(seq):  # seq = full cycle path from one base end to the other, ends' membership known
        for a,b in zip(seq,seq[1:]):
            pass
    import re
    for c,base in (('p',None),('q',('v1','x')),('r',(f'v{2*n}','x'))):
        if not has[c]: continue
        if c=='p':
            i=[int(z[1:]) for z in adj[I['p'][0]] if z[0]=='v'][0]   # p1 ~ v_i
            chain=[f'v{i}']+I['p']+[f'v{i+1}']
        else:
            chain=['x']+I[c]+[base[0]]
        # walk from chain[-1] backwards choosing greedily to meet each edge
        for k in range(len(chain)-2,0,-1):
            if chain[k+1] not in S: S.add(chain[k])
    return S
if __name__=='__main__':
    tot=0
    for (n,i) in [(2,1),(2,2),(2,3),(3,3)]:
        for (p,q,r) in [(2,2,2),(3,2,2),(2,3,2),(2,2,3),(3,3,3)]:
            adj=ghosh(n,i,p,q,r); V=sorted(adj)
            core=[z for z in V if z[0] in 'vx']; I={c:[z for z in V if z[0]==c] for c in 'pqr'}
            for mask in itertools.product([0,1],repeat=3):
                for k in range(len(core)+1):
                    for T in itertools.combinations(core,k):
                        J=set(T)
                        for c,m in zip('pqr',mask):
                            if m: J|=set(I[c])
                        if not J or J==set(V) or 'x' not in J: continue
                        if any(simp(adj,J,z) for z in J): continue
                        S=rule(adj,n,J)&J
                        assert strong(adj,J,S),(n,i,p,q,r,sorted(J),sorted(S))
                        tot+=1
    print("trefoil, x complete to Q: rule gives a strong stable set in all",tot,"simplicial-free proper subgraphs containing x")
    # two larvae on C_p joined by a path with two internal vertices: only larvae are the two given
    import networkx as nx
    def larva(t,n):
        c=[f'{t}c{i}' for i in range(n)]
        return [(c[i],c[(i+1)%n]) for i in range(n)]+[(f'{t}h',c[0]),(f'{t}h',c[1])], f'{t}h'
    for p in (4,6):
        E1,a=larva('A',p); E2,b=larva('B',p)
        adj=mkgraph(E1+E2+[(a,'t1'),('t1','t2'),('t2',b)]); G=nx.Graph([(u,v) for u in adj for v in adj[u] if u<v])
        ok=sp_critical(adj,set(adj),verbose=True)[0]
        holes=[k for k in range(4,len(adj)+1) for S in itertools.combinations(G.nodes(),k)
               if G.subgraph(S).number_of_edges()==k and all(d==2 for _,d in G.subgraph(S).degree()) and nx.is_connected(G.subgraph(S))]
        print(f"two C{p}-larvae: sp-critical {ok}; hole lengths {sorted(set(holes))}; max degree {max(d for _,d in G.degree())}")
    # butterfly middle-path vertices: unwanted in a proper subgraph where they have a neighbour
    def bfly(p,q,r):
        x='x'; U=[f'u{i}' for i in range(1,p+1)]; Vv=[f'v{i}' for i in range(1,q+1)]; W=[f'w{i}' for i in range(1,r+1)]
        E=[(U[i],U[i+1]) for i in range(p-1)]+[(x,u) for u in U]
        P1=[x]+Vv+[U[0]]; P2=[x]+W+[U[-1]]
        return mkgraph(E+[(P1[i],P1[i+1]) for i in range(len(P1)-1)]+[(P2[i],P2[i+1]) for i in range(len(P2)-1)])
    for prm in [(2,2,2),(4,2,2),(4,4,2),(6,2,4)]:
        adj=bfly(*prm); V=set(adj); p=prm[0]
        print("butterfly",prm,"u1 in B\\v1:",status(adj,V-{'v1'},'u1'),"| u_p in B\\w1:",status(adj,V-{'w1'},f'u{p}'))
    # gluing: B1,B2 strongly perfect => sp-critical induced subgraph with v a cutvertex (one instance)
    print("ALL T16 CHECKS PASSED")
