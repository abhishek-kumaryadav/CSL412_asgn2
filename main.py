import collections
import sys
import math
import bisect
import heapq
from sys import stdin, stdout
from math import gcd, floor, sqrt, log
from collections import defaultdict as dd
from itertools import permutations
from bisect import bisect_left as bl, bisect_right as br
from functools import lru_cache
from contextlib import redirect_stdout

sys.setrecursionlimit(100000000)

int_r = lambda: int(sys.stdin.readline())
str_r = lambda: sys.stdin.readline().strip()
intList_r = lambda: list(map(int, sys.stdin.readline().strip().split()))
strList_r = lambda: list(sys.stdin.readline().strip())
jn = lambda x, l: x.join(map(str, l))
mul = lambda: map(int, sys.stdin.readline().strip().split())
mulf = lambda: map(float, sys.stdin.readline().strip().split())
ceil = lambda x: int(x) if (x == int(x)) else int(x) + 1
ceildiv = lambda x, d: x // d if (x % d == 0) else x // d + 1
flush = lambda: stdout.flush()
outStr = lambda x: stdout.write(str(x))
mod = 1000000007


class Graph:
    def __init__(self, inputFileName, outputFileName):
        self.adjMatrix = self.takeInputs(inputFileName)

    def takeInputs(self, inputFileName):
        """Return an Adjacency Matrix
        Reads line by line
        Removes \n per line
        adds
        """
        adj = collections.defaultdict(dict)
        with open(inputFileName, "r") as f:
            lines = f.readlines()
            i = 0
            for line in lines:  # Outer loop, for each line: maintains row in matrix
                graph_input = line.split(" ")
                graph_input = graph_input[0 : len(graph_input) - 1]
                if graph_input is not None:
                    j = 0
                    for (
                        weight
                    ) in (
                        graph_input
                    ):  # Inner loop, for each weight: maintains column in matrix
                        if weight != "-1":
                            adj[i][j] = float(weight)
                            adj[j][i] = float(weight)
                        j += 1
                i += 1
        return adj

    # def findMinFromDict(self, nodes):
    #     """Return node number with minimum edge to any node"""
    #     #   maxsize works as +ve Infinity
    #     min_key, min_val = None, sys.maxsize
    #     for node, val in nodes.items():
    #         if min_val > val[1]:  # val[0] is the node it is connected to
    #             min_val = val[1]  # val[1] is cost to node val[0]
    #             min_key = node
    #     if min_key is None:
    #         # print(list(nodes.keys())[0])
    #         return list(nodes.keys())[0]  # Return first value if no value found
    #     else:
    #         # print(min_key)
    #         return min_key

    def findMinFromNotMst(self, lis):
        min_val = min([l.cost for l in lis])
        min_key = [l.node for l in lis if l.cost == min_val]
        min_k = min(lis, key=lambda x: x.cost)
        # print(min_key[0], min_k.node)
        return min_k

    def getMST(self, nodes=None):
        mstList = list()
        # Creates a linked list of visited set, connected parent to child node
        notMstSet = None
        notMstList = list()
        INF = sys.maxsize

        # notMstSet contains all nodes which are not visited and along with their every neighbour with it's cost
        if nodes is None:
            for n in self.adjMatrix.keys():
                notMstList.append(self.NodeNotMst(n, None, INF))
            notMstSet = {node: (None, INF) for node in self.adjMatrix.keys()}
        else:
            for n in nodes:
                notMstList.append(self.NodeNotMst(n, None, INF))
            notMstSet = {node: (None, INF) for node in nodes}

        # Run until all nodes are in mst
        while len(notMstList) != 0:
            # Find the node which has least cost edge
            # newNode = self.findMinFromDict(notMstSet)
            newListNode = self.findMinFromNotMst(notMstList)
            # print(newNode, newListNode)
            # assert newNode == newListNode.node
            # Remove node from notMstSet and add to mstSet
            # gotoMst = notMstSet.pop(newNode)
            # assert gotoMst[0] == newListNode.neighbour
            notMstList.remove(newListNode)

            mstList.append((newListNode.neighbour, newListNode.node))
            # print(mstList)
            # mstList.append((newNode.node,newListNode.node))

            # Update all edges if shorter edge found
            for b, weight in self.adjMatrix[
                newListNode.node
            ].items():  # Go through all edges of newly added(to mstSet) node
                # if notMstSet.get(b, None) != None and weight < notMstSet.get(b)[1]:
                #     # Check if nodes connected to newly added node are present in notMstSet
                #     notMstSet[b] = (newNode, weight)
                #     # Updating source as newNode with cost
                kek = [k for k in notMstList if (k.node == b and weight < k.cost)]
                if kek:
                    kek[0].neighbour = newListNode.node
                    kek[0].cost = weight
        return mstList

    class NodeNotMst:
        def __init__(self, node, neighbour, cost):
            self.node = node
            self.cost = cost
            self.neighbour = neighbour

        def __str__(self) -> str:
            return "Node: {}, To: {}, Cost: {}".format(
                self.node, self.neighbour, self.cost
            )

    def runAStar(self):
        heap = []
        heapq.heapify(heap)
        baseNode = self.Node(-1, None)  # Used to create a linked list for path
        heapq.heappush(heap, (0, 0, 0, baseNode))

        while heap:
            _, gLow, currentLow, parentLow = heapq.heappop(heap)
            newNode = self.Node(currentLow, parentLow)
            parentNode = newNode.parent  # Creating new node in linked list
            path = [currentLow]
            while parentNode.current != -1:
                path.append(parentNode.current)
                parentNode = parentNode.parent

            if len(path) - 1 == len(self.adjMatrix):
                return path[::-1]
            else:
                all_nodes = set([i for i in range(len(self.adjMatrix))])
                nodes_left = sorted(list(all_nodes - set(path)))
                mst_set = self.getMST(nodes_left)
                hVal = 0
                for i1, i2 in mst_set:
                    if i1 is not None and i2 is not None:
                        hVal += self.adjMatrix[i1][i2]
                for b, cost in self.adjMatrix[currentLow].items():
                    if b not in path:
                        fVal = hVal + cost + gLow
                        heapq.heappush(heap, (fVal, cost + gLow, b, newNode))
                    elif len(path) == len(self.adjMatrix) and b == path[-1]:
                        heapq.heappush(heap, (fVal, cost + gLow, b, newNode))
        return []

    class Node:
        def __init__(self, current=None, parent=None):
            self.current = current
            self.parent = parent

        def __lt__(lhs, rhs):
            return lhs.current < rhs.current

    def dfsConnected(self, node, g, visited):
        if visited[node]:
            return
        visited[node] = True
        for i in g[node]:
            self.dfsConnected(i[0], g, visited)

    def connected(self, g):
        visited = [False for i in range(len(g))]
        self.dfsConnected(0, g, visited)
        for i in visited:
            if not i:
                return False
        return True


def main():
    if len(sys.argv) == 3:
        graph = Graph(sys.argv[1], sys.argv[2])
        print(graph.adjMatrix)
        path = graph.runAStar()
        cost = 0
        for i in range(1, len(path)):
            cost += graph.adjMatrix[path[i]][path[i - 1]]
        print("Path:")
        print(" -> ".join([str(i) for i in path]))
        print("Cost: {}".format(cost))

    else:
        print("Illegal inputs")
        print("Example:")
        print("    python main.py in.txt out.txt")


if __name__ == "__main__":
    main()