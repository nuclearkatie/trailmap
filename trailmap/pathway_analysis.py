import networkx as nx
import matplotlib.pyplot as plt
from pprint import pprint
import pygraphviz as pgv
from pprint import pprint


def draw_graph(G):
    pos = nx.drawing.nx_pydot.graphviz_layout(G, prog=dot)

    plt.figure()
    nx.draw_networkx_nodes(G, pos)
    nx.draw_networkx_labels(G, pos)
    nx.draw_networkx_edges(G, pos)

    return


def draw_path(G, path):
    draw_graph(G)
    pos = nx.drawing.nx_pydot.graphviz_layout(G)
    nx.draw_networkx_nodes(G, pos=pos, nodelist=path, node_color="red")
    plt.show()
    return


def print_graph_parameters(G, pathways):
    '''Prints a set of parameters characterizing the graph
    '''
    print('\nGraph parameters')

    print("A total of " + str(len(pathways)) + " pathways were generated")

    (shortest_path, shortest_length,
     longest_length) = get_shortest_and_longest_path(pathways)
    print("The shortest pathway is " + str(shortest_path))
    print("with length " + str(shortest_length))

    print("\nGraph depth is " + str(longest_length))

    semiconnected = nx.is_semiconnected(G)
    print('\nIs the graph semiconnected? ' + str(semiconnected))
    if semiconnected is False:
        print("-->This is likely because you have multiple source facilities")

    hierarchy = nx.flow_hierarchy(G)
    print("\nGraph hierarchy is " + str(hierarchy))

    return


def find_node_disjoint_paths(G, s, t):
    ndp = set()
    if s in G and t in G:
        paths = list(nx.node_disjoint_paths(G, s, t))
        [ndp.add(tuple(path)) for path in paths]

    return ndp


def find_maximum_flow(G, s, t):
    '''Requires edge attribute 'capacity'
    '''
    max_flow_path = maximum_flow(G, s, t)
    max_flow = maximum_flow_value(G, s, t)
    return max_flow_path, max_flow


def find_simple_cycles(G):
    sc = list(nx.simple_cycles(G))
    return sc


def find_facility_specific_paths(pathways, facility, location='any'):
    '''finds pathways that include a given facility. Options: 'beginning',
    'end', 'any' specify whether the facility should be the start, the end, or
    anywhere in the path
    '''
    subset_pathways = []
    for path in pathways:
        if facility in path:
            if location == 'start' and path[0] == facility:
                subset_pathways.append(path)
            elif location == 'end' and path[-1] == facility:
                subset_pathways.append(path)
            else:
                subset_pathways.append(path)

    return subset_pathways


def find_paths_between_facilities(pathways, source, target):
    subset_pathways = []
    for path in (x for x in pathways if x[0] == source and x[-1] == target):
        subset_pathways.append(path)

    return subset_pathways


def find_paths_containing_facilities(pathways, facilities, contains='any'):
    p = []
    if contains == 'any':
        for path in pathways:
            p.append([path for facility in facilities if facility in path])
    if contains == 'all':
        for path in pathways:
            if set(facilities).issubset(path):
                p.append(path)

    return p


def get_shortest_and_longest_path(pathways):
    '''finds the pathway with the shortest number of steps from source to
    target. Returns a tuple with path and length.
    '''
    if len(pathways) is not 0:
        shortest_length = min([len(path) for path in pathways])
        shortest_path = min([path for path in pathways])
        longest_length = max([len(path) for path in pathways])
    else:
        shortest_path = "No pathways found"
        shortest_length = 0

    return shortest_path, shortest_length, longest_length
