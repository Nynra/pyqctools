from qiskit.quantum_info import Statevector, random_statevector
from qiskit import QuantumCircuit
from kaleidoscope.interactive import probability_distribution, bloch_sphere, qsphere, bloch_disc, bloch_multi_disc

qc_prep = QuantumCircuit(2)
qc_prep.h(0)
qc_prep.cx(0, 1)
print("Bell state preparation circuit:")
print(qc_prep)


print("When reveiving a bell state the state can be corrected using the Z and X gate:")
print("Psi+ = |00> + |11>")
print("Psi- = |00> - |11> -> X0Z0 -> |00> + |11>")
print("Phi+ = |01> + |10> -> Z0 -> |00> + |11>")
print("Phi- = |01> - |10> -> X0 -> |00> + |11>")