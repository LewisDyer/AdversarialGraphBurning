# Adversarial Graph Burning - Definition

Throughout, let G be a finite, simple, undirected graph.

Adversarial Graph Burning (or AGB for short) is a discrete-time graph process for two players, and we say that vertices can either be:
* Unburned
* Burned by Player 1
* Burned by Player 2
* Burned by _both_ players

At t=0, all vertices are unburned. At each time t >= 1, each player simultaneously chooses one unburned vertex to burn. If a vertex is burned in round t, in round t+1 each of its unburned neighbours is burned with the same type of burn. The process ends when all vertices are burned. Once a vertex is burned, its burn type cannot be changed in future rounds.

In particular, vertices may be burned by more than one other vertex simultaneously, and players may simultaneously choose the same vertex to burn. In case of conflict, the following rules apply:

* If a vertex is burned by multiple vertices, all of the same type of burn, the vertex is also burned with the same type of burn.
* If a vertex is burned by multiple vertices, including vertices burned by Player 1 and PLayer 2 (type II and III above), the vertex is considered to be burned by _both_ players.
* If a vertex is burned by multiple vertices, some of which are burned by _both_ players and some of which are burned by Player 1 OR Player 2 (but not both), the vertex is considered to be burned by Player 1 OR Player 2, respectively.