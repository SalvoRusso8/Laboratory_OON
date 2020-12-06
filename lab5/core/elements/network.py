import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lab5.core.elements.node import Node
from lab5.core.elements.line import Line
from lab5.core.info.signalInformation import SignalInformation

class Network(object):
    def __init__(self, file):
        self._nodes = {}
        self._lines = {}
        nodes_json = json.load(open(file, 'r'))
        self._weighted_path = pd.DataFrame()

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

    @property
    def weighted_path(self):
        return self._weighted_path

    @weighted_path.setter
    def weighted_path(self, weighted_path):
        self._weighted_path = weighted_path

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

    def find_best_snr(self, input_node, output_node):
        if input_node == output_node:
            return None
        my_df = self.weighted_path
        my_df.sort_values(by=['snr'], inplace=True, ascending=False)
        my_df_filtered = my_df[(my_df['path'].str[0] == input_node) & (my_df['path'].str[-1] == output_node)]
        found = False
        for i in my_df_filtered.values:
            path = i[0]
            node1 = path[0]
            free = True
            for node_i in range(3, len(path), 3):
                line = self.lines[node1 + path[node_i]]
                if line.state != 'free':
                    free = False
                    break
                node1 = path[node_i]
            if free:
                found = True
                break
        if found:
            return i
        else:
            return None

    def find_best_latency(self, input_node, output_node):
        if output_node == input_node:
            return None
        my_df = self.weighted_path
        my_df.sort_values(by=['latency'], inplace=True, ascending=True)
        my_df_filtered = my_df[(my_df['path'].str[0] == input_node) & (my_df['path'].str[-1] == output_node)]
        found = False
        for i in my_df_filtered.values:
            path = i[0]
            node1 = path[0]
            free = True
            for node_i in range(3, len(path), 3):
                line = self.lines[node1 + path[node_i]]
                if line.state != 'free':
                    free = False
                    break
                node1 = path[node_i]
            if free:
                found = True
                break
        if found:
            return i
        else:
            return None

    def stream(self, connections, label='latency'):
        for connection in connections:
            if label == 'snr':
                best_path = self.find_best_snr(connection.input, connection.output)
            else:
                best_path = self.find_best_latency(connection.input, connection.output)
            if best_path is not None:
                path_label = ''
                for index in range(0, len(best_path[0]), 3):
                    path_label += best_path[0][index]
                signal_information = SignalInformation(connection.signal_power, path_label)
                self.propagate(signal_information)
                connection.snr = 10 * np.log10(signal_information.signal_power / signal_information.noise_power)
                connection.latency = signal_information.latency
                # set to occupied all lines crossed
                node1 = path_label[0]
                for node_i in path_label[1:]:
                    line = self.lines[node1 + node_i]
                    line.state = 'occupied'
                    node1 = node_i
            else:
                connection.snr = 0
                connection.latency = None
