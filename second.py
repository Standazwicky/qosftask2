from qiskit import QuantumCircuit, Aer, execute
import numpy as np
from qiskit.tools.visualization import plot_histogram
from qiskit.quantum_info import Operator
from qiskit.providers.aer import QasmSimulator
from qiskit.providers.aer.noise import NoiseModel
from qiskit.providers.aer.noise import QuantumError
from qiskit.providers.aer.noise import pauli_error

p_bitflip=0.3       #Probability of bit-flip
p_signflip=0.1      #Probability of sign-flip


#Creating quantum circuit
qc=QuantumCircuit(2,2)
qc.h(0)
qc_op=Operator([[1,0],[0,1]])    #Unit operator
qc.unitary(qc_op,[0],label='qc_op')   #add unitary gate on q0 state, were noise will be added
qc.unitary(qc_op,[1],label='qc_op')   #add unitary gate on q0 state, were noise will be added
qc.cx(0,1)
qc.measure([0,1],[0,1])


'unitary' in QasmSimulator().configuration().basis_gates  #allows us to add noise models to arbitrary unitaries

#Quantum Error objects
bit_flip  =pauli_error([('X',p_bitflip),('I',1-p_bitflip)])
phase_flip=pauli_error([('Z',p_signflip),('I',1-p_signflip)])
#Composition of bit-flip and phase-flip error
error_gate=bit_flip.compose(phase_flip)


# Add errors to noise model
noise_bf_sf=NoiseModel()
noise_bf_sf.add_all_qubit_quantum_error(error_gate,'qc_op')
noise_bf_sf.add_basis_gates(['unitary'])


qc.draw()


job=execute(qc,QasmSimulator(noise_model=noise_bf_sf))
result_bf_sf = job.result()
counts_bf_sf = result_bf_sf.get_counts(0)
plt=plot_histogram(counts_bf_sf,title='noise Bell-State counts')
plt.savefig('bla.png')
