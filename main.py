from qiskit import QuantumCircuit
from qiskit_aer.backends.compatibility import Statevector

import examples.MBQC_examples as mbqc_examples
from mbqc_transpiler.decomposer import decompose_qc
import numpy as np
import examples.MBQC_examples
# from mbqc_transpiler.visualization import plot_cluster_state

def main():
    # """Main function to run the quantum circuit transpiler."""
    # # Step 1: Define a sample quantum circuit
    # qc = QuantumCircuit(1)
    # qc.h(0)
    # qc.x(0)
    # qc.z(0)
    # qc.u(np.pi/2, 7 * np.pi / 4, 0, 0)
    # qc.u(np.pi/2, 0, 0, 0)
    #
    # # qc.cx(0, 1)
    # # qc.cx(1, 2)
    #
    # print("\nOriginal Quantum Circuit:")
    # print(qc)
    #
    # # Step 2: Convert to MBQC format
    # print("\nTranspiling to MBQC...")
    # ht_circ = decompose_qc(qc)
    #
    # print(ht_circ)

    """Test MBQC circs:"""
    # input_state = Statevector([1/2, (3**0.5)/2])
    input_state = Statevector([0, 1])

    """ Examples of gates: """
    # mbqc_examples.mbqc_pauli_x()
    mbqc_examples.mbqc_arbitrary_x(input_state, np.pi)
    mbqc_examples.mbqc_arbitrary_z(input_state, np.pi/3)
    # mbqc_examples.mbqc_hadamard()
    # mbqc_examples.mbqc_arbitrary_u(input_state, np.pi/2, np.pi/4, np.pi/8)


    # Step 3: Visualize the cluster state graph
    # plot_cluster_state(mbqc_graph)

if __name__ == "__main__":
    main()
