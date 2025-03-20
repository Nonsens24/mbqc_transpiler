import numpy as np
from graphix import Circuit


#
# def cp(circuit, theta, control, target):
#
#     # print("c: ",  control, " target: ", target)
#     circuit.rz(control, theta / 2)
#     circuit.rz(target, theta / 2)
#     circuit.cnot(control, target)
#     circuit.rz(target, -1 * theta / 2)
#     circuit.cnot(control, target)
#
# def qft_rotations(n, circ: Circuit):
#
#     for q in range(n):
#         circ.h(q)
#         for i in range(q + 1, n):
#             cp(circ, np.pi / (2** i), q, i)
#
#
# def qft_swaps(n, circ):
#     n=n-1
#     for q in range(n//2):
#         print("q:", q, " n-q: ", n-q)
#         circ.swap(q, n-q-1)
#
# def qft(num_inputs):
#
#     if(num_inputs <= 0): return -1
#
#     circ = Circuit(num_inputs)
#     qft_rotations(num_inputs, circ)
#     qft_swaps(num_inputs, circ)
#
#     return circ



def cp(circuit, theta, control, target):
    circuit.rz(control, theta / 2)
    circuit.rz(target, theta / 2)
    circuit.cnot(control, target)
    circuit.rz(target, -1 * theta / 2)
    circuit.cnot(control, target)


def qft_rotations(circuit, n):
    circuit.h(n)
    for qubit in range(n + 1, circuit.width):
        cp(circuit, np.pi / 2 ** (qubit - n), qubit, n)


def swap_registers(circuit, n):
    for qubit in range(n // 2):
        circuit.swap(qubit, n - qubit - 1)
    return circuit


def qft(circuit, n):
    for i in range(n):
        qft_rotations(circuit, i)
    swap_registers(circuit, n)
