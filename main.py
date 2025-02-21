from qiskit import QuantumCircuit
from mbqc_transpiler.transpiler import decompose_qc
# from mbqc_transpiler.visualization import plot_cluster_state

def main():
    """Main function to run the quantum circuit transpiler."""
    # Step 1: Define a sample quantum circuit
    qc = QuantumCircuit(1)
    qc.h(0)
    qc.x(0)
    qc.u(1, 2, 3, 0)
    # qc.cx(0, 1)
    # qc.cx(1, 2)

    print("\nOriginal Quantum Circuit:")
    print(qc)

    # Step 2: Convert to MBQC format
    print("\nTranspiling to MBQC...")
    ht_circ = decompose_qc(qc)

    print(ht_circ)

    # Step 3: Visualize the cluster state graph
    # plot_cluster_state(mbqc_graph)

if __name__ == "__main__":
    main()
