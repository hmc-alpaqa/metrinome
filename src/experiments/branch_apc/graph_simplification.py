from collections import defaultdict
import networkx as nx


def convert_dict_to_string_keys(graph):
    converted_graph = defaultdict(list)

    for key, values in graph.items():
        new_key = '0_' + str(key)
        new_values = ['0_' + str(value) for value in values]
        converted_graph[new_key] = new_values

    return converted_graph


def remove_prefix(graph_with_prefix):
    converted_graph = defaultdict(list)

    for key, values in graph_with_prefix.items():
        new_key = int(key.split('_')[1])
        new_values = [int(value.split('_')[1]) for value in values]
        converted_graph[new_key] = new_values

    return converted_graph


def simplify_graphs(dictgraphs, calldict):
    '''
    Convert edge APC to branch APC

    Basic Rules:
    1. A -> B -> C gets simplified to A -> C
    '''
    simplified_graphs = []

    for graph in dictgraphs:
        G = nx.MultiDiGraph(graph)

        change_made = True
        while change_made:
            change_made = False
            # if in degree == 1 or out degree == 1: remove node, reconnect other edges
            for node in list(G.nodes):
                # keep first node
                if node.split('_')[1] == '0' or node in calldict:
                    continue

                if G.in_degree(node) == 1 and G.out_degree(node) > 0:
                    prev_node = list(G.predecessors(node))[0]
                    next_nodes = list(G.successors(node))
                    # add edges
                    for next_node in next_nodes:
                        for _ in range(G.number_of_edges(node, next_node)):
                            G.add_edge(prev_node, next_node)
                    G.remove_node(node)
                    change_made = True
                    continue

                if G.out_degree(node) == 1:
                    prev_nodes = list(G.predecessors(node))
                    next_node = list(G.successors(node))[0]
                    # add edges
                    for prev_node in prev_nodes:
                        for _ in range(G.number_of_edges(prev_node, node)):
                            G.add_edge(prev_node, next_node)
                    G.remove_node(node)
                    change_made = True
                    continue

        # convert to adjacency list
        adj_list = defaultdict(list)
        for edge in G.edges:
            adj_list[edge[0]].append(edge[1])

        simplified_graphs.append(adj_list)

    return (simplified_graphs, calldict)
