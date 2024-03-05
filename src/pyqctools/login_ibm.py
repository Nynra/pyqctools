from qiskit_ibm_runtime import QiskitRuntimeService


def login_to_ibm(save_to_disk: bool = False, token=str) -> QiskitRuntimeService:
    """Log into the IBM quantum service."""
    if not isinstance(save_to_disk, bool):
        raise TypeError(
            "The save_to_disk must be a boolean not {}.".format(type(save_to_disk))
        )
    if not isinstance(token, str):
        raise TypeError("The token must be a string not {}.".format(type(token)))

    channel = "ibm_quantum"

    if save_to_disk:
        print("WARNING: Saving the token to disk is not secure.")
        service = QiskitRuntimeService.save_account(token=token, channel=channel)
    else:
        service = QiskitRuntimeService(token=token, channel=channel, verify=True)
    return service

