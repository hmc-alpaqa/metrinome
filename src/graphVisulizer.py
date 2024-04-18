# %%
from collections import defaultdict
import graphviz

calldict = defaultdict(list)

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
        incoming = defaultdict(list)  # graph but all the arrows are flipped
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                incoming[neighbor].append(node)

        for node in list(graph.keys()):
            if node.split('_')[1] == '0':  # keep first node
                continue  # remove this node, fix connection
            if node not in calldict and len(incoming[node]) == 1 and len(graph[node]) == 1:
                prev_node = incoming[node][0]
                next_node = graph[node][0]
                # remove prev node's connection to node
                graph[prev_node].remove(node)
                graph[prev_node].append(next_node)  # connect prev to next node
                # update incoming graph (same thing as above)
                incoming[next_node].remove(node)
                incoming[next_node].append(prev_node)
                del graph[node]
                del incoming[node]
        simplified_graphs.append(graph)
    return (simplified_graphs, calldict)

def viz_graph(graph, calldict):
    dot = graphviz.Digraph(format='png')
    # Add nodes to the graph
    for node in graph:
        dot.node(node)
    # Add edges to the graph
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            dot.edge(node, neighbor)
    # Add call edges to the graph
    for node, neighbors in calldict.items():
        for neighbor in neighbors:
            dot.edge(node, f'{neighbor}_0', style='dashed')
    # render file
    dot.render('b')

if __name__ == '__main__':
    calldict = defaultdict(list, {'0_6': [1], '0_8': [1]})
    dictgraphs = [
        defaultdict(list, {
            '0_0': ['0_1'],
            '0_1': ['0_2', '0_4'],
            '0_2': ['0_3'],
            '0_3': ['0_1'],
            '0_4': ['0_5'],
            '0_5': ['0_6', '0_17'],
            '0_6': ['0_7'],
            '0_7': ['0_8', '0_9'],
            '0_8': ['0_7'],
            '0_9': ['0_10'],
            '0_10': ['0_11', '0_16'],
            '0_11': ['0_12', '0_14'],
            '0_12': ['0_13', '0_14'],
            '0_13': ['0_14'],
            '0_14': ['0_15'],
            '0_15': ['0_10'],
            '0_16': ['0_5']
        }),
        defaultdict(list, {
            '1_0': ['1_1'],
            '1_1': ['1_2', '1_6'],
            '1_2': ['1_3', '1_4'],
            '1_3': ['1_4'],
            '1_4': ['1_5'],
            '1_5': ['1_1']
        })
    ]
    # calldict= defaultdict(list, {})
    
    # connect graphs:
    combined_graph = defaultdict(list)
    for graph in dictgraphs:
        combined_graph.update(graph)
    print(dictgraphs)
    viz_graph(combined_graph, calldict)
