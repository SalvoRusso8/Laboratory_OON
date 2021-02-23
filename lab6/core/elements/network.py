import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lab6.core.elements.node import Node
from lab6.core.elements.line import Line
from lab6.core.info.lightpath import Lightpath

n_channel = 10


class Network(object):
    def __init__(self, file):
        self._nodes = {}
        self._lines = {}
        nodes_json = json.load(open(file, 'r'))
        self._weighted_path = pd.DataFrame()
        columns_name = ["path", "channels"]
        self._route_space = pd.DataFrame(columns=columns_name)

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

    @property
    def route_space(self):
        return self._route_space

    @weighted_path.setter
    def weighted_path(self, weighted_path):
        self._weighted_path = weighted_path

    @route_space.setter
    def route_space(self, route_space):
        self._route_space = route_space

    def connect(self):
        nodes_dictionary = self.nodes
        lines_dictionary = self.lines
        for node_label in nodes_dictionary:
            node = nodes_dictionary[node_label]
            # initializing the node switching matrix
            node.switching_matrix = {}
            for node1 in node.connected_nodes:
                node.switching_matrix[node1] = {}
                for node2 in node.connected_nodes:
                    if node2 == node1:
                        node.switching_matrix[node1][node2] = np.zeros(n_channel, np.int8)
                    else:
                        node.switching_matrix[node1][node2] = np.ones(n_channel, np.int8)
                line_label = node_label + node1
                line = lines_dictionary[line_label]
                line.successive[node1] = nodes_dictionary[node1]
                node.successive[line_label] = lines_dictionary[line_label]

    def find_paths(self, label1, label2):
        cross_nodes = [key for key in self.nodes.keys()
                       if ((key != label1) & (key != label2))]
        cross_lines = self.lines.keys()
        inner_paths = {'0': label1}
        for i in range(len(cross_nodes) + 1):
            inner_paths[str(i + 1)] = []
            for inner_path in inner_paths[str(i)]:
                inner_paths[str(i + 1)] += [inner_path + cross_node for cross_node in cross_nodes
                                            if ((inner_path[-1] + cross_node in cross_lines) & (
                            cross_node not in inner_path))]
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
            return None, None, None
        my_df = self.weighted_path
        my_df.sort_values(by=['snr'], inplace=True, ascending=False)
        my_df_filtered = my_df[(my_df['path'].str[0] == input_node) & (my_df['path'].str[-1] == output_node)]
        for i in my_df_filtered.values:
            path = i[0]
            channel = self.find_free_channel(path)
            if channel is not None:
                return i, i[0], channel
        return None, None, None

    def find_best_latency(self, input_node, output_node):
        if output_node == input_node:
            return None
        my_df = self.weighted_path
        my_df.sort_values(by=['latency'], inplace=True, ascending=True)
        my_df_filtered = my_df[(my_df['path'].str[0] == input_node) & (my_df['path'].str[-1] == output_node)]
        for i in my_df_filtered.values:
            path = i[0]
            channel = self.find_free_channel(path)
            if channel is not None:
                return i, i[0], channel
        return None, None, None

    def find_free_channel(self, path):
        # finding the requested path in the route space, and searching for the first free channel, if present
        path_found = self.route_space[self.route_space['path'] == path]
        for i in range(n_channel):
            if path_found['channels'].values[0][i] == 1:
                return i
        return None

    def stream(self, connections, label='latency'):
        for connection in connections:
            if label == 'snr':
                best_path_info, best_path, channel = self.find_best_snr(connection.input, connection.output)
            else:
                best_path_info, best_path, channel = self.find_best_latency(connection.input, connection.output)
            # best_path_info contains the entire weighted path row, best_path contains only the path
            if best_path is not None:
                path_label = ''
                for index in range(0, len(best_path), 3):
                    path_label += best_path[index]
                lightpath = Lightpath(connection.signal_power, path_label, channel)
                self.propagate(lightpath)
                # setting to occupied the channel in the lines crossed and in the complete path in the route space
                # data structure
                connection.snr = 10 * np.log10(lightpath.signal_power / lightpath.noise_power)
                connection.latency = lightpath.latency
                self.update_routing_space(best_path)
            else:
                connection.snr = 0
                connection.latency = -1

    def update_routing_space(self, best_path):
        if best_path is None:
            # initializing routing space
            for path in self.weighted_path['path']: self.route_space = self.route_space.append(
                {'path': path, 'channels': [1] * n_channel}, ignore_index=True, sort=None)
        else:
            for path in self.route_space['path']:
                node1 = 3
                first_line = self.lines[path[0] + path[node1]]
                line_state = first_line.state
                for node_i in range(6, len(path), 3):
                    line = self.lines[path[node1] + path[node_i]]
                    line_state = np.multiply(line_state, line.state)
                    line_state = np.multiply(self.nodes[path[node1]].switching_matrix[path[node1 - 3]][path[node_i]],
                                             line_state)
                    node1 = node_i
                route_space_index = self.route_space[self.route_space['path'] == path].index.values[0]
                self.route_space.at[route_space_index, 'channels'] = line_state
