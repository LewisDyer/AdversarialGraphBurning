# Plan for writing up so far

1. Definition of adversarial graph burning, along with "clusters"
2. Definition of burning sequences (plus how to "find" regular graph burning in adverserial graph burning)
3. Proof that the maximum number of rounds on a connected graph with n vertices is ceiling(n/3)
4. Corollary that this means the maximum number of clusters is ceiling(n/3), and showing this is attainable on a path.
5. Introducing caterpillar graphs, and the sequence notation for describing all caterpillar graphs
6. Show that, in order to count clusters on caterpillar graphs, you can reduce the number of caterpillars substantially (bitstrings with 0s on the end).
7. Show the algorithmic procedure for counting colours on caterpillar graphs, and justify its complexity.
8. Show this procedure is *exact*, not just a lower bound.