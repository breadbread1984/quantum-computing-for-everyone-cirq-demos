#!/usr/bin/python3

import numpy as np;
import cirq;

def oracle(circuit, qubits_x, qubits_y):
  n = len(qubits_x);
  m = np.eye(2**(2 * n));
  m = np.concatenate([m[:,:2**(2*n-1)], m[:,2**(2*n-1):][:,::-1]], axis = 1);
  circuit.append(cirq.ops.MatrixGate(m)(*qubits_x, *qubits_y));

def simon(n):
  hadamard = np.array([[np.sqrt(0.5), np.sqrt(0.5)],[np.sqrt(0.5),-np.sqrt(0.5)]]);
  n_hadamard = cirq.linalg.kron(*([hadamard] * n));

  circuit = cirq.circuits.Circuit();
  qubits_x = [cirq.devices.LineQubit(i) for i in range(n)];
  qubits_y = [cirq.devices.LineQubit(i) for i in range(n,2*n)];
  circuit.append(cirq.ops.MatrixGate(n_hadamard)(*qubits_x));
  oracle(circuit, qubits_x, qubits_y);
  circuit.append(cirq.ops.MatrixGate(n_hadamard)(*qubits_x));
  circuit.append(cirq.ops.measure_each(*qubits_x));
  return circuit;
