# Burn Strategies

In Adverserial Graph Burning, it's natural for each player to develop a strategy for choosing which vertex they should burn at each round. Across all strategies, several conditions must hold:

* A player may view the whole state of the graph before burning a vertex - there is no hidden information here
* A player can only burn a vertex that is currently unburned by either player.
* Both players choose a vertex to burn simultaneously, so each player doesn't know which vertex the other player has chosen.

Under these constraints, many different strategies are possible. This document aims to summarise each burn strategy which I've developed.

### "Random"

Pick any unburned vertex randomly.

This is mainly designed as a baseline measure to compare other burn strategies to.

### "Degree"

Pick the unburned vertex with highest degree, only considering adjacency to other unburned vertices (e.g an unburned vertex surroudned by burned vertices has degree 0 for the purposes of this strategy).

The idea here is that nodes with higher degree are often more central, so burning here leads to a fire that spreads quickly.

### "Between"

Consider the subgraph of that player's own vertex, along with unburned vertex, and pick the unburned vertex with highest betweenness centrality on this graph.

The idea here is that these vertices are very "central", and things in the center have more room to spread out and burn the rest of the graph, whereas choosing something in the "corner" (loosely speaking) leads to some potential spread being blocked off very early on.

### "Closeness"

Very similar to the above (with similar rationale), but with closeness centrality.

### "Far From"

Initially, pick a random vertex. Then, pick the unburned vertex that's furthest away from any of this player's other vertices, only travelling through unburned vertices.

This is designed to minimise the amount of overlap between each cluster of vertices burned, since each burn spreads as far as possible before encountering another cluster of vertices of the same colour.