import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def game_of_thrones():
    # Return a network of characters from Game of Thrones
    # adapted from https://pyvis.readthedocs.io/en/latest/tutorial.html#example-visualizing-a-game-of-thrones-character-network
    got_data = pd.read_csv('https://www.macalester.edu/~abeverid/data/stormofswords.csv')
    
    sources = got_data['Source']
    targets = got_data['Target']

    edges = zip(sources, targets)
    got_graph = nx.Graph()

    people = {}
    for pair in edges:
        end1 = pair[0]
        end2 = pair[1]

        got_graph.add_node(end1)
        got_graph.add_node(end2)

        got_graph.add_edge(end1, end2)
    
    return got_graph

def powerlaw(n):
    # return a graph on n vertices created using a powerlaw sequence with the Havel-Hakimi algorithm.
    seq = [int(n) for n in powerlaw_sequence(200)]
    while not nx.is_graphical(seq):
        seq = [int(n) for n in powerlaw_sequence(200)]
    G = nx.havel_hakimi_graph(seq)
    return G