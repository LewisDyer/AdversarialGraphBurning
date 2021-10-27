### Notes on Burning sequences

In order to describe a single instance of adversarial graph burning, a convenient notation could be to define a _burning sequence_, listing which vertices are burned at each step.

This sequence consists of a sequence of _tuples_, (v1, v2), such that player 1 burns vertex v1 and player 2 burns vertex v2.

# Validity

Given a sequence S, how can we tell whether it represents a valid burning? We need to know that each vertex is unburned when it's chosen, so we add the additional constraint that:

* For some element of the sequence x_n, for each x_(n-i), for i between 1 and n inclusive (starting at 0!), each vertex in x_n is more than distance i from each vertex in x_(n-1)

So for instance, the vertices are distance more than 1 from the last entry, more than 2 from the last entry, and so on...

## Relation to Graph Burning

From this, it's clear that regular graph burning is a subset of Adversarial Graph Burning, by taking sequences where v1=v2 for all elements (v1, v2), with the same constraints on distance as above.

## Length of Burning sequences

It's also clear that burning sequences must be finite, with length at most |V| (on a graph with n nodes, n separate components with one vertex each, with each player burning the same vertex each time).

But this can be reduced further. For each connected component in a graph, its _diameter_, diam(C) is the longest path between any two vertices in the component. Equivalently, starting at any vertex, you can reach any other vertexes in diam(C) rounds.

As a result, you can have at most diam(C) vertices from any one component in the sequence, so the number of rounds is bounded by ceiling(S/2), where S is the sum of all diameters for each component, or simply ceiling(diameter/2) for a connected graph.