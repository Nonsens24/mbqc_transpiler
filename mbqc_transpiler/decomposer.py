from qiskit import QuantumCircuit, transpile
from qiskit.circuit.equivalence_library import SessionEquivalenceLibrary
from qiskit.quantum_info import Operator
from qiskit.transpiler.passes import Decompose
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
    clifford_basis = ['h', 's', 'sdg', 'x', 'y', 'z', 'cz']  # Clifford gates
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
    if np.isclose(theta, np.pi / 2):
        qc.h(0)  # Hadamard for π/2 rotations
    if np.isclose(phi, np.pi / 2):
        qc.s(0)  # S gate for phase shifts
    if np.isclose(lamb, np.pi / 2):
        qc.s(0)
    if np.isclose(phi, np.pi):
        qc.z(0)  # Pauli-Z for π phase shift
    if np.isclose(lamb, np.pi):
        qc.z(0)
    if np.isclose(theta, np.pi):
        qc.x(0)  # Pauli-X for π rotations

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