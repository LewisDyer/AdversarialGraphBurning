import networkx as nx
import random
import simulateAGB as sim

def random_burn(G):
    # A basic random strategy: just pick a random vertex.
    unburned = sim.all_burn(G, sim.BurnType.NONE)
    return random.choice(unburned)

def degree_burn(G):
    # Slightly more involved: take the subgraph of unburned vertices, and pick the vertex of highest degree. If there are multiple of highest degree, pick any of them randomly.
    unburned = sim.all_burn(G, sim.BurnType.NONE)
    SG = G.subgraph(unburned)

    all_degrees = sorted(SG.degree, key=lambda x: x[1], reverse=True)

    max_degree = all_degrees[0][1] # get the actual highest degree
    highest_degrees = [node[0] for node in all_degrees if node[1] == max_degree] # get all vertices of highest degree
    return random.choice(highest_degrees) # pick a random one!

def between_burn(G):
    # Select the unburned node with the highest betweeness centrality
    unburned = sim.all_burn(G, sim.BurnType.NONE)

    betweens = list(nx.betweenness_centrality(G, normalized=False).items())

    all_betweens = sorted(betweens, key=lambda x: x[1], reverse=True)
    unb_betweens = [node for node in all_betweens if node[0] in unburned]

    max_between = unb_betweens[0][1]
    highest_betweens = [node[0] for node in unb_betweens if node[1] == max_between]
    return random.choice(highest_betweens)

