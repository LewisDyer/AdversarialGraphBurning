We'll describe caterpillars using a tuple,

(x1, x2, ..., xn), where x_i is the number of leaves on path vertex i. In particular:

* For the purposes of cluster counting, having more than 2 leaves doesn't make a difference, so 0 <= x_i <= 2 for all i.
* The x_is can be chosen such that x1 = xn = 0 (if they have a leaf, that can be put as an endpoint)

Hence, the total number of caterpillar graphs on k path vertices is 3^(k-2) for k >= 3 and 1 for k either 1 or 2.

4 path vertices:

(0,0,0,0): 2 (path)
(0,0,1,0) 2 (same construction as path colouring)
(0,1,1,0): 2 (again same idea)
(0,0,2,0): 2 (same issue, not enough room to maneuver...)
(0,2,2,0): 2 ()

conjecture: always 2

5 path vertices:

(0, 2, 2, 2, 0): 3


# Lemma

Given a caterpillar tuple, you can replace all 2s with 1s and get the same maximum number of clusters.

# Proof of lemma

Essentially, you can merge the two leaves such that they're red if 1 of them is red. You can do this because there's no way to have both of those leaves be red unless their common path vertex is also red (so it's only 1 cluster). Since you'd need to burn each of these by picking, and you can't do both in the same round since the common path vertex will spread to one of the leaves.

So only need to consider 2^(n-2) trees - treat these as bitstrings starting and ending with 0.

00010010

## BOUNDS

As an aside, adding more leaves to new nodes is monotonic in cluster count, since you can simulate the effect of having no leaves by just burning the path vertex, which will get the leaf later.

For a path vertex of length n (for n > 3):

Lower bound: ceiling(n/3). This is (0,0,...,0), the path on n vertices.

Upper bound: This is for (0,1,...,1,0), the caterpiller graph where every non-end path vertex has 1 leaf. ceiling((2n-2)/3)

It's a repeating pattern where you burn red 2 leaves then burn the next one blue, so it acts like a barrier and you can reset the cycle. 2 clusters every 3 path vertices on average
(note however that this has 2n-2 vertices, so it doesn't break path extremity)

Note: for this pattern, better to burn the very first vertex red, then the first leaf blue and proceed like that - this just helps generalise this method to all caterpillar graphs.

## Proof Idea

I think that this proof is going to be algorithmic in nature: Rather than a formula, I'll provide an algorithm that will show you how to colour a given caterpillar graph.

First off, I need to find a way to partition a reduced caterpillar graph into several caterpillar graphs, then find the optimal way to colour each of these pieces. Note this might give me a bound rather than an exact result, but it's a strong start.

## The partitions

Remark: For any caterpillar tree, if it begins with a 1, I can replace it with two 0s to get the exact same graph.