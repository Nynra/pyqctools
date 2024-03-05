from qiskit import QuantumCircuit, execute
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
from qiskit_ibm_runtime import Options, QiskitRuntimeService
from qiskit import transpile

# Set the QtAgg backend for matplotlib
plt.switch_backend('QtAgg')

# Define a function to create a quantum eraser circuit
def quantum_eraser() -> QuantumCircuit:
    """Create a simple quantum eraser circuit.

    The circuit consists of a Hadamard gate to simulate a 50/50 beam splitter,
    followed by a controlled-X gate to simulate a Mach-Zehnder interferometer.
    The simulated setup does not contain any polarizers or a wiper.

    Parameters:
    -----------
    use_wiper: bool
        Whether to include the wiper in the circuit.

    Returns:
    --------
    QuantumCircuit
        The quantum eraser circuit.
    """
    # Generate a circuit corresponding with a quantum eraser
    # experiment in a mach-zehnder interferometer
    qc = QuantumCircuit(2, 2)
    qc.h(0)  # Apply a Hadamard gate to qubit 0 to simulate a 50/50 beam splitter
    qc.cx(0, 1)  # Apply a controlled-X gate to qubit 1, controlled by qubit 0

    # Measure the qubits
    qc.measure([0, 1], [0, 1])
    return qc


def quantum_bomb_tester() -> QuantumCircuit:
    """Create a simple quantum bomb tester circuit.

    The circuit consists of a Hadamard gate to simulate a 50/50 beam splitter,
    followed by a controlled-X gate to simulate the recombination of the two
    paths.

    Returns:
    --------
    QuantumCircuit
        The quantum bomb tester circuit.
    """
    pass


if __name__ == "__main__":
    # Create a quantum eraser circuit
    qc = quantum_eraser()

    # Draw the circuit
    qc.draw(output='mpl')
    plt.show()

    # Log into the IBM quantum service
    service = QiskitRuntimeService()
    simulator = service.get_backend('ibmq_qasm_simulator')

    # Execute the quantum eraser circuit
    job = transpile(qc, simulator)
    result = simulator.run(job).result().get_counts()

    # Plot the results
    plot_histogram(result)
    plt.ylabel('$Counts$ [-]')
    plt.xlabel('$State$ [-]')
    plt.show()

    