from qiskit import QuantumCircuit, transpile
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi



from qiskit import QuantumCircuit, transpile
import numpy as np
from qiskit.circuit.library import RealAmplitudes
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.quantum_info import SparsePauliOp
from qiskit_aer import AerSimulator
from qiskit_aer.primitives import EstimatorV2
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi

def measure_in_xy_plane(qc, qubit, alpha, classical_bit):
    """Measure a qubit in the XY-plane at an arbitrary angle alpha."""
    qc.rz(alpha, qubit)  # Rotate around Z-axis by alpha
    qc.ry(-np.pi/2, qubit)  # Rotate into the XY-plane
    qc.measure(qubit, classical_bit)  # Standard computational basis measurement

def mbqc_pauli_x():
    """Simulates MBQC for the Pauli-X gate with explicit transpilation and classical control."""

    # Step 1: Create a 2-qubit quantum circuit
    qc = QuantumCircuit(3, 3)  # 2 qubits, 1 classical bit for measurement storage

    # Step 1: Initialize |+> states -- includes 0 to range-1
    for q in range(3):
        qc.h(q)

    qc.h(0) # Test to see if x is performed on 0
    # Step 2: Apply CZ gates to create a linear 1D cluster state
    qc.cz(0, 1)
    qc.cz(1, 2)

    # Step 3: Measurements in the XY-plane
    # Define measurement angles for -X, -Y, -Z application
    angles = [0, -np.pi, np.pi/2]

    # Adaptive measurements and dependencies
    measure_in_xy_plane(qc, 0, angles[0], 0)  # First qubit measurement J(0)
    qc.barrier()

    # Step 4: Corrections applied after measurement
    # If s1 = 1, apply X on final qubit - use the value of the measured qubit
    qc.x(1).c_if(0, 1)

    #J(pi)
    measure_in_xy_plane(qc, 1, angles[1], 1)  # Second qubit measurement J(pi)
    qc.barrier()
    qc.x(2).c_if(1, 1)  #Second conditional correction

    #MEasure the output bit
    qc.measure(2, 2)

    # Step 5: Transpile manually (since we assume no noise, this is perfect execution) SKIPPED


    # Step 6: Simulate using a perfect (noiseless) quantum simulator
    sim = AerSimulator(method='statevector')  # Perfect noiseless simulation
    transpiled_qc = transpile(qc, sim, optimization_level=0)

    #transpiled_qc.remove_final_measurements(inplace=True)  # Remove measurements for statevector
    result = sim.run(transpiled_qc, shots=1024).result()
    # final_statevector = result
    # qi.DensityMatrix(final_statevector)

    # Output the statevector (final quantum state)
    # final_state = result.get_counts(transpiled_qc)
    counts = result.get_counts(transpiled_qc)
    plot_histogram(counts, title='State counts').show()

    # plot_state_city(final_statevector, title="state vector")
    print("Counts after Pauli X:\n", counts)

    return transpiled_qc


