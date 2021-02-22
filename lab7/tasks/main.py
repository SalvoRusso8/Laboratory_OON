import csv
from copy import deepcopy

from lab7.core.elements.network import Network
from lab7.core.info.signalInformation import SignalInformation
from lab7.core.elements.connection import Connection
import pandas as pd
import numpy as np
import random as rand
import matplotlib.pyplot as plt

if __name__ == '__main__':
    network_full = Network('../resources/nodes_full.json')
    network_full.connect()
    node_labels = network_full.nodes.keys()
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
                for path in network_full.find_paths(pair[0], pair[1]):
                    path_string = ''
                    for node in path:
                        path_string += node + '->'
                    paths.append(path_string[:-2])
                    signal_information = SignalInformation(1e-3, path)
                    signal_information = network_full.propagate(signal_information)
                    latencies.append(signal_information.latency)
                    noises.append(signal_information.noise_power)
                    snrs.append(
                        10 * np.log10(
                            signal_information.signal_power / signal_information.noise_power))
            df['path'] = paths
            df['latency'] = latencies
            df['noise'] = noises
            df['snr'] = snrs

    network_full.draw()
    network_full.weighted_path = df
    network_full.update_routing_space(None)

    connections_full = []
    with open('../resources/connections_test.csv') as connections_file:
        csvReader = csv.reader(connections_file)
        for row in csvReader:
            connections_full.append(Connection(row[0], row[1], float(row[2])))

    '''nodes = 'ABCDEF'
    for i in range(0, 100):
        input_rand = rand.choice(nodes)
        while True:
            output_rand = rand.choice(nodes)
            if input_rand != output_rand:
                break
        connections_full.append(Connection(input_rand, output_rand, 1e-3))'''

    connections_not_full = deepcopy(connections_full)

    # Stream with label='snr'
    network_full.stream(connections_full, 'snr')
    snr_full_list = [c.snr for c in connections_full]
    plt.figure()
    plt.hist(snr_full_list, label='Snr distribution')
    plt.title('[Lab7] SNR distribution with full switching matrix')
    plt.ylabel('#Connections')
    plt.xlabel('SNR [dB]')
    plt.show(block=True)

    network_not_full = Network('../resources/nodes_not_full.json')
    network_not_full.connect()
    network_not_full.weighted_path = df
    network_not_full.update_routing_space(None)
    network_not_full.stream(connections_not_full, 'snr')
    snr_not_full_list = [c.snr for c in connections_not_full]
    plt.figure()
    plt.hist(snr_not_full_list, label='Snr distribution')
    plt.title('[Lab7] SNR distribution with not full switching matrix')
    plt.ylabel('#Connections')
    plt.xlabel('SNR [dB]')
    plt.show(block=True)

