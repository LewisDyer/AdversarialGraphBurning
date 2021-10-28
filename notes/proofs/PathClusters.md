theorem: The maximum number of clusters on a path of n vertices is ceiling(n/3)

PROOF: In general, creating n clusters requires at least n rounds of play, since spreading fires cannot create any new clusters (though it may remove some clusters by combining existing ones).

If there is more than 1 vertex available, at least two vertices must be burned per round. But if 2 vertices are burned in a round, at least 4 must be burned in the previous round (claim unproved for now!).

Therefore, at least 3 vertices are burned per round on average, so the number of rounds is at most ceiling(n/3), and moreover this bound is tight by the RBB-construction.

Proof of Claim: If two vertices are burned this round, there's two cases in which this can occur:

1. The path is fully burned, except for two isolated unburned vertices. 
2. The path is fully burned, except for two connected unburned vertices.

For case 1: The vertices on either side of each unburned vertex must have been burned in the previous round. If neither of them are on the end, we're done. If they're both on ends, since the inner-adjacent vertices were burned last round but it didn't spread, 2 in must have burned as well. (if those match it's P_5).
If one's on an end and one isn't, if they're distance more than 2 apart we're done. If they're distance 2 apart,can't have a single vertex in the middle burned so contradiction. Case proven, at least 4 vertices burned.

For case 2: If it doesn't touch the ends, very similar reasoning to case 1. If it's against one of the ends of the path, the only way you can burn 2 vertices in the previous round is if they're both green, so the last round didn't create a new cluster.