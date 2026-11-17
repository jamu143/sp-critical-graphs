# Verification code for "Some new results on sp-critical graphs"

James Alex and Louis Caccetta

This folder contains the code used to check statements in the paper by
exhaustive search over induced subgraphs. A stable set of a graph is
*strong* if it meets every nonempty maximal clique; a graph is *strongly
perfect* if every induced subgraph has a strong stable set; and a graph is
*sp-critical* if it is not strongly perfect but every proper induced
subgraph is.

## Requirements

Python 3.9 or later and `networkx`:

    pip install networkx

Run each script from this folder, for example `python3 t19tests.py`. Each
script stops with an assertion error if a check fails.

## What is proved by computer in the paper

Two statements in the paper rest on computation. No other proof depends on it.

| Statement in the paper | Script |
|---|---|
| The graph W (a cycle of length ten plus eight chords) is sp-critical and has no clique cutset; the seven further graphs listed after it have the same properties | `t19tests.py` |
| The properties of the graphs E and F (strong perfection, their strong stable sets, the status of the distinguished vertex in every induced subgraph) | `t18tests.py` |

`t18tests.py` and `t19tests.py` use plain brute force and do not import
`splib.py`.

## Additional checks (not needed for any proof)

| Script | What it checks |
|---|---|
| `t18tests.py` | The exact cutvertex criterion against brute force on all pairs of small rooted strongly perfect graphs; that no descendible or ascendible vertex of a small graph is a cutvertex |
| `t15tests.py` | Moon graphs for small parameters, and that wrong parities fail |
| `t16tests.py` | The trefoil criterion for small parameters; the two-larvae family; the butterfly non-examples |
| `t17tests.py` | Joins by a single edge (the case of a path with no internal vertex) |

## Library files

| File | Contents |
|---|---|
| `splib.py` | Maximal cliques, strong stable sets, strong perfection, sp-criticality, status of a vertex |
| `gadgets.py` | Larvae, pupae and butterflies |
| `families.py` | The families obtained by joining gadgets |
| `ghosh2.py` | The trefoil graphs G(n, i, p, q, r). Importing this file runs a battery of checks |

## Data

`sp_critical_upto10.g6` lists, in graph6 format, all sp-critical graphs on
at most ten vertices: 1, 1, 2, 3, 4 and 77 graphs on 5, 6, 7, 8, 9 and 10
vertices. The list was produced by two independent enumerations that agree.
The statement in the paper that no graph on at most nine vertices, and
exactly eight graphs on ten vertices, are sp-critical with no clique cutset
and are not odd holes, antiholes or odd prisms was obtained from this list.

## Running time

`t19tests.py` takes about a minute. `t18tests.py` takes several minutes,
because it checks graphs on up to sixteen vertices by brute force.
