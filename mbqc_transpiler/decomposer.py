from qiskit import QuantumCircuit, transpile
from mbqc_transpiler import utils
import numpy as np


def decompose_qc(qc):
    """Decomposes a given single-qubit quantum circuit into only Clifford gates."""
    if len(qc.qubits) != 1:
        raise ValueError("This function only works for single-qubit circuits.")

    # Replace arbitrary U gates with approximations
    qc_no_u = QuantumCircuit(1)
    for instr, qargs, _ in qc.data:
        if instr.name == 'u':
            theta, phi, lamb = instr.params
            approx_qc = approximate_rotation_to_clifford(theta, phi, lamb)
            qc_no_u.append(approx_qc.to_instruction(), qargs)
        else:
            qc_no_u.append(instr, qargs)
    print("Rotations approximated")

    # Transpile to Clifford-only gate set
    clifford_basis = ['h', 's', 't', 'sdg', 'x', 'y', 'z', 'cz']  # Clifford gates
    clofford_qc = transpile(qc_no_u, basis_gates=clifford_basis, optimization_level=3)

    print("decomposed to Clifford set")

    final_qc = transpile_to_H_T(clofford_qc)
    print("Fully decomposed to H and T, decomposition complete")

    return final_qc


def approximate_rotation_to_clifford(theta, phi, lamb):
    """Approximates a U(θ, φ, λ) gate using only Clifford gates."""
    qc = QuantumCircuit(1)



    print("Approximating rotations....")
    # Approximate rotations using Clifford gates only
    if utils.is_close_to_multiple(theta, np.pi/2):
        multiple = int(np.round(theta / (np.pi/2)))
        for i in range(multiple):
            qc.h(0)

    elif utils.is_close_to_multiple(theta, np.pi/4):
        multiple = int(np.round(theta / (np.pi/4)))
        for i in range(multiple):
            qc.h(0)  # Move Z-axis rotation to X-axis
            qc.t(0)  # Apply π/4 rotation
            qc.h(0)  # Move back to original basis

    if utils.is_close_to_multiple(phi, np.pi / 2):
        multiple = int(np.round(theta / (np.pi / 2)))
        for i in range(multiple):
            qc.s(0)  # S gate for phase shifts

    elif utils.is_close_to_multiple(phi, np.pi / 4):
        multiple = int(np.round(phi / (np.pi / 4)))
        for i in range(multiple):
            qc.t(0)  # S gate for phase shifts

    if utils.is_close_to_multiple(lamb, np.pi/2):
        multiple = int(np.round(theta / (np.pi/2)))
        for i in range(multiple):
            qc.h(0)

    elif utils.is_close_to_multiple(lamb, np.pi/4):
        multiple = int(np.round(theta / (np.pi/4)))
        for i in range(multiple):
            qc.h(0)  # Move Z-axis rotation to X-axis
            qc.t(0)  # Apply π/4 rotation
            qc.h(0)  # Move back to original basis

    return qc


def transpile_to_H_T(transpiled_qc):
    # Convert to H and T only by rewriting standard Clifford gates
    final_qc = QuantumCircuit(1)
    for instr, qargs, _ in transpiled_qc:
        if instr.name == 'h':
            final_qc.h(qargs[0])
        elif instr.name == 't':
            final_qc.t(qargs[0])
        elif instr.name == 'tdg':
            # Tdg = T^7
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
        elif instr.name == 'x':
            # X = HTH
            final_qc.h(qargs[0])
            final_qc.t(qargs[0])
            final_qc.h(qargs[0])
        elif instr.name == 'y':
            #S
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            #X
            final_qc.h(qargs[0])
            final_qc.t(qargs[0])
            final_qc.h(qargs[0])
            #Sdg
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
        elif instr.name == 'z':
            # Z = THTHT
            final_qc.t(qargs[0])
            final_qc.h(qargs[0])
            final_qc.t(qargs[0])
            final_qc.h(qargs[0])
            final_qc.t(qargs[0])
        elif instr.name == 's':
            # S = T^2
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
        elif instr.name == 'sdg':
            # Sdg = (T)^6
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
            final_qc.t(qargs[0])
        else:
            raise ValueError(f"Unsupported gate: {instr.name}")

    return final_qc