import dataclasses
import numpy as np
from simulation_controller import Component


@dataclasses.dataclass
class TsodyksMarkramSynapse(Component):
    A: float
    U: float
    tau_f: float
    tau_d: float
    tau_s: float
    spikes: list[float] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.u: float = 0
        self.x: float = 1
        self.I: float = 0
        self.t: float = 0

    def init(self, t0, dt, tmax):
        self.__post_init__()
        self.spike_bins = iter(
            np.histogram(self.spikes, int(tmax // dt) + 2, range=(0, tmax))[0]
        )

    def step(self, dt):
        self._n_spikes = next(self.spike_bins)
        self.u += self.du(dt)
        self.I += self.dI(dt)
        self.x += self.dx(dt)

    def du(self, dt):
        return -self.u / self.tau_f * dt + self.U * (1 - self.u) * self._n_spikes

    def dx(self, dt):
        return (1 - self.x) / self.tau_d * dt - self.u * self.x * self._n_spikes

    def dI(self, dt):
        return -self.I / self.tau_s * dt + self.A * self.u * self.x * self._n_spikes

    def u_monitor(self):
        return self.u

    def x_monitor(self):
        return self.x

    def I_monitor(self):
        return self.I

    def output(self):
        return self.I
