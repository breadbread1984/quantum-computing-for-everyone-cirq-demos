#!/usr/bin/python3

import numpy as np;
import cirq;

def const_func(circuit, qubits, q):
  # f(x1,...,xn) = 0, in other words y^f(x)=y
  for qubit in qubits:
    circuit.append(cirq.ops.I(qubit));
  circuit.append(cirq.ops.I(q));

def balance_func(circuit, qubits, q):
  # balance function
  circuit.append(cirq.ops.CCNOT(*qubits,q));

def deutsch_jozsa(n, use_balance = True):
  hadamard = np.array([[1/np.sqrt(2), 1/np.sqrt(2)],[1/np.sqrt(2),-1/np.sqrt(2)]]);
  oracle = const_func if use_balance == False else balance_func;
  qubits = [cirq.devices.GridQubit(i, 0) for i in range(n)];
  q = cirq.devices.GridQubit(n, 0);
  circuit = cirq.circuits.Circuit();
  circuit.append(cirq.ops.X(q));
  circuit.append(cirq.ops.MatrixGate(cirq.linalg.kron(*([hadamard] * n)), *qubits));
  circuit.append(cirq.ops.H(q));
  oracle(circuit, qubits, q);
  circuit.append(cirq.ops.MatrixGate(cirq.linalg.kron(*([hadamard] * n)), *qubits));
  circuit.append(cirq.measure_each(*qubits));
  return circuit;
