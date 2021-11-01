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

