import dataclasses
from simulation_controller import Component


@dataclasses.dataclass
class Cell(Component):
    Cm: float
    V_reset: float
    threshold: float
    inputs: list[Component] = dataclasses.field(default_factory=list)

    def init(self, t0, dt, tmax):
        self.V = self.V_reset

    def step(self, dt):
        self.V += sum(input.output() for input in self.inputs) / self.Cm
        if self.V > self.threshold:
            self.V = self.V_reset
            self.spiked = True
        else:
            self.spiked = False

    def receive_from(self, synapse: Component):
        self.inputs.append(synapse)

    def V_monitor(self):
        return self.V

    def output(self):
        return getattr(self, "spiked", False)
