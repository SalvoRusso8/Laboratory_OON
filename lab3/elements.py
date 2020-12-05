from lab3.info import Signal_information
from scipy.constants import c
import json
import numpy as np
import matplotlib.pyplot as plt

class Node(object):
    def __init__(self, node_dictionary):
        self._label = node_dictionary['label']
        self._position = node_dictionary['position']
        self._connected_nodes = node_dictionary['connected_nodes']
        self._successive = {}

    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def propagate(self, signal_information):
        path = signal_information.path
        if len(path) > 1:
            line_label = path[:2]
            line = self.successive[line_label]
            signal_information.next()
            signal_information = line.propagate(signal_information)
        return signal_information


class Line(object):
    def __init__(self, line_dictionary):
        self._label = line_dictionary['label']
        self._length = line_dictionary['length']
        self._successive = {}

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    def latency_generation(self):
        latency = self.length / (c * 2 / 3)
        return latency

    def noise_generation(self, signal_power):
        noise = 1e-9 * signal_power * self.length
        return noise

    def propagate(self, signal_information):
        signal_power = signal_information.signal_power
        noise = self.noise_generation(signal_power)
        signal_information.add_noise(noise)
        latency = self.latency_generation()
        signal_information.add_latency(latency)
        node = self.successive[signal_information.path[0]]
        signal_information = node.propagate(signal_information)
        return signal_information


class Network(object):
    def __init__(self, file):
        self._nodes = {}
        self._lines = {}
        nodes_json = json.load(open(file, 'r'))

        for label in nodes_json:
            node_dictionary = nodes_json[label]
            node_dictionary['label'] = label
            node = Node(node_dictionary)
            self._nodes[label] = node
            for connected_nodes_label in node_dictionary['connected_nodes']:
                line_dictionary = {}
                line_label = label + connected_nodes_label
                line_dictionary['label'] = line_label
                node_position = np.array(nodes_json[label]['position'])
                connected_nodes_position = np.array(nodes_json[connected_nodes_label]['position'])
                line_dictionary['length'] = np.sqrt(np.sum((node_position - connected_nodes_position) ** 2))
                line = Line(line_dictionary)
                self._lines[line_label] = line

    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    def connect(self):
        nodes_dictionary = self.nodes
        lines_dictionary = self.lines
        for node_label in nodes_dictionary:
            node = nodes_dictionary[node_label]
            for connected_node in node.connected_nodes:
                line_label = node_label + connected_node
                line = lines_dictionary[line_label]
                line.successive[connected_node] = nodes_dictionary[connected_node]
                node.successive[line_label] = lines_dictionary[line_label]

    def find_paths(self, label1, label2):
        cross_nodes = [key for key in self.nodes.keys()
                       if ((key != label1) & (key != label2))]
        cross_lines = self.lines.keys()
        inner_paths = {'0': label1}
        for i in range(len(cross_nodes) + 1):
            inner_paths[str(i+1)] = []
            for inner_path in inner_paths[str(i)]:
                inner_paths[str(i+1)] += [inner_path + cross_node for cross_node in cross_nodes
                                          if ((inner_path[-1] + cross_node in cross_lines) & ( cross_node not in inner_path))]
        paths = []
        for i in range(len(cross_nodes) + 1):
            for path in inner_paths[str(i)]:
                if path[-1] + label2 in cross_lines:
                    paths.append(path + label2)
        return paths

    def propagate(self, signal_information):
        path = signal_information.path
        first_node = self.nodes[path[0]]
        propagated_signal_information = first_node.propagate(signal_information)
        return propagated_signal_information

    def draw(self):
        nodes = self.nodes
        for node_label in nodes:
            n0 = nodes[node_label]
            x0 = n0.position[0]
            y0 = n0.position[1]
            plt.plot(x0, y0, 'go', markersize=10)
            plt.text(x0 + 20, y0 + 20, node_label)
            for connected_node_label in n0.connected_nodes:
                n1 = nodes[connected_node_label]
                x1 = n1.position[0]
                y1 = n1.position[1]
                plt.plot([x0, x1], [y0, y1], 'b')
        plt.title('Network')
        plt.show()