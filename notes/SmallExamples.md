## Small examples of cluster counting

This document aims to demonstrate some very small examples for considering upper and lower bounds for counting the number of monochromatic components on particular classes of graphs.

Note by convention that, where possible, we only care about the number of clusters for red, not for blue.

### Complete graphs, K_n

Fewest clusters: 1 each
Attained when: Both players choose the same vertex to burn (everything is green)

Most clusters: 1 each
Attained when: Both players choose different vertices to burn (everything is green apart from the initial choices)

Comment: Since green nodes count as red and blue, the choice of vertices doesn't matter here, and there will always be one cluster per player.

### Wheel graph, W_n

Each player always gets one cluster. A few cases to check (one middle, both middle, both outer).

Comment: It seems like having a highly connected component like that reduces the number of clusters overall.

### Path graph, P_n

P_1: 1-1 red clusters (only 1 vertex)
P_2: 1-1 red clusters (both adjacent)
P_3: 1-1 red clusters (can get to 2 rounds, but RBR not possible)
P_4: 1-2 red clusters (RRRB in 1 round for lower, RBBG in 2 rounds for upper)
P_5: 1-2 red clusters (BRRRR in 2 rounds for lower, RBBBR in 2 rounds for upper)
P_6: 1-2 (RRRBBB in 2, RBBBBR in 2)
P_7: 1-3 (RRRGBBB in 2, RBBRBBR in 3)


Overall:

Minimum is always 1 (red starts from left, blue starts from right keep travelling until you reach the other colour)

Maximum seems to be ceiling(n/3)

Showing how to do this isn't very hard (the sequence RBB can be replicated ad finitum, though it might end in a G/RB if it's not a multiple of 3). But to prove it I need to show I can't fit any more.


BETTER PROOF:

Suppose the number of red clusters in P_n is greater than ceiling(n/3). Then the number of red vertices in P_n must be greater than ceiling(n/3), hence greater than n/3. So there must exist 3 consecutive vertices such that R is contained twice. Two cases:

* There are two consecutive red vertices: Adding a new red vertex in this way doesn't lead to any new clusters.
* The red vertices are separated by a blue vertex (RBR). Then at least one of the Rs must be adjacent to another R - you can't get the sequence BRBRB. So it doesn't add anything to the cluster count.

FORMALISED:

Given a path on n vertices, consider the sequence of partitions of vertices of length 3 (the last one may be shorter than length 3). There are ceiling(n/3) partitions, and we claim that the number of possible clusters is equal to the number of partitions.

partitions >= clusters:

Firstly, consider the following burning sequence: ((v1, v2), (v4, v5), (v7, v8), ...). Each round burns one partition completely, with the first vertex being red and the remaining two being blue. (edge case: if final partition of length 1, it's green but doesn't change anything). the sequence RBBRBBRBB... contains one red vertex per partition, and no red node is adjacent to any other, so there are ceiling(n-1) clusters.

clusters <= partitions:

Now suppose there are more clusters than partitions. Then one partition must contain at least two red vertices. [and must be a full length one]. If they're adjacent, this partition still only contains 1 cluster. If they're not adjacent, then at least one neighbouring vertex to the partition must be red, since BRBRB (or RBRB) are both impossible to attain. So no new clusters are created. 













PROOF: In general, creating n clusters requires at least n rounds of play, since spreading fires cannot create any new clusters (though it may remove some clusters by combining existing ones).

If there is more than 1 vertex available, at least two vertices must be burned per round. But if 2 vertices are burned in a round, at least 4 must be burned in the previous round (claim unproved for now!).

Therefore, at least 3 vertices are burned per round on average, so the number of rounds is at most ceiling(n/3), and moreover this bound is tight by the RBB-construction.

Proof of Claim: If two vertices are burned this round, there's two cases in which this can occur:

1. The path is fully burned, except for two isolated unburned vertices. 
2. The path is fully burned, except for two connected unburned vertices.

For case 1: The vertices on either side of each unburned vertex must have been burned in the previous round. If neither of them are on the end, we're done. If they're both on ends, since the inner-adjacent vertices were burned last round but it didn't spread, 2 in must have burned as well. (if those match it's P_5).
If one's on an end and one isn't, if they're distance more than 2 apart we're done. If they're distance 2 apart,can't have a single vertex in the middle burned so contradiction. Case proven, at least 4 vertices burned.

For case 2: If it doesn't touch the ends, very similar reasoning to case 1. If it's against one of the ends of the path, the only way you can burn 2 vertices in the previous round is if they're both green, so the last round didn't create a new cluster.