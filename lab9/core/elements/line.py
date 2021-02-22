from scipy.constants import c
import numpy as np
from lab9.core.info.lightpath import Lightpath
from math import ceil

n_channel = 10
distance_amp = 80e3  # [m]
gain_const = 16  # [dB]
noise_figure_const = 3  # [dB]

class Line(object):
    def __init__(self, line_dictionary):
        self._label = line_dictionary['label']
        self._length = line_dictionary['length']
        self._successive = {}
        self._state = []
        self._state = np.ones(n_channel, np.int8)
        self._n_amplifiers = (ceil(self.length / distance_amp) - 1) + 2  # +2 is because of booster and preamp
        self._gain = gain_const
        self._noise_figure = noise_figure_const

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

    @property
    def n_amplifiers(self):
        return self._n_amplifiers

    @property
    def gain(self):
        return self._gain

    @property
    def noise_figure(self):
        return self._noise_figure

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
        if type(lightpath) is Lightpath:
            lightpath = node.propagate(lightpath, self.label[0])
        else:
            lightpath = node.propagate(lightpath, None)
        return lightpath
