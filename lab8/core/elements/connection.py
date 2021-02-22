class Connection(object):
    def __init__(self, input, output, signal_power):
        self._input = input
        self._output = output
        self._signal_power = signal_power
        self._latency = 0.00
        self._snr = 0.00
        self._bit_rate = 0
    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def latency(self):
        return self._latency

    @property
    def snr(self):
        return self._snr

    @property
    def bit_rate(self):
        return self._bit_rate

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @snr.setter
    def snr(self, snr):
        self._snr = snr

    @bit_rate.setter
    def bit_rate(self, bit_rate):
        self._bit_rate = bit_rate

