"""
Author:     Coen Konings
Date:       October 9, 2023
Edited by:  Coen Konings
On:         October 21, 2023

markov.py:
Contains the necessary classes to generate a polyphonic rhythm using a Markov
chain.
"""
from random import random


class Node:
    def __init__(self, name):
        """
        A node has a name. After the node has been created, edges can be added
        to connect nodes with each other.

        TODO restructure so that the name and the sounds associated with the
        node are independent.
        """
        self.name = name
        self.edges = []

    def __str__(self):
        return "Node {}.".format(self.name)

    def add_edge(self, node, value):
        """
        Add an edge from this node to the given node.
        """
        total_value = sum(edge.value for edge in self.edges)

        if total_value + value > 1:
            raise Exception("Node: Value of edges exceeded 1")

        self.edges.append(Edge(self, node, value))

    def follow_random_edge(self):
        """
        Follow a random edge based on their probabilities. Return the node that
        edge leads to.
        """
        value = random()
        total = 0

        for edge in self.edges:
            total += edge.value

            if value < total:
                return edge.follow()

        # If none of the edges are selected (this can happen if the edges'
        # probabilities don't add up to 1), return self.
        return self


class Edge:
    """
    Edges are one-directional connections between nodes.
    """

    def __init__(self, node_1, node_2, value):
        self.node_from = node_1
        self.node_to = node_2
        self.value = value

    def __str__(self):
        return "Edge from {} to {} with value {}".format(
            self.node_from, self.node_to, self.value
        )

    def follow(self):
        return self.node_to


class MarkovChain:
    """
    A markov chain consists of a set of nodes. The nodes are connected by
    edges, whose values represent the probability that the state transitions
    from one node to another at every timestep.
    """

    def __init__(self):
        """
        Markov chains are initialized stateless and with an empty set of nodes.
        """
        self.nodes = []
        self.state = None

    def add_node(self, name):
        """
        Add a new node to the Markov chain. Names should be unique.
        """
        if self.node_exists(name):
            raise Exception("A node with name {} already exists.".format(name))

        self.nodes.append(Node(name))

    def add_edge_by_node_index(self, node_1, node_2, value):
        """
        Add an edge between two nodes identified by their indices.
        """
        if (
            node_1 < 0
            or node_1 >= len(self.nodes)
            or node_2 < 0
            or node_2 >= len(self.nodes)
        ):
            raise Exception("Node index out of range")

        self.nodes[node_1].add_edge(self.nodes[node_2], value)

    def get_node_by_name(self, node_name):
        """
        Get a node by its name.
        """
        return next((node for node in self.nodes if node.name == node_name), None)

    def add_edge_by_node_name(self, node_1_name, node_2_name, value):
        """
        Add an edge between two nodes identified by their names.
        """
        self.check_if_nodes_exist([node_1_name, node_2_name])
        node_1 = self.get_node_by_name(node_1_name)
        node_2 = self.get_node_by_name(node_2_name)

        node_1.add_edge(node_2, value)

    def check_if_nodes_exist(self, node_names):
        """
        Check if a node exists. Raise an exception if it doesn't.
        """
        for node_name in node_names:
            if not self.node_exists(node_name):
                raise Exception("Node with name {} does not exist.".format(node_name))

    def node_exists(self, node_name):
        """
        Return true if a node with the given name exists. Return false
        otherwise.
        """
        return any(node.name == node_name for node in self.nodes)

    def set_state(self, node_name):
        """
        Set the current state to the node with the given name.
        """
        self.check_if_nodes_exist([node_name])
        self.state = self.get_node_by_name(node_name)

    def step(self):
        """
        Change the chain's state.
        """

        if not self.state:
            self.state = self.nodes[0]
        else:
            self.state = self.state.follow_random_edge()

    def from_rhythm_file(self, file_path):
        """
        Read a rhythm from a file and generate a markov chain.
        TODO: clean up this mess
        """

        self.nodes = []
        self.state = None

        with open(file_path) as input_file:
            lines = [line for line in input_file]

        lines.append(lines[-1])  # Process the rhythm as if it is looping
        rhythm = {}
        total_length = 0

        for line in lines:
            # Get part name and rhythm from line.
            name, part = line.split()
            rhythm[name] = [*part]

            # Track the total length of the rhythm in 16th notes.
            if len(rhythm[name]) > total_length:
                total_length = len(rhythm[name])

        onsets = []

        for i in range(total_length):
            node_name = ""

            # Nodes are named for their events (eg. low for a kick, high&low for a
            # kick and a hihat simultaneously, empty string for a rest)
            for key in rhythm.keys():
                if rhythm[key][i] == "x":
                    node_name = key if node_name == "" else node_name + "&" + key

            onsets.append(node_name)

        edges = {}
        onset = onsets.pop(0)

        # Create a dictionary of the ways in which nodes follow each other.
        while len(onsets) != 0:
            if onset in edges.keys():
                edges[onset].append(onsets[0])
            else:
                edges[onset] = [onsets[0]]

            onset = onsets.pop(0)

        # Create the Markov Chain given the previously generated dictionary.
        for node_name in edges.keys():
            self.add_node(node_name)

        for from_node_name in edges.keys():
            for to_node_name in edges.keys():
                percent = edges[from_node_name].count(to_node_name) / len(
                    edges[from_node_name]
                )
                self.add_edge_by_node_name(from_node_name, to_node_name, percent)


if __name__ == "__main__":
    print("Please run from main.py.")
