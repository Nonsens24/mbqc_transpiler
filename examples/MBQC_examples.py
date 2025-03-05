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
from fractions import Fraction

def format_angle(angle):
    frac = Fraction(angle / np.pi).limit_denominator(100)  # Convert to fraction of π
    return f"{frac.numerator}π/{frac.denominator}" if frac.denominator != 1 else f"{frac.numerator}π"

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
    qc.x(0)
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


def mbqc_arbitrary_z(alpha, graph=True):
    """Simulates MBQC for an arbitrary Z-rotation using a linear cluster state."""
    print("Example: MBQC Arbitrary Z-Rotation")

    # Step 1: Create a 3-qubit quantum circuit (2 ancillas + 1 logical output)
    qc = QuantumCircuit(3, 3)  # 3 qubits, 3 classical bits for measurement storage

    # Step 2: Initialize |+> states for all qubits
    for q in range(3):
        qc.h(q)

    # Step 3: Apply Controlled-Z (CZ) gates to create a 1D cluster state
    qc.cz(0, 1)
    qc.cz(1, 2)

    # Step 4: Measurements in the XY-plane
    # Measurement angles for Z-rotation implementation
    angles = [-alpha, 0]

    # Perform measurement on qubit 0 in the XY-plane at angle -alpha
    measure_in_xy_plane(qc, 0, angles[0], 0)
    qc.barrier()

    # Adaptive correction based on measurement result (s_0)
    qc.x(1).c_if(0, 1)  # Apply Z correction if s_0 = 1

    # Measure qubit 1 in the XY-plane at angle 0 (i.e., standard measurement)
    measure_in_xy_plane(qc, 1, angles[1], 1)
    qc.barrier()

    # Final adaptive correction based on second measurement result (s_1)
    qc.x(2).c_if(1, 1)  # Apply X correction if s_1 = 1

    # Step 5: Save the final logical qubit's density matrix before final measurement
    qc.save_density_matrix()

    if graph:
        # Measure the output qubit to verify the results
        qc.measure(2, 2)

    # Step 6: Simulate using a perfect (noiseless) quantum simulator
    sim = AerSimulator(method='density_matrix')  # Use noiseless simulator
    transpiled_qc = transpile(qc, sim, optimization_level=0)

    # Run the simulation and extract the final quantum state
    result = sim.run(transpiled_qc, shots=1024).result()
    full_density_matrix = result.data()["density_matrix"]

    # Extract only the logical output qubit's state (tracing out qubits 0 and 1)
    reduced_density_matrix = qi.partial_trace(full_density_matrix, [0, 1])

    # Print the final output qubit's state
    print("Output Qubit State (Density Matrix):\n", reduced_density_matrix)

    # Plot measurement results if graphing is enabled
    counts = result.get_counts(transpiled_qc)
    plot_histogram(counts, title='State counts').show()

    return transpiled_qc

# def mbqc_arbitrary_z(alpha, graph = True):
#     """Simulates MBQC for the Pauli-X gate with explicit transpilation and classical control."""
#     print("Example: MBQC arbitrary X-rotation")
#
#     # Step 1: Create a 2-qubit quantum circuit
#     qc = QuantumCircuit(3, 3)  # 2 qubits, 1 classical bit for measurement storage
#
#     # Step 1: Initialize |+> states -- includes 0 to range-1
#     for q in range(3):
#         qc.h(q)
#
#     qc.h(0)  # Test to see if x is performed on 0
#     # Step 2: Apply CZ gates to create a linear 1D cluster state
#     qc.cz(0, 1)
#     qc.cz(1, 2)
#
#     # Step 3: Measurements in the XY-plane
#     # Define measurement angles for -X, -Y, -Z application
#     angles = [-alpha, 0]
#
#     # Adaptive measurements and dependencies
#     measure_in_xy_plane(qc, 0, angles[0], 0)  # First qubit measurement J(0)
#     qc.barrier()
#
#     # Step 4: Corrections applied after measurement
#     # If s1 = 1, apply X on final qubit - use the value of the measured qubit
#     qc.x(1).c_if(0, 1)
#
#     # J(pi)
#     measure_in_xy_plane(qc, 1, angles[1], 1)  # Second qubit measurement J(pi)
#     qc.barrier()
#     qc.x(2).c_if(1, 1)  # Second conditional correction
#
#     # **Save the final state before measuring the output qubit**
#     qc.save_density_matrix()
#
#     if graph:
#         # MEasure the output bit
#         qc.measure(2, 2)
#
#     # Step 5: Transpile manually (since we assume no noise, this is perfect execution) SKIPPED
#
#     # Step 6: Simulate using a perfect (noiseless) quantum simulator
#     sim = AerSimulator(method='density_matrix')  # Perfect noiseless simulation
#     transpiled_qc = transpile(qc, sim, optimization_level=0)
#
#     # transpiled_qc.remove_final_measurements(inplace=True)  # Remove measurements for statevector
#     result = sim.run(transpiled_qc, shots=1024).result()
#     # final_statevector = result
#     # qi.DensityMatrix(final_statevector)
#     full_density_matrix = result.data()["density_matrix"]
#
#     # print("Full density matrix: \n", full_density_matrix)
#     # Extract only the output qubit (qubit 2)
#     reduced_density_matrix = qi.partial_trace(full_density_matrix, [0, 1])
#
#     # Print the final output qubit state
#     print("Output Qubit State (Density Matrix):\n", reduced_density_matrix)
#
#     # Output the statevector (final quantum state)
#     # final_state = result.get_counts(transpiled_qc)
#     counts = result.get_counts(transpiled_qc)
#     plot_histogram(counts, title='State counts').show()
#
#     # plot_state_city(final_statevector, title="state vector")
#     # print("Counts after Pauli X:\n", counts)
#
#     return transpiled_qc

def mbqc_arbitrary_u(alpha, beta, gamma):
    """Simulates MBQC for the Pauli-X gate with explicit transpilation and classical control."""
    print("Example: MBQC arbitrary U-rotation")

    # Step 1: Create a 2-qubit quantum circuit
    qc = QuantumCircuit(7, 7)  # 2 qubits, 1 classical bit for measurement storage

    # Step 1: Initialize |+> states -- includes 0 to range-1
    for q in range(7):
        qc.h(q)

    qc.h(0)  # Test to see if x is performed on 0

    #Entangle Cluster State
    for q in range(6):
        qc.cz(q, q + 1) # Apply CZ between consecutive qubits

    #Rz
    # Define measurement angles for -X, -Y, -Z application
    angles = [-alpha, 0, 0, -beta, -gamma, 0]

    #Propagate
    for i in range(6):  # Measure first 6 qubits
        measure_in_xy_plane(qc, i, angles[i], i)
        qc.barrier()
        if i < 6:  # Conditional correction on the next qubit
            qc.x(i + 1).c_if(i, 1)
            qc.z(i + 1).c_if(i, 1)  # Add Z correction as well

    # **Save the final state before measuring the output qubit**
    qc.save_density_matrix()

    # MEasure the output bit
    qc.measure(6, 6)

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

    #Print parameters
    print("Angles as multiples of π:")
    print(f"α = {format_angle(alpha)} rad")
    print(f"β = {format_angle(beta)} rad")
    print(f"γ = {format_angle(gamma)} rad")
    print("Output Qubit State (Density Matrix) after RzRxRz:\n", reduced_density_matrix)

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

