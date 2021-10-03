import networkx as nx
import random

def random_burn(unburned):
    # A basic random strategy: Given a list of unburned vertices, just pick one randomly!
    return random.choice(unburned)