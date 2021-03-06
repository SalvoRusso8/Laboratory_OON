import csv
from copy import deepcopy

from lab10.core.elements.network import Network
from lab10.core.info.signalInformation import SignalInformation
from lab10.core.elements.connection import Connection
import pandas as pd
import numpy as np
import random as rand
import matplotlib.pyplot as plt
import statistics as st

if __name__ == '__main__':
    network_fixed_rate = Network('../resources/nodes_full_fixed_rate.json')
    network_fixed_rate.connect()
    node_labels = network_fixed_rate.nodes.keys()
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
                for path in network_fixed_rate.find_paths(pair[0], pair[1]):
                    path_string = ''
                    for node in path:
                        path_string += node + '->'
                    paths.append(path_string[:-2])
                    signal_information = SignalInformation(1e-3, path)
                    signal_information = network_fixed_rate.propagate(signal_information)
                    latencies.append(signal_information.latency)
                    noises.append(signal_information.noise_power)
                    snrs.append(
                        10 * np.log10(
                            signal_information.signal_power / signal_information.noise_power))
            df['path'] = paths
            df['latency'] = latencies
            df['noise'] = noises
            df['snr'] = snrs

    network_fixed_rate.draw()
    network_fixed_rate.weighted_path = df
    network_fixed_rate.update_routing_space(None)

    connections_fixed_rate = []
    with open('../resources/connections_test.csv') as connections_file:
        csvReader = csv.reader(connections_file)
        for row in csvReader:
            connections_fixed_rate.append(Connection(row[0], row[1], float(row[2])))

    '''nodes = 'ABCDEF'
    for i in range(0, 100):
        input_rand = rand.choice(nodes)
        while True:
            output_rand = rand.choice(nodes)
            if input_rand != output_rand:
                break
        connections_full.append(Connection(input_rand, output_rand, 1e-3))'''

    connections_flex_rate = deepcopy(connections_fixed_rate)
    connections_shannon =  deepcopy(connections_fixed_rate)
    
    # Stream with label='snr'
    network_fixed_rate.stream(connections_fixed_rate, 'snr')
    snr_fixed_rate = [c.snr for c in connections_fixed_rate if c.bit_rate != 0]
    plt.figure()
    plt.hist(snr_fixed_rate, label='Snr distribution')
    plt.title('[Lab8] SNR distribution with fixed rate')
    plt.ylabel('#Connections')
    plt.xlabel('SNR [dB]')
    plt.show(block=True)
    bit_rate_fixed_rate = [c.bit_rate for c in connections_fixed_rate if c.bit_rate != 0]
    print("Overall average bit rate with Fixed Rate: ", st.mean(bit_rate_fixed_rate), "bps [",
          st.mean(bit_rate_fixed_rate)/1e9, "Gbps]")
    print("Total capacity with Fixed Rate: ", sum(bit_rate_fixed_rate), "bps [",
          sum(bit_rate_fixed_rate)/1e9, "Gbps]")

    network_flex_rate = Network('../resources/nodes_full_flex_rate.json')
    network_flex_rate.connect()
    network_flex_rate.weighted_path = df
    network_flex_rate.update_routing_space(None)
    network_flex_rate.stream(connections_flex_rate, 'snr')
    snr_flex_rate = [c.snr for c in connections_flex_rate if c.bit_rate != 0]
    plt.figure()
    plt.hist(snr_flex_rate, label='Snr distribution')
    plt.title('[Lab8] SNR distribution with flex rate')
    plt.ylabel('#Connections')
    plt.xlabel('SNR [dB]')
    plt.show(block=True)
    bit_rate_flex_rate = [c.bit_rate for c in connections_flex_rate if c.bit_rate != 0]
    print("Overall average bit rate with Flex Rate: ", st.mean(bit_rate_flex_rate),
          "bps [", st.mean(bit_rate_flex_rate)/1e9, "Gbps]")
    print("Total capacity with Flex Rate: ", sum(bit_rate_flex_rate), "bps [", sum(bit_rate_flex_rate)/1e9, "Gbps]")

    network_shannon = Network('../resources/nodes_full_shannon.json')
    network_shannon.connect()
    network_shannon.weighted_path = df
    network_shannon.update_routing_space(None)
    network_shannon.stream(connections_shannon, 'snr')
    snr_shannon = [c.snr for c in connections_shannon if c.bit_rate != 0]
    plt.figure()
    plt.hist(snr_shannon, label='Snr distribution')
    plt.title('[Lab8] SNR distribution with Shannon')
    plt.ylabel('#Connections')
    plt.xlabel('SNR [dB]')
    plt.show(block=True)
    bit_rate_shannon = [c.bit_rate for c in connections_shannon if c.bit_rate != 0]
    print("Overall average bit rate with Shannon: ", st.mean(bit_rate_shannon), "bps [", st.mean(bit_rate_shannon)/1e9, "Gbps]")
    print("Total capacity with Shannon: ", sum(bit_rate_shannon), "bps [", sum(bit_rate_shannon)/1e9, "Gbps]")

    plt.figure()
    plt.hist(bit_rate_fixed_rate, label='Bit Rate Fixed Rate')
    plt.title('[Lab8] Bit rate distribution with Fixed Rate')
    plt.ylabel('#Connections')
    plt.xlabel('bit rate [bps]')
    plt.show(block=True)

    plt.figure()
    plt.hist(bit_rate_flex_rate, label='Bit Rate Flex Rate')
    plt.title('[Lab8] Bit rate distribution with Flex Rate')
    plt.ylabel('#Connections')
    plt.xlabel('bit rate [bps]')
    plt.show(block=True)

    plt.figure()
    plt.hist(bit_rate_shannon, label='Bit Rate Shannon')
    plt.title('[Lab8] Bit rate distribution with Shannon')
    plt.ylabel('#Connections')
    plt.xlabel('bit rate [bps]')
    plt.show(block=True)

