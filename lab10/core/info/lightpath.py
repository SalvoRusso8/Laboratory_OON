from lab10.core.info.signalInformation import SignalInformation

Rs = 32e9  # [Hz] symbol rate
df = 50e9  # [Hz] frequency spacing


class Lightpath(SignalInformation):
    def __init__(self, power, path, channel):
        self._signal_power = power
        self._path = path
        self._noise_power = 0
        self._latency = 0
        self._channel = channel
        self._symbol_rate = Rs
        self._df = df
        self._isnr = 0.0

    @property
    def channel(self):
        return self._channel

    @property
    def symbol_rate(self):
        return self._symbol_rate

    @property
    def df(self):
        return self._df

    @channel.setter
    def channel(self, channel):
        self._channel = channel

