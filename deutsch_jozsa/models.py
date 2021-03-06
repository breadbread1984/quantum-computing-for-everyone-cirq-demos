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
  circuit.append(cirq.ops.CNOT(qubits[-1],q));

def deutsch_jozsa(n, use_balance = True):
  # NOTE: no readily available Hadamard for multiple qubits, so I have to create the gate with kronecker
  hadamard = np.array([[np.sqrt(0.5), np.sqrt(0.5)],[np.sqrt(0.5),-np.sqrt(0.5)]]);
  n_hadamard = cirq.linalg.kron(*([hadamard] * n));

  oracle = const_func if use_balance == False else balance_func;
  qubits = [cirq.devices.LineQubit(i) for i in range(n)];
  q = cirq.devices.LineQubit(n);
  circuit = cirq.circuits.Circuit();
  circuit.append(cirq.ops.X(q));
  circuit.append(cirq.ops.MatrixGate(n_hadamard)(*qubits));
  circuit.append(cirq.ops.H(q));
  oracle(circuit, qubits, q);
  circuit.append(cirq.ops.MatrixGate(n_hadamard)(*qubits));
  circuit.append(cirq.measure_each(*qubits));
  return circuit;
