"""
Author:     Coen Konings
Date:       October 9, 2023

markov.py:
Contains the necessary classes to generate a polyphonic rhythm using a Markov
chain.
"""
from random import random


class Node:
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration
        self.edges = []

    def __str__(self):
        return "Node {}, duration {}.".format(self.name, self.duration)

    def add_edge(self, node, value):
        """
        Add an edge from this node to the given node.
        """
        total_value = sum(edge.value for edge in self.edges)

        if total_value + value > 1:
            raise Exception("Node: Value of edges exceeded 1")

        self.edges.append(Edge(self, node, value))

    def follow_random_edge(self):
        value = random()
        total = 0

        for edge in self.edges:
            total += edge.value

            if value < total:
                return edge.node_to


class Edge:
    """
    Edges are one-directional connections between nodes.
    """
    def __init__(self, node_1, node_2, value):
        self.node_from = node_1
        self.node_to = node_2
        self.value = value


class MarkovChain:
    """
    A markov chain consists of a set of nodes. The nodes are connected by
    edges, whose values represent the probability that the state transitions
    from one node to another at every timestep.
    """
    def __init__(self):
        self.nodes = []

    def add_node(self, name, duration):
        """
        Add a new node to the Markov chain.
        """
        if any(node.name == name for node in self.nodes):
            raise Exception("A node with name {} already exists.".format(name))

        self.nodes.append(Node(name, duration))

    def add_edge_by_node_index(self, node_1, node_2, value):
        """
        Add an edge between two nodes identified by their indices.
        """
        if node_1 < 0 or node_1 >= len(self.nodes) or node_2 < 0 or node_2 >= len(self.nodes):
            raise Exception("Node index out of range")

        self.nodes[node_1].add_edge(self.nodes[node_2], value)

    def add_edge_by_node_name(self, node_1_name, node_2_name, value):
        """
        Add an edge between two nodes identified by their names.
        """
        node_1 = next((node for node in self.nodes if node.name == node_1_name), None)
        node_2 = next((node for node in self.nodes if node.name == node_2_name), None)

        if not node_1:
            raise Exception("Node with name {} does not exist.".format(node_1_name))
        if not node_2:
            raise Exception("Node with name {} does not exist.".format(node_2_name))

        node_1.add_edge(node_2, value)
