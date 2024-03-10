from simulation_controller import *
from neuron_integrate_fire import Cell
from synapse_tsodyks_markram import TsodyksMarkramSynapse

sim = Simulator()

syn = TsodyksMarkramSynapse(A=1, U=0.45, tau_f=0.05, tau_d=0.75, tau_s=0.02, spikes=[0.02, 0.085, 0.15, 0.2, 0.23])
cell = Cell(Cm=1, V_reset=-70, threshold=-50)
cell.receive_from(syn)

sim.add_component(syn)
sim.add_component(cell)
sim.add_monitor('Current', monitor=syn.I_monitor)
sim.add_monitor('U', monitor=syn.u_monitor)
sim.add_monitor('X', monitor=syn.x_monitor)
sim.add_monitor('V', monitor=cell.V_monitor)

sim.run(0, 0.3, 0.001)
sim.save('test.html')