"""
Author:     Coen Konings
Date:       October 9, 2023

markov.py:
Contains the necessary classes to generate a polyphonic rhythm using a Markov
chain.
"""
from random import random
import simpleaudio as sa
import time


class Node:
    def __init__(self, name):
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
        self.state = None

    def add_node(self, name):
        """
        Add a new node to the Markov chain.
        """
        if self.node_exists(name):
            raise Exception("A node with name {} already exists.".format(name))

        self.nodes.append(Node(name))

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

    def node_exists(self, name):
        return any(node.name == name for node in self.nodes)

    def step(self):
        """
        Change the chain's state.
        """

        if not self.state:
            self.state = self.nodes[0]
        else:
            self.state = self.state.follow_random_edge()

        sounds = self.state.name.split("&")

        for sound in sounds:
            if sound == "low":
                sa.WaveObject.from_wave_file("../assets/kick.wav").play()
            elif sound == "mid":
                sa.WaveObject.from_wave_file("../assets/snare.wav").play()
            elif sound == "high":
                sa.WaveObject.from_wave_file("../assets/hat.wav").play()


def markov_chain_from_rhythm_file():
    """
    Read a rhythm from a file and generate a markov chain.
    TODO: clean up this mess
    """
    markov_chain = MarkovChain()

    with open("markov_input.txt") as input_file:
        lines = [line for line in input_file]

    rhythm = {}
    total_length = 0

    for line in lines:
        name, part = line.split()
        rhythm[name] = [*part]

        if len(rhythm[name]) > total_length:
            total_length = len(rhythm[name])

    onsets = []

    for i in range(total_length):
        node_name = ""

        for key in rhythm.keys():
            if rhythm[key][i] == "x":
                node_name = key if node_name == "" else node_name + "&" + key

        onsets.append(node_name)

    edges = {}
    onset = onsets.pop(0)

    while len(onsets) != 0:
        if onset in edges.keys():
            edges[onset].append(onsets[0])
        else:
            edges[onset] = [onsets[0]]

        onset = onsets.pop(0)

    for node_name in edges.keys():
        markov_chain.add_node(node_name)

    for from_node_name in edges.keys():
        for to_node_name in edges.keys():
            percent = edges[from_node_name].count(to_node_name) / len(edges[from_node_name])
            markov_chain.add_edge_by_node_name(from_node_name, to_node_name, percent)

    return markov_chain


def main():
    mode = input("Select the mode. 1 for markov chain from rhythm, 2 for markov chain from file.\n>")
    markov_chain = None

    if mode == "1":
        markov_chain = markov_chain_from_rhythm_file()
    elif mode == "2":
        pass
    else:
        print("Invalid mode.")
        exit()

    start_time = time.time()
    bpm = 120
    sixteenth_duration = 15 / bpm
    i = 0

    while True:
        if time.time() - start_time >= i * sixteenth_duration:
            markov_chain.step()
            i += 1

        time.sleep(0.001)


if __name__ == "__main__":
    main()
