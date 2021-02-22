from scipy.constants import c
import numpy as np
from lab6.core.info.lightpath import Lightpath

n_channel = 10


class Line(object):
    def __init__(self, line_dictionary):
        self._label = line_dictionary['label']
        self._length = line_dictionary['length']
        self._successive = {}
        self._state = []
        self._state = np.ones(n_channel, np.int8)

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

    def propagate(self, lightpath):
        if type(lightpath) is Lightpath:
            if lightpath.channel is not None:
                self.state[lightpath.channel] = 0  # 0 is occupied
        # updating noise
        signal_power = lightpath.signal_power
        noise = self.noise_generation(signal_power)
        lightpath.add_noise(noise)
        # updating latency
        latency = self.latency_generation()
        lightpath.add_latency(latency)

        node = self.successive[lightpath.path[0]]
        signal_information = node.propagate(lightpath)
        return signal_information
