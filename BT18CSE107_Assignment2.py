import sys
import heapq
from collections import defaultdict

# Node class
class Node:
    def __init__(self, id=None, parent=None):
        self.id = id
        self.parent = parent

    def __lt__(self, other):
        return self.id < other.id


# class Tree:
#   def __init__(self,node_data = None, unique_id = None, parent_unique_id = None):
#     self.node = node_data
#     self.unique_id = unique_id
#     self.parent_unique_id = parent_unique_id


def adding_new_edge_to_graph(graph, node1, node2, cost):
    """
    Adding a new edge to the graph
    Input Parameters:
        graph : The actual graph (2D Dictionary) :: {'node1' : [(node2, cost2), (node3, cost3), ... ], 'node2' : [ ... ], ...}
        node1 : Source node of the edge (starting point)
        node2 : Destination node of the edge (end point)
        cost  : Cost to travel from node1 to node2
    """

    graph[node1][node2] = cost
    graph[node2][node1] = cost


def min_key_for_mst(node_dict):
    """
    Parameters:
        node_dict : The input dictionary
    Return :
         Returns the key (node) with minimum value
    """
    #     maxsize works as Infinity
    ret_key, min_val = None, sys.maxsize

    for node, val in node_dict.items():
        # print("Here ", node, val)
        if min_val > val[1]:
            min_val = val[1]
            ret_key = node

    return ret_key if ret_key is not None else list(node_dict.keys())[0]


def find_MST(graph, nodes=None):
    """
    Heurestic Function
    Finds the minimum spanning tree of a given graph, considering only unvisited  nodes
    Parameters:
        graph : The actual graph
        nodes : List of nodes to be considered in the MST(unvisted nodes), by default it takes all nodes.
    """
    mstSet = list()
    notMstSet = None
    INFINITY = sys.maxsize

    # Intializing Non MST dictionary :: {node : (source, cost from source to node), ... }
    if nodes is None:  # for all nodes
        notMstSet = {node: (None, INFINITY) for node in graph.keys()}
    else:
        notMstSet = {node: (None, INFINITY) for node in nodes}

    while len(notMstSet) != 0:  # While mstSet doesn’t include all vertices
        # Find the key with minimum value
        min_key = min_key_for_mst(notMstSet)

        # Adding the node to the MST list and removing from Non MST (ret[0] contains the source)
        ret = notMstSet.pop(min_key)
        mstSet.append((ret[0], min_key))

        # Updating the source and cost from source of neighbour nodes of the returned key
        """
        Update key value of all adjacent vertices 
        if weight of current edge is less than the previous key value of neighbour, update the key value as weight
    """
        for neighbour, val in graph[min_key].items():
            if (
                notMstSet.get(neighbour, None) is not None
                and val < notMstSet.get(neighbour)[1]
            ):
                notMstSet[neighbour] = (min_key, val)

    if len(mstSet) > 0:
        mstSet.pop(0)

    return mstSet


def find_optimal_tsp_path(graph):
    """
    Finds the optimal tour (min-cost tour) given the condition that each node has to visited only once
    and end at city from where we have started
    Parameters:
        graph : The actual graph
    Returns:
        The optimal path from start to end (In form of a list)
    """
    fringe_list = []
    # Dummy root node
    root = Node("#", None)
    no_nodes_expanded = 0
    no_nodes_generated = 0

    # Fringe List stores nodes generated and not yet expanded (min-heap implementation) ::
    # [(f-value, g-value, node, parent node(_id)), ... ]
    # Expanded Tree stores expanded nodes in form of a tree :: (node_data, unique_id, parent_unique_id)
    # hash represents no parent node
    # print(list(graph.keys()))
    fringe_list.append((0, 0, list(graph.keys())[0], root))
    # Time complexity of heapify is O(Logn). Time complexity of createAndBuildHeap() is O(n)
    heapq.heapify(fringe_list)

    # Running the loop until an optimal path is found
    while fringe_list:

        # Picking the node with smallest f-value from fringe list
        least_f_value_node = heapq.heappop(fringe_list)
        g_value, node, p_node = (
            least_f_value_node[1],
            least_f_value_node[2],
            least_f_value_node[3],
        )

        # Adding the node to the tree
        # state=[0 for i in range(len(graph))]

        t = Node(node, p_node)
        # Storing all the nodes from root to the current node
        parent_nodes = [node]
        temp = t.parent
        while temp.id != "#":
            parent_nodes.append(temp.id)
            temp = temp.parent
        # If number of collected nodes is the actual total number of nodes, then path has been found, returning it
        """
        Return
        """
        if len(parent_nodes) == len(graph) + 1:
            return (parent_nodes[::-1]), no_nodes_expanded, no_nodes_generated
        else:
            # Otherwise, finding the h-value of the successor nodes via find_MST() function
            # set difference of all nodes and visted nodes
            unvisited_nodes = sorted(
                list(set(graph.keys()).difference(set(parent_nodes)))
            )
            # Call to MST function
            mst_path = find_MST(graph, unvisited_nodes)

            h_value, min_dist_start, min_dist_end = 0, sys.maxsize, sys.maxsize
            # Calculating the MST weight
            # Heurestic value is sum of cost of all paths of Unvisted MST
            for n1, n2 in mst_path:
                if n1 != None and n2 != None:
                    h_value = h_value + graph[n1][n2]

            # Finding shortest distance from start and to end of the already determined path which connect the rest of MST

            for unvisNodes in unvisited_nodes:
                if graph[parent_nodes[0]].get(unvisNodes, None) is not None:
                    min_dist_end = min(min_dist_end, graph[parent_nodes[0]][unvisNodes])

                if parent_nodes[0] != parent_nodes[-1]:
                    if graph[parent_nodes[-1]].get(unvisNodes, None) is not None:
                        min_dist_start = min(
                            min_dist_start, graph[parent_nodes[-1]][unvisNodes]
                        )

                else:  # only one parent node
                    min_dist_start = 0

            if min_dist_start == sys.maxsize:
                min_dist_start = 0

            if min_dist_end == sys.maxsize:
                min_dist_end = 0

            # Calculating Final h-value
            h_value = h_value + min_dist_start + min_dist_end

            # Adding the successor nodes to the fringe list with it's h-value, f-value and, parent_node_id
            for neighbour, true_val in graph[node].items():
                if neighbour not in parent_nodes:
                    f_value = h_value + true_val + g_value
                    heapq.heappush(
                        fringe_list, (f_value, true_val + g_value, neighbour, t)
                    )
                    no_nodes_generated = no_nodes_generated + 1
                # Ending condition...when we reach again to root node
                elif len(parent_nodes) == len(graph) and neighbour == parent_nodes[-1]:
                    heapq.heappush(
                        fringe_list, (f_value, true_val + g_value, neighbour, t)
                    )
                    no_nodes_generated = no_nodes_generated + 1

            no_nodes_expanded = no_nodes_expanded + 1
    return [], 0, 0


if __name__ == "__main__":

    graph = defaultdict(dict)  # store data values like a map key:value pair
    graph_input = None
    # graph_input = [('A', 'B', 20), ('B', 'D', 34), ('C', 'D', 12), ('A', 'C', 42), ('A', 'D', 35), ('B', 'C', 30)]
    # graph_input = [('A', 'B', 10), ('B', 'D', 25), ('C', 'D', 30), ('A', 'C', 15), ('A', 'D', 20), ('B', 'C', 35)]

    i = 0
    with open("example.txt", "r") as f:
        lines = f.readlines()

    for line in lines:
        graph_input = line.split(" ")
        graph_input = graph_input[0 : len(graph_input) - 1]
        if graph_input is not None:
            j = 0
            for c in graph_input:
                if c != "inf":
                    adding_new_edge_to_graph(graph, i, j, float(c))
                j += 1
        i += 1
        # print(i)

    # Creating the graph from hard coded input
    # if graph_input is not None:
    #     for n1, n2, c in graph_input:
    #         if c != 'inf':
    #             adding_new_edge_to_graph(graph, n1, n2, c)

    print(graph)
    if len(graph) != 0:
        # Call Tsp path function which uses A* algorithm to exapnd nodes in order of non decresing f-values using
        # MST as admisible Heurestics (Prim's algorithm for MST)
        # print(find_optimal_tsp_path(graph))
        optimal_tsp, expanded_nodes, generated_nodes = find_optimal_tsp_path(graph)
        print("\nOptimal Path for TSP : \n")
        print(optimal_tsp)

        optimal_cost = 0
        for i in range(1, len(optimal_tsp)):
            optimal_cost = optimal_cost + graph[optimal_tsp[i - 1]][optimal_tsp[i]]

        print("\nOptimal Cost for TSP :", optimal_cost, "\n")
        print("Number of Expanded Nodes : ", expanded_nodes, "\n")
        print("Number of Generated nodes in fringe list : ", generated_nodes, "\n")

    else:
        print("Given Graph is empty")