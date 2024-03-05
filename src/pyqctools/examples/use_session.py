from qiskit_ibm_runtime import QiskitRuntimeService, Session, Options, Estimator
from qiskit.quantum_info import SparsePauliOp
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np
from src.pyqctools.login_ibm import login_to_ibm

service = login_to_ibm()
options = Options(optimization_level=1)
options.execution.shots = 1024  # Options can be set using auto-complete.

# 1. A quantum circuit for preparing the quantum state (|000> + e^{itheta} |111>)/rt{2}
theta = Parameter('θ')
qc_example = QuantumCircuit(3)
qc_example.h(0) # generate superpostion
qc_example.p(theta,0) # add quantum phase
qc_example.cx(0, 1) # condition 1st qubit on 0th qubit
qc_example.cx(0, 2) # condition 2nd qubit on 0th qubit

# 2. the observable to be measured
M1 = SparsePauliOp.from_list([("XXY", 1), ("XYX", 1), ("YXX", 1), ("YYY", -1)])


gr = (np.sqrt(5) + 1) / 2 # golden ratio
thetaa = 0 # lower range of theta
thetab = 2*np.pi # upper range of theta
tol = 1e-1 # tol

# 3. Execute iteratively using the Estimator primitive
with Session(service=service, backend="ibmq_qasm_simulator") as session:
    estimator = Estimator(session=session, options=options)
    #next test range
    thetac = thetab - (thetab - thetaa) / gr
    thetad = thetaa + (thetab - thetaa) / gr
    while abs(thetab - thetaa) > tol:
        print(f"max value of M1 is in the range theta = {[thetaa, thetab]}")
        job = estimator.run(circuits=[qc_example]*2, observables=[M1]*2, parameter_values=[[thetac],[thetad]])
        test =job.result().values
        if test[0] > test[1]:
            thetab = thetad
        else:
            thetaa = thetac
        thetac = thetab - (thetab - thetaa) / gr
        thetad = thetaa + (thetab - thetaa) / gr

    # Final job to evaluate Estimator at midpoint found using golden search method
    theta_mid = (thetab + thetaa) / 2
    job = estimator.run(circuits=qc_example, observables=M1, parameter_values=theta_mid)
    print(f"Session ID is {session.session_id}")
    print(f"Final Job ID is {job.job_id()}")
    print(f"Job result is {job.result().values} at theta = {theta_mid}")