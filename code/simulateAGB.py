import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import animation as anim
from enum import Enum
from PIL import Image
import time, os
import burn_strategies as burns

class BurnType(Enum):
    NONE = 0
    P1_ONLY = 1
    P2_ONLY = 2
    BOTH = 3

class NodesOverTime:
    def __init__(self, G):
        self.p1_nodes = [0]
        self.ne_nodes = [0]
        self.p2_nodes = [0]
        self.un_nodes = [G.number_of_nodes()]
    
    def update(self, G):
        self.p1_nodes.append(len(all_burn(G, BurnType.P1_ONLY)))
        self.ne_nodes.append(len(all_burn(G, BurnType.BOTH)))
        self.p2_nodes.append(len(all_burn(G, BurnType.P2_ONLY)))
        self.un_nodes.append(len(all_burn(G, BurnType.NONE)))

    def output(self):
        return [self.p1_nodes, self.ne_nodes, self.p2_nodes, self.un_nodes]

class Experiment:
    
    def __init__(self):
        self.trials = []
    
    def add_trial(self, trial):
        self.trials.append(trial)
    
    def get_no_trials(self):
        return len(self.trials)
    
    def csv_titles(self):
        # return string giving title of each heading, for a csv file
        return "No. nodes,P1 nodes,Neutral nodes,P2 nodes,P1 score,P2 score,P1 clusters,P2 clusters"
    
    def output_csv(self, filename):
        with open(filename, 'w') as results_file:
            results_file.write(self.csv_titles()+"\n")
            for trial in self.trials:
                results_file.write(trial.csv_trial() + "\n")

class TrialResult:

    def __init__(self, G):
        self.no_nodes = G.number_of_nodes()
        self.p1_nodes = len(all_burn(G, BurnType.P1_ONLY))
        self.ne_nodes = len(all_burn(G, BurnType.BOTH))
        self.p2_nodes = len(all_burn(G, BurnType.P2_ONLY))

        self.p1_score = self.p1_nodes + 0.5*self.ne_nodes
        self.p2_score = self.p2_nodes + 0.5*self.ne_nodes

        self.p1_clusters = count_clusters(G, 1)
        self.p2_clusters = count_clusters(G, 2)
    
    def __str__(self):
        output = []
        output.append(f"Number of nodes: {self.no_nodes}")
        output.append(f"Number of P1 nodes: {self.p1_nodes}")
        output.append(f"Number of neutral nodes: {self.ne_nodes}")
        output.append(f"Number of P2 nodes: {self.p2_nodes}")
        output.append(f"Player 1 score: {self.p1_score}")
        output.append(f"Player 2 score: {self.p2_score}")
        output.append(f"Player 1 clusters: {self.p1_clusters}")
        output.append(f"Player 2 clusters: {self.p2_clusters}")

        return "\n".join(output)
    
    def csv_trial(self):
        return f"{self.no_nodes},{self.p1_nodes},{self.ne_nodes},{self.p2_nodes},{self.p1_score},{self.p2_score},{self.p1_clusters},{self.p2_clusters}"

def simulate():
    # Main function, run this to simulate AGB

    G = build_graph()

    new_burns = set()

    default_attrs = {node:{"current_burn": BurnType.NONE, "prospective_burns":set()} for node in G.nodes()}

    nx.set_node_attributes(G, values=default_attrs)

    images = []
    round_no=1
    draw_images = False
    show_progress = False

    node_counts = NodesOverTime(G)
    
    while still_to_burn(G):
        #print("still to burn")
        p1_burn = player_1_burn(G)
        p2_burn = player_2_burn(G)
        #print(f"DEBUG: P1 picks {p1_burn}")
        #print(f"DEBUG: P2 picks {p2_burn}")
        nodes_to_resolve = spread_burn(G, p1_burn, p2_burn, new_burns)
        #print(nodes_to_resolve)
        resolve_conflicts(G, nodes_to_resolve)
        new_burns = nodes_to_resolve
        
        if(draw_images):
            save_image(G, images, round_no)
            plt.clf()

        node_counts.update(G)

        round_no += 1
    
    if(draw_images):
        filename = "test"
        images.extend([images[-1]]*5) # add 5 copies of last image so it pauses on the final result a bit longer
        make_gif(images, filename)
        plt.clf()
    if(show_progress):
        progress_graph(G, node_counts)

    return logging(G, True)

def expers(runs):

    exp = Experiment()
    for run in range(runs):
        result = simulate()
        exp.add_trial(result)
    
    exp.output_csv("test_experiment_degree_random_50.csv")

def build_graph():
    # Make a graph to burn over
    return nx.grid_2d_graph(50, 50)

def all_burn(G, burn_type):
    # Given a graph, returns a list of all nodes with a given burn type
    this_burn = []
    for n in G.nodes():
        if G.nodes[n]['current_burn'] == burn_type:
            this_burn.append(n)
    
    return(this_burn)

def player_1_burn(G):
    # Player 1's strategy for picking a vertex to burn
    return burns.degree_burn(G)

def player_2_burn(G):
    # Player 2's strategy for picking a vertex to burn
    return burns.random_burn(G)

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
    filename = f"{int(time.time())}_{frame_no}.jpg"
    plt.savefig(filename)
    img = Image.open(filename)
    images.append(img)
    
def make_gif(images, filename):
    images[0].save(f"{filename}.gif", save_all=True, append_images=images[1:], optimize=False, duration=100, loop=0)

def logging(G, print_logs):
    # print out logging info about the process which has just terminated.

    trial = TrialResult(G)
    if print_logs:
        print(trial)
    return trial

def count_clusters(G, player_no):
    if player_no == 1:
        vertices = all_burn(G, BurnType.P1_ONLY) + all_burn(G, BurnType.BOTH)
    elif player_no == 2:
        vertices = all_burn(G, BurnType.P2_ONLY) + all_burn(G, BurnType.BOTH)
    else:
        return None # invalid player number
    
    SG = G.subgraph(vertices)
    return nx.number_connected_components(SG)

def progress_graph(G, node_counts):
    rounds = len(node_counts.output()[1])
    
    for count in node_counts.output():
        plt.plot(range(rounds), count)
    
    plt.legend(["Player 1 nodes", "Both nodes", "Player 2 nodes", "Unburned nodes"])
    plt.xlabel("Round number")
    plt.ylabel("Number of vertices")
    plt.show()

expers(1000)