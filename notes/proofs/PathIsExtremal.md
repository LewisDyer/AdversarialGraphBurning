## THEOREM

Given any connected graph G, let c_G be the maximum number of red clusters that can exist on G. Take G' as a graph such that G' adds one additional edge between any vertices of G that don't currently have an edge between them. Then c_G >= c_G'.

## PROOF





Suppose by contradiction that this isn't the case, and that c_G < c_G'. Consider the colouring on G' which attains c_G' clusters, and consider the same colouring on c_G. Then c_G = c_G', so by contradiction the result follows.

[need to be careful here, to justify that the same colouring is valid on c_G]

## COROLLARY

Hence, for a connected traceable graph on n vertices, the path on n vertices gives the maximum number of clusters possible.

As a remark, this corollary only holds for traceable graphs, i.e graphs containing a Hamiltonian path, because these graphs can be generated by starting with the Hamiltonian path and including additional edges, reapplying the theorem successively.

Idea: Take the longest path as a subgraph of the original vertex. "move" vertices off that path to either end, one by one.

## REMARK

Let C(G) be the set of valid colourings via AGB over the graph G. Defining G' as above, C(G) is not a subset of C(G'), and C(G') is not a subset of C(G) - counterexample is RBBR then connecting vertices 1 and 3 from G to G', and RBRB in the inverse direction with the same connection


# AN ACTUAL PROOF

Each round, at most 1 cluster can be created. 2 vertices are burned, and at least 3 vertices are burned as a result if there are at least 3 unburned vertices. if the chosen vertices both have degree 1, there's there 2 vertices left or another vertex gets burned via spread, since it's a connected graph. and if at least 1 has degree 2 then you get it via spreading.

# COR

at most this many rounds