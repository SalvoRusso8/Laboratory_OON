from lab7.core.info.lightpath import Lightpath

class Node(object):
    def __init__(self, node_dictionary):
        self._label = node_dictionary['label']
        self._position = node_dictionary['position']
        self._connected_nodes = node_dictionary['connected_nodes']
        self._successive = {}
        self._switching_matrix = None

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

    @property
    def switching_matrix(self):
        return self._switching_matrix

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    @switching_matrix.setter
    def switching_matrix(self, switching_matrix):
        self._switching_matrix = switching_matrix

    def propagate(self, signal_information, previous_node):
        path = signal_information.path
        if len(path) > 1:
            line_label = path[:2]
            if type(signal_information) is Lightpath:
                # making switching matrix dynamic
                if previous_node is not None:
                    channels = self.switching_matrix[previous_node][line_label[1]]
                    channels[signal_information.channel] = 0
                    if signal_information.channel != 9:
                        channels[signal_information.channel + 1] = 0
                    if signal_information.channel != 0:
                        channels[signal_information.channel - 1] = 0
            line = self.successive[line_label]
            signal_information.next()
            signal_information = line.propagate(signal_information)
        return signal_information
