from qiskit import QuantumCircuit
from qiskit_aer.backends.compatibility import Statevector

import examples.MBQC_examples as mbqc_examples
from mbqc_transpiler.decomposer import decompose_qc
import numpy as np
import examples.MBQC_examples

#Test Graphix
from graphix import Circuit
import mbqc_transpiler.graphix_unitaries as graphix_unitaries


# from mbqc_transpiler.visualization import plot_cluster_state

def main():
    # Graphix MBQC transpiler

    n = 5
    circuit = Circuit(n)

    graphix_unitaries.qft(circuit, n)

    pattern = circuit.transpile().pattern
    pattern.standardize()
    pattern.shift_signals()

    pattern.draw_graph()

    # %%
    # Using efficient graph state simulator `graphix.GraphSim`, we can classically preprocess Pauli measurements.
    # We are currently improving the speed of this process by using rust-based graph manipulation backend.
    pattern.perform_pauli_measurements(use_rustworkx=True)

    # %%
    # To specify TN backend of the simulation, simply provide as a keyword argument.
    # here we do a very basic check that one of the statevector amplitudes is what it is expected to be:

    import time

    t1 = time.time()
    tn = pattern.simulate_pattern(backend="tensornetwork")
    value = tn.get_basis_amplitude(0)
    t2 = time.time()
    print("amplitude of |00...0> is ", value)
    print("1/2^n (true answer) is", 1 / 2 ** n)
    print("approximate execution time in seconds: ", t2 - t1)

    # print("Calculating output state...")
    # out_state = pattern.simulate_pattern(backend="statevector")
    # print("out state: ", out_state.flatten())

    #
    # circuit = Circuit(n)
    #
    # for i in range(n):
    #     circuit.h(i)
    # graphix_unitaries.qft(circuit, n)
    #
    # pattern = circuit.transpile().pattern
    # pattern.standardize()
    # pattern.shift_signals()
    #
    # nodes, edges = pattern.get_graph()
    # print(f"Number of nodes: {len(nodes)}")
    # print(f"Number of edges: {len(edges)}")
    #
    # pattern.draw_graph()

    """Test MBQC circs:"""
    # input_state = Statevector([1/2, (3**0.5)/2])
    # input_state = Statevector([0, 1])

    """ Examples of gates: """
    # mbqc_examples.mbqc_pauli_x()
    # mbqc_examples.mbqc_arbitrary_x(input_state, np.pi)
    # mbqc_examples.mbqc_arbitrary_z(input_state, np.pi/3)
    # mbqc_examples.mbqc_hadamard()
    # mbqc_examples.mbqc_arbitrary_u(input_state, np.pi/2, np.pi/4, np.pi/8)


    # Step 3: Visualize the cluster state graph
    # plot_cluster_state(mbqc_graph)

if __name__ == "__main__":
    main()
