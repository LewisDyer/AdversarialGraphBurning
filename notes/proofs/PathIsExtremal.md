## THEOREM

Given any connected graph G, let c_G be the maximum number of red clusters that can exist on G. Take G' as a graph such that G' adds one additional edge between any vertices of G that don't currently have an edge between them. Then c_G >= c_G'.

## PROOF

Suppose by contradiction that this isn't the case, and that c_G < c_G'. Consider the colouring on G' which attains c_G' clusters, and consider the same colouring on c_G. Then c_G = c_G', so by contradiction the result follows.

## COROLLARY

Hence, for a connected graph on n vertices, the path on n vertices gives the maximum number of clusters possible.
