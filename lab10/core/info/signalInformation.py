Rs = 32e9  # [Hz] symbol rate
df = 50e9  # [Hz] frequency spacing


class SignalInformation(object):
    def __init__(self, power, path):
        self._signal_power = power
        self._path = path
        self._noise_power = 0
        self._latency = 0
        self._symbol_rate = Rs
        self._df = df
        self._isnr = 0.0

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def path(self):
        return self._path

    @property
    def noise_power(self):
        return self._noise_power

    @property
    def latency(self):
        return self._latency

    @property
    def symbol_rate(self):
        return self._symbol_rate

    @property
    def df(self):
        return self._df

    @property
    def isnr(self):
        return self._isnr

    @signal_power.setter
    def signal_power(self, signal_power):
        self._signal_power = signal_power

    @path.setter
    def path(self, path):
        self._path = path

    @noise_power.setter
    def noise_power(self, noise_power):
        self._noise_power = noise_power

    @latency.setter
    def latency(self, latency):
        self._latency = latency

    @isnr.setter
    def isnr(self, isnr):
        self._isnr = isnr

    def add_noise(self, noise):
        self.noise_power += noise

    def add_latency(self, latency):
        self.latency += latency

    def next(self):
        self.path = self.path[1:]
