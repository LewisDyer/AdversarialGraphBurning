import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation as anim

def simulate():
    # Main function, run this to simulate AGB

    G = build_graph()

    while still_to_burn():
        player_1_burn()
        player_2_burn()
        spread_burn()
        resolve_conflicts()

    output()


def build_graph():
    # Make a graph to burn over
    return nx.path_graph(10)

def player_1_burn():
    # Player 1's strategy for picking a vertex to burn
    pass

def player_2_burn():
    # Player 2's strategy for picking a vertex to burn
    pass

def spread_burn():
    # Spread the fire for vertices which have been newly burned
    # Both players' picks + where the spread occurred last time
    pass

def still_to_burn():
    # Are there any unburned vertices remaining?
    pass

def resolve_conflicts():
    # Deal with any multiple-burn scenarios and update the final graph
    pass

def output():
    # Give the visualisation and logging results
    pass

simulate()