from qiskit_ibm_runtime import QiskitRuntimeService, Options, Sampler
from qiskit import QuantumCircuit
from src.pyqctools.login_ibm import login_to_ibm

service = login_to_ibm()
options = Options(optimization_level=1)
options.execution.shots = 1024  # Options can be set using auto-complete.

# 1. A quantum circuit for preparing the quantum state (|00> + |11>)/rt{2}
bell = QuantumCircuit(2)
bell.h(0)
bell.cx(0, 1)

# 2. Map the qubits to a classical register in ascending order
bell.measure_all()

# 3. Execute using the Sampler primitive
backend = service.get_backend('ibmq_qasm_simulator')
sampler = Sampler(backend=backend, options=options)
job = sampler.run(circuits=bell)
print(f"Job ID is {job.job_id()}")
print(f"Job result is {job.result()}")