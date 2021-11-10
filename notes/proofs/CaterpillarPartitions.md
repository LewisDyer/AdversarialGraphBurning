
longest path in directed graph problem!

each partition of 3 is a "layer" - each layer gives the boundary points. For going into a new layer, it's either that the "next vertex in" is red, blue, blank and preceded by blue or blank and preceded by red.

When we move along an edge, each edge is weighted with the amount of clusters that START(!) in that partition of 3. So the objective is to bring the directed path from start to finish with the highest weight.

Three steps to the problem:

1. Construct the digraph for each bitstring of length 3, along with the bitstrings 0, 00 and 10. Each of these digraphs has a set of 4 start vertices, going to 4 end vertices: BW if the previous vertex is blue and the bottom left is blank, similarly for RW, and B/R if the bottom left is already blue or red, respectively. Each edge has a weight for the number of the maximum red clusters which START in that partition, across all colourings with that given start and end. I could also store the exact colouring that attains each cluster count in this label, but that's not fully necessary here. This process is quite time-consuming, but not massively hard. How to compute these tables? I could probably automate this process, with some care...

2. For the full bitstring, combine the directed graphs together in "layers" to make the final graph. (for the first and last bitstrings, some minor tweaks are needed. For the first one, only need to start with BW. For the last one, need to be a bit more careful, I think?)

3. This produces a directed acyclic graph (DAG) - use standard algorithms to compute the maximum weight directed path from the start to the end.


I'm not sure if this will give the "optimal" amount of clusters (keeping in mind that each bitstring of length 3 will contain either 0,1 or 2 new clusters). But I could also argue that this approach can be generalised for different sizes of partitions (not just 3), which gives a tradeoff between the size of the graph and the difficulty of computing each step of the graph.