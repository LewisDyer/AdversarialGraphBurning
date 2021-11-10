import networkx as nx
import matplotlib.pyplot as plt
import json

def count_clusters(caterpillar):
    # given a reduced caterpillar bitstring, use the algorithm to construct the maximum number of clusters that red can attain.

    # STEPS

    # Split the bitstring into substrings of length 3 (plus remainder), and construct the part of the graph for each substring using the partition tables.

    # Combine each of these parts together to make the final DAG, keeping in mind the restrictions at the start/end of the bitstring.

    # Find the longest weighted path from start to finish in the DAG.
    
    if not validate_string(caterpillar):
        print("Invalid bitstring")
        return None

    with open("code\partition_tables.json", "r") as table:
        part_data = table.read() 
        
    part_table = json.loads(part_data)
    
    # split into chunks
    pieces = [caterpillar[i:i+3] for i in range(0, len(caterpillar), 3)]
    subgraphs = [read_from_partition(p, part_table, 2*i+1) for i, p in enumerate(pieces)]

    full_dag = combine_graphs(pieces, subgraphs)

    print(f"Graph {caterpillar}:")
    print(nx.dag_longest_path(full_dag))
    print(nx.dag_longest_path_length(full_dag))
    
    return nx.dag_longest_path_length(full_dag)

def validate_string(bitstring):
    # check if a bitstring is a reduced caterpillar string
    for char in bitstring:
        if char not in ["0", "1"]:
            print("not a bitstring character")
            return False
    if bitstring[0] != "0" or bitstring[-1] != "0":
        print("start or end not right")
        return False
    
    return True
    
def read_from_partition(bitstring, part_table, cl):
    # given a bitstring, return the weighted directed graph from the partition tables.
    G = nx.DiGraph()
    
    G.add_nodes_from([f"RW_start_{bitstring}_{cl}", f"BW_start_{bitstring}_{cl}", f"R_start_{bitstring}_{cl}", f"B_start_{bitstring}_{cl}"], layer=cl)

    G.add_nodes_from([f"RW_end_{bitstring}_{cl+1}", f"BW_end_{bitstring}_{cl+1}", f"R_end_{bitstring}_{cl+1}", f"B_end_{bitstring}_{cl+1}"], layer=cl+1)

    print(G.nodes)

    for start in ["RW", "BW", "R", "B"]:
        for end in ["RW", "BW", "R", "B"]:
            clusters = part_table[bitstring][start][end]
            if clusters != "NA":
                G.add_edge(f"{start}_start_{bitstring}_{cl}", f"{end}_end_{bitstring}_{cl+1}", weight=clusters)
    
    print("about to draw the graph...")
    pos = nx.bipartite_layout(G, [f"RW_start_{bitstring}_{cl}", f"BW_start_{bitstring}_{cl}", f"R_start_{bitstring}_{cl}", f"B_start_{bitstring}_{cl}"])
    return(G)

def combine_graphs(pieces, subgraphs):
    # Combine together to get the full DAG

    # modify first graph, remove all vertices except BW and add a source vertex
    bit = pieces[0]
    first_graph = subgraphs[0]

    # it's not possible to have one node coloured at the start, and a red at the start will introduce a new cluster so we treat it as BW
    first_graph.remove_nodes_from([f"RW_start_{bit}_1", f"R_start_{bit}_1", f"B_start_{bit}_1"])

    first_graph.add_node("START", layer=0)
    first_graph.add_edge("START", f"BW_start_{bit}_1", weight=0)
    subgraphs[0] = first_graph

    # modify the last graph, add a sink vertex at the end
    # I *could* prune the graph at the end, I think, but I don't need to
    bit = pieces[-1]
    last_graph = subgraphs[-1]

    fl = 2*len(subgraphs)

    last_graph.add_node("END", layer=fl+1)
    for n in [f"RW_end_{bit}_{fl}", f"BW_end_{bit}_{fl}", f"R_end_{bit}_{fl}", f"B_end_{bit}_{fl}"]:
        last_graph.add_edge(n, "END", weight=0)
    
    subgraphs[-1] = last_graph

    """
    pos = nx.multipartite_layout(subgraphs[-1], subset_key="layer")
    nx.draw(subgraphs[-1], pos, with_labels=True)
    plt.show()

    bit = pieces[0]
    pos = nx.multipartite_layout(subgraphs[0], subset_key="layer")
    nx.draw(subgraphs[0], pos, with_labels=True)
    plt.show()
    """

    full_graph = subgraphs[0].copy()

    bit_pairs = list(zip(pieces, pieces[1:]))
    subgraph_pairs = list(zip(subgraphs, subgraphs[1:]))

    print(bit_pairs)
    print(subgraph_pairs)
    for i in range(len(bit_pairs)):
        bits, sgs = bit_pairs[i], subgraph_pairs[i]
        print(sgs[1].nodes())
        for node in sgs[1].nodes():
            full_graph.add_node(node, layer=sgs[1].nodes[node]["layer"]-(i+1))
        for edge in sgs[1].edges:
            full_graph.add_edge(edge[0], edge[1], weight=sgs[1].edges[edge]["weight"])
        for edge_type in ["RW", "BW", "R", "B"]:
            first_layer = 2*(i+1)
            start_node = f"{edge_type}_end_{bits[0]}_{first_layer}"
            end_node = f"{edge_type}_start_{bits[1]}_{first_layer+1}"
            nx.contracted_nodes(full_graph, start_node, end_node, copy=False)

    print(len(full_graph.nodes))
    print("=====")
    nodes = list(full_graph.nodes)
    for n in nodes:
        if full_graph.in_degree(n) == 0 and n != "START":
            full_graph.remove_node(n)

    pos = nx.multipartite_layout(full_graph, subset_key="layer")
    nx.draw(full_graph, pos, with_labels=True)
    plt.show()

    return(full_graph)

if __name__ == '__main__':
    # 01011100
    count_clusters("00111010")
