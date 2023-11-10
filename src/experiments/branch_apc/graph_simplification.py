# %%
from collections import defaultdict
import networkx as nx
# import graphviz


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

    return (calldict, simplified_graphs)


# def viz_graph(graph, calldict):
#     dot = graphviz.Digraph(format='png')

#     # Add nodes to the graph
#     for node in graph:
#         dot.node(node)

#     # Add edges to the graph
#     for node, neighbors in graph.items():
#         for neighbor in neighbors:
#             dot.edge(node, neighbor)

#     # Add call edges to the graph
#     for node, neighbors in calldict.items():
#         for neighbor in neighbors:
#             dot.edge(node, f'{neighbor}_0', style='dashed')

#     # render file
#     dot.render('b')


if __name__ == '__main__':

    # bubble sort og
    # dictgraphs = [defaultdict(list, {'0_0': ['0_1'], '0_1': ['0_2', '0_4'], '0_2': ['0_3'], '0_3': ['0_1'], '0_4': ['0_5'], '0_5': ['0_6', '0_8'], '0_6': ['0_7'], '0_7': ['0_5'], '0_8': ['0_9'], '0_9': ['0_10', '0_18'], '0_10': ['0_11'], '0_11': [
    #     '0_12', '0_16'], '0_12': ['0_13', '0_14'], '0_13': ['0_14'], '0_14': ['0_15'], '0_15': ['0_11'], '0_16': ['0_17'], '0_17': ['0_9'], '0_18': ['0_19'], '0_19': ['0_20', '0_22'], '0_20': ['0_21'], '0_21': ['0_19']})]

    # is even is odd
    calldict = defaultdict(list, {'0_2': [1], '1_2': [0]})
    dictgraphs = [defaultdict(list, {'0_0': ['0_1', '0_2'], '0_1': ['0_3'], '0_2': [
                              '0_3']}), defaultdict(list, {'1_0': ['1_1', '1_2'], '1_1': ['1_3'], '1_2': ['1_3']})]

    # merge sort
    calldict = defaultdict(list, {'0_2': [1, 2], '1_4': [3]})
    dictgraphs = [defaultdict(list, {'0_0': ['0_1'], '0_1': ['0_2', '0_4'], '0_2': ['0_3'], '0_3': ['0_1']}), defaultdict(list, {'1_0': ['1_1'], '1_1': ['1_2', '1_5'], '1_2': ['1_3', '1_4'], '1_3': ['1_4'], '1_4': ['1_1']}), defaultdict(list, {'2_0': ['2_1'], '2_1': ['2_2', '2_4'], '2_2': ['2_3'], '2_3': ['2_1'], '2_4': ['2_5'], '2_5': [
        '2_6', '2_8'], '2_6': ['2_7'], '2_7': ['2_5']}), defaultdict(list, {'3_0': ['3_1'], '3_1': ['3_2', '3_3'], '3_2': ['3_3'], '3_3': ['3_4', '3_8'], '3_4': ['3_5', '3_6'], '3_5': ['3_7'], '3_6': ['3_7'], '3_7': ['3_1'], '3_8': ['3_9'], '3_9': ['3_10', '3_11'], '3_10': ['3_9'], '3_11': ['3_12'], '3_12': ['3_13', '3_14'], '3_13': ['3_12']})]
    print(dictgraphs)
    call_dict, simplified_graphs = simplify_graphs(dictgraphs, calldict)

    # connect graphs:
    combined_graph = defaultdict(list)
    for graph in simplified_graphs:
        combined_graph.update(graph)

    print(simplified_graphs)
    viz_graph(combined_graph, calldict)
