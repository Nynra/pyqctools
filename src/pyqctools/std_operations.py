import numpy as np
from typing import List


def get_initial_state(states=List[int]) -> np.array:
    """Get the initial state for a given number of qbits states."""
    if not isinstance(states, list):
        raise TypeError('States must be a list not type {}'.format(type(states)))
    if not all(isinstance(x, int) for x in states):
        raise TypeError('States must be a list of integers')
    if not all(x in [0, 1] for x in states):
        raise ValueError('States must be a list of non-negative integers')
    zero_bit = np.array([1, 0])
    one_bit = np.array([0, 1])

    # Calculate the resulting matrix using the kronecker product
    result = zero_bit if states[0] == 0 else one_bit
    for i in range(1, len(states)):
        result = np.kron(result, zero_bit if states[i] == 0 else one_bit)
    return result


class SingleQbitGate:
    # Some basic gates
    X = np.array([[0, 1], [1, 0]])
    Y = np.array([[0, -1j], [1j, 0]])
    Z = np.array([[1, 0], [0, -1]])
    H = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
    S = np.array([[1, 0], [0, 1j]])
    T = np.array([[1, 0], [0, np.exp(1j * np.pi / 4)]])
    I = np.eye(2)

    def get_operator(self, operator:str) -> np.array:
        if not isinstance(operator, str):
            raise TypeError('Operator must be a string not type {}'.format(type(operator)))
        match operator.lower():
            case "x":
                return self.X
            case "y":
                return self.Y
            case "z":
                return self.Z
            case "h":
                return self.H
            case "s":
                return self.S
            case "t":
                return self.T
            case "i":
                return self.I
            case _:
                raise ValueError(f'Operator {operator} not supported')


class TwoQbitGate:
    SWAP = np.array([
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1]
    ])
    
    def __init__(self) -> ...:
        self._single_gates = SingleQbitGate()

    def create_controlled_matrix(self, operator:str, control:int, target:int) -> np.array:
        """Create a controlled matrix for a given operator"""
        operator_array = self._single_gates.get_operator(operator)
        if control == target:
            raise ValueError('Control and target must be different')
        if control not in [0, 1] or target not in [0, 1]:
            raise ValueError('Control and target must be 0 or 1')
        if operator_array.shape != (2, 2):
            raise ValueError('Operator must be a single qbit operator')
        if control == 0:
            return np.array([
                [1, 0, 0, 0],
                [0, 1, 0, 0],
                [0, 0, operator_array[0, 0], operator_array[0, 1]],
                [0, 0, operator_array[1, 0], operator_array[1, 1]]
            ])
        else:
            return np.array([
                [operator_array[0, 0], operator_array[0, 1], 0, 0],
                [operator_array[1, 0], operator_array[1, 1], 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ])

    