from scipy.constants import c


class Line(object):
    def __init__(self, line_dictionary):
        self._label = line_dictionary['label']
        self._length = line_dictionary['length']
        self._successive = {}
        self._state = 'free'

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @property
    def state(self):
        return self._state

    @successive.setter
    def successive(self, successive):
        self._successive = successive

    @state.setter
    def state(self, state):
        self._state = state

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
