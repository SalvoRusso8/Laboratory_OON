import csv
from copy import deepcopy, copy

from lab10.core.elements.network import Network
from lab10.core.info.signalInformation import SignalInformation
from lab10.core.elements.connection import Connection
import pandas as pd
import numpy as np
import random as rand
import matplotlib.pyplot as plt
import statistics as st
from math import inf

default_bandwidth = 100e9  # [bit]
M = 37
default_signal_power = 1e-3


def reset_traffic_matrix(traffic_matrix, network):
    for node1 in network.nodes.keys():
        traffic_matrix[node1] = {}
        for node2 in network_fixed_rate.nodes.keys():
            if node1 != node2:
                traffic_matrix[node1][node2] = default_bandwidth * M
            else:
                traffic_matrix[node1][node2] = inf


if __name__ == '__main__':
    for i in range(2):
        # if i==0, test connections, if i==1 use traffic matrix
        # i=1
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
                        signal_information = SignalInformation(default_signal_power, path)
                        signal_information = network_fixed_rate.propagate(signal_information)
                        latencies.append(signal_information.latency)
                        noises.append(signal_information.noise_power)
                        snrs.append(10 * np.log10(1 / signal_information.isnr))
                df['path'] = paths
                df['latency'] = latencies
                df['noise'] = noises
                df['snr'] = snrs

        network_fixed_rate.draw()
        network_fixed_rate.weighted_path = df
        network_fixed_rate.update_routing_space(None)
        if i == 0:
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
            connections_shannon = deepcopy(connections_fixed_rate)
            # Stream with label='snr'
            network_fixed_rate.stream(connections_fixed_rate, 'snr')
            print('Test connections iteration')
        if i == 1:
            print('Traffic matrix iteration')
            node_number = len(network_fixed_rate.nodes)
            traffic_matrix_fixed = {}
            reset_traffic_matrix(traffic_matrix_fixed, network_fixed_rate)
            # populate connections_fixed_rate array with the traffic matrix
            connections_left = node_number ** 2 - node_number
            connections_fixed_rate = []
            while connections_left > 0:
                connections_left -= network_fixed_rate.connections_traffic_matrix(traffic_matrix_fixed,
                                                                                  connections_fixed_rate,
                                                                                  default_signal_power)

        snr_fixed_rate = [c.snr for c in connections_fixed_rate if c.bit_rate != 0]
        plt.figure()
        plt.hist(snr_fixed_rate, label='Snr distribution')
        plt.title('[Lab10] SNR distribution with fixed rate')
        plt.ylabel('#Connections')
        plt.xlabel('SNR [dB]')
        plt.show()
        bit_rate_fixed_rate = [c.bit_rate for c in connections_fixed_rate if c.bit_rate != 0]
        print("Overall average bit rate with Fixed Rate: ", st.mean(bit_rate_fixed_rate), "bps [",
              st.mean(bit_rate_fixed_rate) / 1e9, "Gbps]")
        print("Total capacity with Fixed Rate: ", sum(bit_rate_fixed_rate), "bps [",
              sum(bit_rate_fixed_rate) / 1e9, "Gbps]")

        ch_occ = []
        for label in network_fixed_rate.lines.keys():
            counter = 0
            line_state = network_fixed_rate.lines[label].state
            for c in line_state:
                counter += c
            ch_occ.append((1 - (counter / len(line_state))) * 100)
            print(label + ":" + str((1 - (counter / len(line_state))) * 100))
        plt.figure()
        plt.bar(list(network_fixed_rate.lines.keys()), ch_occ,  label='Wavelength congestion')
        plt.xticks(list(network_fixed_rate.lines.keys()))
        plt.title('[Lab10] Wavelength congestion fixed rate')
        plt.ylabel('Congestion [%]')
        plt.xlabel('Line label')
        plt.show()

        network_flex_rate = Network('../resources/nodes_full_flex_rate.json')
        network_flex_rate.connect()
        network_flex_rate.weighted_path = df
        network_flex_rate.update_routing_space(None)
        if i == 1:
            traffic_matrix_flex = {}
            reset_traffic_matrix(traffic_matrix_flex, network_flex_rate)
            # populate connections_fixed_rate array with the traffic matrix
            connections_left = node_number ** 2 - node_number
            connections_flex_rate = []
            while connections_left > 0:
                connections_left -= network_flex_rate.connections_traffic_matrix(traffic_matrix_flex,
                                                                                 connections_flex_rate,
                                                                                 default_signal_power)
        else:
            network_flex_rate.stream(connections_flex_rate, 'snr')
        snr_flex_rate = [c.snr for c in connections_flex_rate if c.bit_rate != 0]
        plt.figure()
        plt.hist(snr_flex_rate, label='Snr distribution')
        plt.title('[Lab10] SNR distribution with flex rate')
        plt.ylabel('#Connections')
        plt.xlabel('SNR [dB]')
        plt.show()
        bit_rate_flex_rate = [c.bit_rate for c in connections_flex_rate if c.bit_rate != 0]
        print("Overall average bit rate with Flex Rate: ", st.mean(bit_rate_flex_rate),
              "bps [", st.mean(bit_rate_flex_rate) / 1e9, "Gbps]")
        print("Total capacity with Flex Rate: ", sum(bit_rate_flex_rate), "bps [", sum(bit_rate_flex_rate) / 1e9,
              "Gbps]")

        ch_occ = []
        for label in network_flex_rate.lines.keys():
            counter = 0
            line_state = network_flex_rate.lines[label].state
            for c in line_state:
                counter += c
            ch_occ.append((1 - (counter / len(line_state))) * 100)
            print(label + ":" + str((1 - (counter / len(line_state))) * 100))
        plt.figure()
        plt.bar(list(network_flex_rate.lines.keys()), ch_occ,  label='Wavelength congestion')
        plt.xticks(list(network_flex_rate.lines.keys()))
        plt.title('[Lab10] Wavelength congestion flex rate')
        plt.ylabel('Congestion [%]')
        plt.xlabel('Line label')
        plt.show()

        network_shannon = Network('../resources/nodes_full_shannon.json')
        network_shannon.connect()
        network_shannon.weighted_path = df
        network_shannon.update_routing_space(None)
        if i == 1:
            traffic_matrix_shannon = {}
            reset_traffic_matrix(traffic_matrix_shannon, network_shannon)
            # populate connections_fixed_rate array with the traffic matrix
            connections_left = node_number ** 2 - node_number
            connections_shannon = []
            while connections_left > 0:
                connections_left -= network_shannon.connections_traffic_matrix(traffic_matrix_shannon,
                                                                               connections_shannon,
                                                                               default_signal_power)
        else:
            network_shannon.stream(connections_shannon, 'snr')
        snr_shannon = [c.snr for c in connections_shannon if c.bit_rate != 0]
        plt.figure()
        plt.hist(snr_shannon, label='Snr distribution')
        plt.title('[Lab10] SNR distribution with Shannon')
        plt.ylabel('#Connections')
        plt.xlabel('SNR [dB]')
        plt.show()
        bit_rate_shannon = [c.bit_rate for c in connections_shannon if c.bit_rate != 0]
        print("Overall average bit rate with Shannon: ", st.mean(bit_rate_shannon), "bps [",
              st.mean(bit_rate_shannon) / 1e9, "Gbps]")
        print("Total capacity with Shannon: ", sum(bit_rate_shannon), "bps [", sum(bit_rate_shannon) / 1e9, "Gbps]")

        ch_occ = []
        for label in network_shannon.lines.keys():
            counter = 0
            line_state = network_shannon.lines[label].state
            for c in line_state:
                counter += c
            ch_occ.append((1 - (counter / len(line_state))) * 100)
            print(label + ":" + str((1 - (counter / len(line_state))) * 100))
        plt.figure()
        plt.bar(list(network_shannon.lines.keys()), ch_occ,  label='Wavelength congestion')
        plt.xticks(list(network_shannon.lines.keys()))
        plt.title('[Lab10] Wavelength congestion Shannon rate')
        plt.ylabel('Congestion [%]')
        plt.xlabel('Line label')
        plt.show()

        plt.figure()
        plt.hist(bit_rate_fixed_rate, label='Bit Rate Fixed Rate')
        plt.title('[Lab10] Bit rate distribution with Fixed Rate')
        plt.ylabel('#Connections')
        plt.xlabel('bit rate [bps]')
        plt.show()

        plt.figure()
        plt.hist(bit_rate_flex_rate, label='Bit Rate Flex Rate')
        plt.title('[Lab10] Bit rate distribution with Flex Rate')
        plt.ylabel('#Connections')
        plt.xlabel('bit rate [bps]')
        plt.show()

        plt.figure()
        plt.hist(bit_rate_shannon, label='Bit Rate Shannon')
        plt.title('[Lab10] Bit rate distribution with Shannon')
        plt.ylabel('#Connections')
        plt.xlabel('bit rate [bps]')
        plt.show()

        if i == 1:
            x_labels = ['A', 'B', 'C', 'D', 'E', 'F']
            y_labels = ['A', 'B', 'C', 'D', 'E', 'F']
            # Create dummy x values, with a value for every label entry
            x = np.r_[:len(x_labels)]
            y = np.r_[:len(y_labels)]
            cmap = plt.cm.jet
            cmap = copy(plt.cm.get_cmap("jet"))
            cmap.set_bad('red', 1.)

            # plot traffic matrix fixed
            a = df.from_dict(traffic_matrix_fixed).to_numpy(dtype=float, na_value=None).astype(float)
            fig, ax = plt.subplots()
            for ind1 in range(df.from_dict(traffic_matrix_fixed).shape[0]):
                for ind2 in range(df.from_dict(traffic_matrix_fixed).shape[1]):
                    text = ax.text(ind2, ind1, a[ind1, ind2],
                                   ha="center", va="center", color="w")
            # Change the xticks and yticks as desired
            plt.xticks(x, x_labels)
            plt.yticks(y, y_labels)
            plt.title("Traffic matrix Fixed Rate with M = " + str(M))
            ax.imshow(a, interpolation='nearest', cmap=cmap)

            # plot traffic matrix flex rate
            a = df.from_dict(traffic_matrix_flex).to_numpy(dtype=float, na_value=None).astype(float)
            fig, ax = plt.subplots()
            for ind1 in range(df.from_dict(traffic_matrix_flex).shape[0]):
                for ind2 in range(df.from_dict(traffic_matrix_flex).shape[1]):
                    text = ax.text(ind2, ind1, a[ind1, ind2],
                                   ha="center", va="center", color="w")
            # Change the xticks and yticks as desired
            plt.xticks(x, x_labels)
            plt.yticks(y, y_labels)
            plt.title("Traffic matrix Flex Rate with M = " + str(M))
            ax.imshow(a, interpolation='nearest', cmap=cmap)

            # plot traffic matrix shannon
            a = df.from_dict(traffic_matrix_shannon).to_numpy(dtype=float, na_value=None).astype(float)
            fig, ax = plt.subplots()
            for ind1 in range(df.from_dict(traffic_matrix_shannon).shape[0]):
                for ind2 in range(df.from_dict(traffic_matrix_shannon).shape[1]):
                    text = ax.text(ind2, ind1, a[ind1, ind2],
                                   ha="center", va="center", color="w")
            # Change the xticks and yticks as desired
            plt.xticks(x, x_labels)
            plt.yticks(y, y_labels)
            plt.title("Traffic matrix Shannon with M = " + str(M))
            ax.imshow(a, interpolation='nearest', cmap=cmap)
