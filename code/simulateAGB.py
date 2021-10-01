import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation as anim
from enum import Enum
from PIL import Image
import random, time, os

class BurnType(Enum):
    NONE = 0
    P1_ONLY = 1
    P2_ONLY = 2
    BOTH = 3

def simulate():
    # Main function, run this to simulate AGB

    G = build_graph()

    new_burns = set()

    default_attrs = {node:{"current_burn": BurnType.NONE, "prospective_burns":set()} for node in G.nodes()}

    nx.set_node_attributes(G, values=default_attrs)

    images = []
    frame_no=0

    while still_to_burn(G):
        #print("still to burn")
        p1_burn = player_1_burn(G)
        p2_burn = player_2_burn(G)
        nodes_to_resolve = spread_burn(G, p1_burn, p2_burn, new_burns)
        #print(nodes_to_resolve)
        resolve_conflicts(G, nodes_to_resolve)
        new_burns = nodes_to_resolve

        save_image(G, images, frame_no)
        frame_no += 1
    
    filename = "test"
    make_gif(images, filename)
    logging(G)


def build_graph():
    # Make a graph to burn over
    return nx.hexagonal_lattice_graph(5, 5)

def all_burn(G, burn_type):
    # Given a graph, returns a list of all nodes with a given burn type
    this_burn = []
    for n in G.nodes():
        if G.nodes[n]['current_burn'] == burn_type:
            this_burn.append(n)
    
    return(this_burn)

def player_1_burn(G):
    # Player 1's strategy for picking a vertex to burn
    return random_burn(all_burn(G, BurnType.NONE))

def player_2_burn(G):
    # Player 2's strategy for picking a vertex to burn
    return random_burn(all_burn(G, BurnType.NONE))

def random_burn(unburned):
    # A basic random strategy: Given a list of unburned vertices, just pick one randomly!
    return random.choice(unburned)

def spread_burn(G, p1_burn, p2_burn, new_burns):
    # Spread the fire for vertices which have been newly burned
    # Both players' picks + where the spread occurred last time
    #print(f"DEBUG: player 1 picks {p1_burn}")
    #print(f"DEBUG: player 2 picks {p2_burn}")
    # We can resolve these burns immediately
    if p1_burn == p2_burn:
        G.nodes[p1_burn]["current_burn"] = BurnType.BOTH
    else:
        G.nodes[p1_burn]["current_burn"] = BurnType.P1_ONLY
        G.nodes[p2_burn]["current_burn"] = BurnType.P2_ONLY

    new_burns.add(p1_burn)
    new_burns.add(p2_burn)

    unburned = all_burn(G, BurnType.NONE)
    nodes_to_resolve = set()

    for node_to_burn in new_burns:
        fire_type = G.nodes[node_to_burn]["current_burn"]
        # spread the fire from each newly burned node to its unburned neighbours
        for next_node in G.neighbors(node_to_burn):
            if next_node in unburned:
                #print(f"DEBUG: {node_to_burn} spreads {fire_type} to {next_node}")
                G.nodes[next_node]["prospective_burns"].add(fire_type)
                nodes_to_resolve.add(next_node)
    
    return nodes_to_resolve


def still_to_burn(G):
    # Are there any unburned vertices remaining?
    return (all_burn(G, BurnType.NONE) != [])

def resolve_conflicts(G, nodes_to_resolve):
    # Deal with any multiple-burn scenarios and update the final graph
    for resolve in nodes_to_resolve:
        burn_types = G.nodes[resolve]["prospective_burns"]
        #print(f"DEBUG: Burn types of {resolve} are {burn_types}")

        ## IMPORTANT: Main section for handling burn type conflicts
        if BurnType.P1_ONLY in burn_types and BurnType.P2_ONLY in burn_types:
            # the different fire types lead to conflict
            G.nodes[resolve]["current_burn"] = BurnType.BOTH
        elif BurnType.P1_ONLY in burn_types and BurnType.BOTH in burn_types:
            # the singular fire type takes priority
            G.nodes[resolve]["current_burn"] = BurnType.P1_ONLY
        elif BurnType.P2_ONLY in burn_types and BurnType.BOTH in burn_types:
            G.nodes[resolve]["current_burn"] = BurnType.P2_ONLY
        else: # there can only be one burn type left! Just take that one
            G.nodes[resolve]["current_burn"] = next(iter(burn_types))


def save_image(G, images, frame_no):
    # Give the visualisation and logging results

    colour_map = {BurnType.NONE: 'gray', BurnType.P1_ONLY: 'red', BurnType.P2_ONLY: 'blue', BurnType.BOTH: 'green'}

    pos = nx.kamada_kawai_layout(G) # fixes the layout of the graph, maintaining consistency with each step

    node_colours = [colour_map[G.nodes[node]["current_burn"]] for node in G]

    nx.draw(G, pos, with_labels=True, node_color=node_colours)
    # saving to a file like this is a bodge, but it'll do since this is just to help me visualise things
    filename = f"{int(time.time())}_{frame_no}.png"
    plt.savefig(filename)
    img = Image.open(filename)
    images.append(img)
    

def make_gif(images, filename):
    images[0].save(f"{filename}.gif", save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)

def logging(G):
    # print out logging info about the process which has just terminated.

    print(f"Number of nodes: {G.number_of_nodes()}")
    print(f"Player 1 score: {len(all_burn(G, BurnType.P1_ONLY)) + 0.5*len(all_burn(G, BurnType.BOTH))}")
    print(f"Player 2 score: {len(all_burn(G, BurnType.P2_ONLY)) + 0.5*len(all_burn(G, BurnType.BOTH))}")
    
    print(f"Number of P1 nodes: {len(all_burn(G, BurnType.P1_ONLY))}")
    print(f"Number of neutral nodes: {len(all_burn(G, BurnType.BOTH))}")
    print(f"Number of P2 nodes: {len(all_burn(G, BurnType.P2_ONLY))}")
    
simulate()