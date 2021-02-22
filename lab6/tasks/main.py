from copy import deepcopy

from lab6.core.elements.network import Network
from lab6.core.info.signalInformation import SignalInformation
from lab6.core.elements.connection import Connection
import pandas as pd
import numpy as np
import random as rand
import matplotlib.pyplot as plt

if __name__ == '__main__':
    network_snr = Network('../resources/nodes.json')
    network_snr.connect()
    node_labels = network_snr.nodes.keys()
    pairs = []
    for label1 in node_labels:
        for label2 in node_labels:

            if label1 != label2:
                pairs.append(label1 + label2)
            columns = ['path', 'latency', 'noise', 'snr']
            df = pd.DataFrame()
            paths = []
            latencies = []
            noises = []
            snrs = []
            for pair in pairs:
                for path in network_snr.find_paths(pair[0], pair[1]):
                    path_string = ''
                    for node in path:
                        path_string += node + '->'
                    paths.append(path_string[:-2])
                    signal_information = SignalInformation(1e-3, path)
                    signal_information = network_snr.propagate(signal_information)
                    latencies.append(signal_information.latency)
                    noises.append(signal_information.noise_power)
                    snrs.append(
                        10 * np.log10(
                            signal_information.signal_power / signal_information.noise_power))
            df['path'] = paths
            df['latency'] = latencies
            df['noise'] = noises
            df['snr'] = snrs

    network_snr.draw()
    network_snr.weighted_path = df
    network_snr.update_routing_space(None)

    connections_snr = []
    nodes = 'ABCDEF'
    for i in range(0, 100):
        input_rand = rand.choice(nodes)
        while True:
            output_rand = rand.choice(nodes)
            if input_rand != output_rand:
                break
        connections_snr.append(Connection(input_rand, output_rand, 1e-3))
    connections_latency = deepcopy(connections_snr)

    # Stream with label='snr'
    network_snr.stream(connections_snr, 'snr')
    snr_list = [c.snr for c in connections_snr]
    plt.figure()
    plt.hist(snr_list, label='Snr distribution')
    plt.title('[Lab6] SNR distribution')
    plt.ylabel('#Connections')
    plt.xlabel('SNR [dB]')
    plt.show(block=True)

    # Stream with label='latency'
    network_latency = Network('../resources/nodes.json')
    network_latency.connect()
    network_latency.weighted_path = df
    network_latency.update_routing_space(None)
    network_latency.stream(connections_latency, 'latency')
    latency_list = [c.latency * 1e3 for c in connections_latency]
    plt.figure()
    plt.hist(latency_list, label='Latency distribution')
    plt.title('[Lab6] Latency distribution')
    plt.ylabel('#Connections')
    plt.xlabel('Latency [ms]')
    plt.show(block=True)
