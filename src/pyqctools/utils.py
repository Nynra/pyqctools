from kaleidoscope.interactive import probability_distribution, bloch_sphere, qsphere, bloch_disc, bloch_multi_disc
from qiskit.quantum_info import Statevector, random_statevector
from qiskit import QuantumCircuit
from typing import Tuple


def state_to_dirac(state: Statevector) -> str:
    """Convert a statevector to Dirac notation.

    This function accepts an arbitrary state vector and prints
    it in its corresponding Dirac notation

    Parameters
    ----------
    state : Statevector
        The state vector to be converted to Dirac notation.

    Returns
    -------
    str
        The state vector in Dirac notation.
    """
    if not isinstance(state, Statevector):
        raise TypeError("The state must be a Statevector object not {}.".format(type(state)))
    
    # Convert the statevector to dictionary form.
    state_to_dict = state.to_dict()

    return " ".join(
        "{1:+.4f}|{0}>".format(key, value) for key, value in state_to_dict.items()
    )


# Function: simulate_circuit_and_obtain_vector(quantum_circuit, number_shots)
def simulate_circuit_and_obtain_vector(qc: QuantumCircuit, randomize_init:bool=False) -> Tuple[Statevector, str]:
    """Simulate a quantum circuit and obtain the resulting state vector.

    This function accepts an arbitrary circuit, performs its
    state vector simulation and returns the resulting vector
    state as a [x, y, z] vector that could be plotted

    .. attention::

        This function does not support circuits with measurements as
        this requires classical bits to save the data to.

    Parameters
    ----------
    qc : QuantumCircuit
        The quantum circuit to be simulated.
    randomize_init : bool
        If True, the initial state will be randomized. Default is False.

    Returns
    -------
    Statevector
        The resulting state vector of the simulation.
    """
    if not isinstance(qc, QuantumCircuit):
        raise TypeError("The circuit must be a QuantumCircuit object not {}.".format(type(qc)))
    if not isinstance(randomize_init, bool):
        raise TypeError("The randomize_init must be a boolean not {}.".format(type(randomize_init)))

    if randomize_init:
        state_vector = random_statevector(2**qc.num_qubits)
        state_vector.evolve(qc)
    else:
        state_vector = Statevector.from_instruction(qc)

    # Convert the resulting state vector in its Dirac notation
    dirac_vector = state_to_dirac(state_vector)

    return state_vector, dirac_vector


if __name__ == "__main__":
    # Test the functions
    qc_test = QuantumCircuit(2)
    qc_test.h(0)
    test_state, test_dirac = simulate_circuit_and_obtain_vector(qc_test)
    bloch_sphere(test_state)

