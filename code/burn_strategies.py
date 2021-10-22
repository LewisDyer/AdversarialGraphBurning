import networkx as nx
import random
from simulateAGB import all_burn, BurnType
import math

def random_burn(G):
    # A basic random strategy: just pick a random vertex.
    unburned = all_burn(G, BurnType.NONE)
    return random.choice(unburned)

def degree_burn(G):
    # Slightly more involved: take the subgraph of unburned vertices, and pick the vertex of highest degree. If there are multiple of highest degree, pick any of them randomly.
    unburned = all_burn(G, BurnType.NONE)
    SG = G.subgraph(unburned)

    all_degrees = sorted(SG.degree, key=lambda x: x[1], reverse=True)

    max_degree = all_degrees[0][1] # get the actual highest degree
    highest_degrees = [node[0] for node in all_degrees if node[1] == max_degree] # get all vertices of highest degree
    return random.choice(highest_degrees) # pick a random one!

def between_burn(G):
    # Select the unburned node with the highest betweeness centrality
    unburned = all_burn(G, BurnType.NONE)

    SG = G.subgraph(unburned)

    betweens = list(nx.betweenness_centrality(SG, normalized=False).items())

    all_betweens = sorted(betweens, key=lambda x: x[1], reverse=True)
    unb_betweens = [node for node in all_betweens if node[0] in unburned]

    max_between = unb_betweens[0][1]
    highest_betweens = [node[0] for node in unb_betweens if node[1] == max_between]
    return random.choice(highest_betweens)

def closeness_burn(G):
    # Select the unburned node with the highest closeness centrality
    unburned = all_burn(G, BurnType.NONE)

    SG = G.subgraph(unburned)

    closeness = list(nx.closeness_centrality(SG).items())

    all_closeness = sorted(closeness, key=lambda x: x[1], reverse=True)
    unb_closeness = [node for node in all_closeness if node[0] in unburned]

    max_closeness = unb_closeness[0][1]
    highest_closeness = [node[0] for node in unb_closeness if node[1] == max_closeness]
    return random.choice(highest_closeness)

def far_from_own(G, player_no):
    # Returns the node that's furthest away from another node of the player's own colour.
    if player_no == 1:
        own_vertices = all_burn(G, BurnType.P1_ONLY) + all_burn(G, BurnType.BOTH)
    elif player_no == 2:
        own_vertices = all_burn(G, BurnType.P2_ONLY) + all_burn(G, BurnType.BOTH)
    else:
        return None # invalid player number
    
    unburned = all_burn(G, BurnType.NONE)
    most_isolated_dist = 0
    most_isolated_nodes = []
    # checks all unburned/own pairs, quite inefficient especially midway through
    # could switch to expanding balls at all unburned vertices until an owned vertex is found
    for start in unburned:
        furthest_dist = math.inf
        for dest in own_vertices:
            try:
                dist = nx.shortest_path_length(G, start, dest)
            except:
                dist = math.inf
            if dist < furthest_dist:
                furthest_dist = dist
        if furthest_dist == most_isolated_dist:
            most_isolated_nodes.append(start)
        elif furthest_dist > most_isolated_dist:
            most_isolated_dist = furthest_dist
            most_isolated_nodes = [start]
    return random.choice(most_isolated_nodes)