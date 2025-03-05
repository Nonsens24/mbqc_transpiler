from qiskit import QuantumCircuit, transpile
import numpy as np
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
import qiskit.quantum_info as qi


from qiskit.result import marginal_counts
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
    print("Example: MBQC Pauli X")

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
    angles = [0, -np.pi]

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

    # **Save the final state before measuring the output qubit**
    qc.save_density_matrix()

    #MEasure the output bit
    qc.measure(2, 2)

    # Step 5: Transpile manually (since we assume no noise, this is perfect execution) SKIPPED


    # Step 6: Simulate using a perfect (noiseless) quantum simulator
    sim = AerSimulator(method='density_matrix')  # Perfect noiseless simulation
    transpiled_qc = transpile(qc, sim, optimization_level=0)

    #transpiled_qc.remove_final_measurements(inplace=True)  # Remove measurements for statevector
    result = sim.run(transpiled_qc, shots=1024).result()

    full_density_matrix = result.data()["density_matrix"]

    # print("Full density matrix: \n", full_density_matrix)
    # Extract only the output qubit (qubit 2)
    reduced_density_matrix = qi.partial_trace(full_density_matrix, [0, 1])

    # Print the final output qubit state
    print("Output Qubit State (Density Matrix):\n", reduced_density_matrix)

    # Output the statevector (final quantum state)
    # final_state = result.get_counts(transpiled_qc)
    counts = result.get_counts(transpiled_qc)
    plot_histogram(counts, title='State counts').show()

    # plot_state_city(final_statevector, title="state vector")
    # print("Counts after Pauli X:\n", counts)

    return transpiled_qc

def mbqc_arbitrary_x(alpha, graph = True):
    """Simulates MBQC for the Pauli-X gate with explicit transpilation and classical control."""
    print("Example: MBQC arbitrary X-rotation")

    # Step 1: Create a 2-qubit quantum circuit
    qc = QuantumCircuit(3, 3)  # 2 qubits, 1 classical bit for measurement storage

    # Step 1: Initialize |+> states -- includes 0 to range-1
    for q in range(3):
        qc.h(q)

    qc.h(0)  # Test to see if x is performed on 0
    # Step 2: Apply CZ gates to create a linear 1D cluster state
    qc.cz(0, 1)
    qc.cz(1, 2)

    # Step 3: Measurements in the XY-plane
    # Define measurement angles for -X, -Y, -Z application
    angles = [0, -alpha]

    # Adaptive measurements and dependencies
    measure_in_xy_plane(qc, 0, angles[0], 0)  # First qubit measurement J(0)
    qc.barrier()

    # Step 4: Corrections applied after measurement
    # If s1 = 1, apply X on final qubit - use the value of the measured qubit
    qc.x(1).c_if(0, 1)

    # J(pi)
    measure_in_xy_plane(qc, 1, angles[1], 1)  # Second qubit measurement J(pi)
    qc.barrier()
    qc.x(2).c_if(1, 1)  # Second conditional correction

    # **Save the final state before measuring the output qubit**
    qc.save_density_matrix()

    if graph:
        # MEasure the output bit
        qc.measure(2, 2)

    # Step 5: Transpile manually (since we assume no noise, this is perfect execution) SKIPPED

    # Step 6: Simulate using a perfect (noiseless) quantum simulator
    sim = AerSimulator(method='density_matrix')  # Perfect noiseless simulation
    transpiled_qc = transpile(qc, sim, optimization_level=0)

    # transpiled_qc.remove_final_measurements(inplace=True)  # Remove measurements for statevector
    result = sim.run(transpiled_qc, shots=1024).result()
    # final_statevector = result
    # qi.DensityMatrix(final_statevector)
    full_density_matrix = result.data()["density_matrix"]

    # print("Full density matrix: \n", full_density_matrix)
    # Extract only the output qubit (qubit 2)
    reduced_density_matrix = qi.partial_trace(full_density_matrix, [0, 1])

    # Print the final output qubit state
    print("Output Qubit State (Density Matrix):\n", reduced_density_matrix)

    # Output the statevector (final quantum state)
    # final_state = result.get_counts(transpiled_qc)
    counts = result.get_counts(transpiled_qc)
    plot_histogram(counts, title='State counts').show()

    # plot_state_city(final_statevector, title="state vector")
    # print("Counts after Pauli X:\n", counts)

    return transpiled_qc

def mbqc_arbitrary_z(alpha, graph = True):
    """Simulates MBQC for the Pauli-X gate with explicit transpilation and classical control."""
    print("Example: MBQC arbitrary X-rotation")

    # Step 1: Create a 2-qubit quantum circuit
    qc = QuantumCircuit(3, 3)  # 2 qubits, 1 classical bit for measurement storage

    # Step 1: Initialize |+> states -- includes 0 to range-1
    for q in range(3):
        qc.h(q)

    qc.h(0)  # Test to see if x is performed on 0
    # Step 2: Apply CZ gates to create a linear 1D cluster state
    qc.cz(0, 1)
    qc.cz(1, 2)

    # Step 3: Measurements in the XY-plane
    # Define measurement angles for -X, -Y, -Z application
    angles = [-alpha, 0]

    # Adaptive measurements and dependencies
    measure_in_xy_plane(qc, 0, angles[0], 0)  # First qubit measurement J(0)
    qc.barrier()

    # Step 4: Corrections applied after measurement
    # If s1 = 1, apply X on final qubit - use the value of the measured qubit
    qc.x(1).c_if(0, 1)

    # J(pi)
    measure_in_xy_plane(qc, 1, angles[1], 1)  # Second qubit measurement J(pi)
    qc.barrier()
    qc.x(2).c_if(1, 1)  # Second conditional correction

    # **Save the final state before measuring the output qubit**
    qc.save_density_matrix()

    if graph:
        # MEasure the output bit
        qc.measure(2, 2)

    # Step 5: Transpile manually (since we assume no noise, this is perfect execution) SKIPPED

    # Step 6: Simulate using a perfect (noiseless) quantum simulator
    sim = AerSimulator(method='density_matrix')  # Perfect noiseless simulation
    transpiled_qc = transpile(qc, sim, optimization_level=0)

    # transpiled_qc.remove_final_measurements(inplace=True)  # Remove measurements for statevector
    result = sim.run(transpiled_qc, shots=1024).result()
    # final_statevector = result
    # qi.DensityMatrix(final_statevector)
    full_density_matrix = result.data()["density_matrix"]

    # print("Full density matrix: \n", full_density_matrix)
    # Extract only the output qubit (qubit 2)
    reduced_density_matrix = qi.partial_trace(full_density_matrix, [0, 1])

    # Print the final output qubit state
    print("Output Qubit State (Density Matrix):\n", reduced_density_matrix)

    # Output the statevector (final quantum state)
    # final_state = result.get_counts(transpiled_qc)
    counts = result.get_counts(transpiled_qc)
    plot_histogram(counts, title='State counts').show()

    # plot_state_city(final_statevector, title="state vector")
    # print("Counts after Pauli X:\n", counts)

    return transpiled_qc

def mbqc_arbitrary_u(alpha, beta, gamma):
    """Simulates MBQC for the Pauli-X gate with explicit transpilation and classical control."""
    print("Example: MBQC arbitrary U-rotation")

    # Step 1: Create a 2-qubit quantum circuit
    qc = QuantumCircuit(7, 7)  # 2 qubits, 1 classical bit for measurement storage

    # Step 1: Initialize |+> states -- includes 0 to range-1
    for q in range(7):
        qc.h(q)

    qc.h(0)  # Test to see if x is performed on 0
    # Step 2: Apply CZ gates to create a linear 1D cluster state
    for q in range(6):  # Apply CZ between consecutive qubits
        qc.cz(q, q + 1)

    #Rz
    # Define measurement angles for -X, -Y, -Z application
    angles = [-alpha, 0, 0, -beta, -gamma, 0]

    #Propagate
    for i in range(6):  # Measure first 6 qubits
        measure_in_xy_plane(qc, i, angles[i], i)
        qc.barrier()
        if i < 6:  # Conditional correction on the next qubit
            qc.x(i + 1).c_if(qc.cregs[0], 1)

    # **Save the final state before measuring the output qubit**
    qc.save_density_matrix()

    # MEasure the output bit
    qc.measure(6, 6)

    # Step 5: Transpile manually (since we assume no noise, this is perfect execution) SKIPPED

    # Step 6: Simulate using a perfect (noiseless) quantum simulator
    sim = AerSimulator(method='density_matrix')  # Perfect noiseless simulation
    transpiled_qc = transpile(qc, sim, optimization_level=0)

    # transpiled_qc.remove_final_measurements(inplace=True)  # Remove measurements for statevector
    result = sim.run(transpiled_qc, shots=1024).result()
    # final_statevector = result
    # qi.DensityMatrix(final_statevector)
    full_density_matrix = result.data()["density_matrix"]

    #DM after RzRxRz
    reduced_density_matrix = qi.partial_trace(full_density_matrix, [0, 1, 2, 3, 4, 5])
    print("Output Qubit State (Density Matrix) after RzRxRz (angles = ", alpha, beta, gamma, ":\n", reduced_density_matrix)

    # Output the statevector (final quantum state)
    # final_state = result.get_counts(transpiled_qc)
    counts = result.get_counts(transpiled_qc)
    counts_q7 = marginal_counts(counts, [6])
    plot_histogram(counts_q7, title='State counts').show()

    # plot_state_city(final_statevector, title="state vector")
    # print("Counts after Pauli X:\n", counts)

    return transpiled_qc

def mbqc_hadamard():
    """Simulates MBQC for the Pauli-X gate with explicit transpilation and classical control."""
    print("Example: MBQC Hadamard")

    # Step 1: Create a 2-qubit quantum circuit
    qc = QuantumCircuit(3, 3)  # 2 qubits, 1 classical bit for measurement storage

    # Step 1: Initialize |+> states -- includes 0 to range-1
    for q in range(3):
        qc.h(q)

    qc.h(0) # Test to see if x is performed on 0
    # Step 2: Apply CZ gates to create a linear 1D cluster state
    qc.cz(0, 1)

    # Step 3: Measurements in the XY-plane
    # Define measurement angles for -X, -Y, -Z application
    angles = [0]

    # Adaptive measurements and dependencies
    measure_in_xy_plane(qc, 0, angles[0], 0)  # First qubit measurement J(0)
    qc.barrier()

    # Step 4: Corrections applied after measurement
    # If s1 = 1, apply X on final qubit - use the value of the measured qubit
    qc.x(1).c_if(0, 1)

    # **Save the final state before measuring the output qubit**
    qc.save_density_matrix()

    #MEasure the output bit
    qc.measure(2, 2)

    # Step 5: Transpile manually (since we assume no noise, this is perfect execution) SKIPPED


    # Step 6: Simulate using a perfect (noiseless) quantum simulator
    sim = AerSimulator(method='density_matrix')  # Perfect noiseless simulation
    transpiled_qc = transpile(qc, sim, optimization_level=0)

    #transpiled_qc.remove_final_measurements(inplace=True)  # Remove measurements for statevector
    result = sim.run(transpiled_qc, shots=1024).result()

    full_density_matrix = result.data()["density_matrix"]

    # print("Full density matrix: \n", full_density_matrix)
    # Extract only the output qubit (qubit 2)
    reduced_density_matrix = qi.partial_trace(full_density_matrix, [0, 1])

    # Print the final output qubit state
    print("Output Qubit State (Density Matrix):\n", reduced_density_matrix)

    # Output the statevector (final quantum state)
    # final_state = result.get_counts(transpiled_qc)
    counts = result.get_counts(transpiled_qc)
    plot_histogram(counts, title='State counts').show()

    # plot_state_city(final_statevector, title="state vector")
    # print("Counts after Pauli X:\n", counts)

    return transpiled_qc

