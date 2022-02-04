#!/usr/bin/python3

import numpy as np;
import cirq;

def oracle(circuit, x, y):
  n = len(x);
  idx = np.random.randint(low = 0, high = 2, size = (n,));
  for s, q in zip(idx, x):
    if s == 0: circuit.append(cirq.ops.X(q)); # flip qubit to make it flags for controlling output qubit
  circuit.append(cirq.ops.CCNOT(*x, y));
  for s, q in zip(idx, x):
    if s == 0: circuit.append(cirq.ops.X(q)); # restore qubit status
  idx = int(''.join(idx.astype(np.str)),2);
  return idx;

def grover(n = 2):
  hadamard = np.array([[np.sqrt(0.5), np.sqrt(0.5)],[np.sqrt(0.5),-np.sqrt(0.5)]]);
  n_hadamard = cirq.linalg.kron(*([hadamard] * n));
  amplitude = 1/(np.sqrt(2)**n)*(np.ones(2**n) - 2 * np.eye(2**n));

  x = [cirq.devices.LineQubit(i) for i in range(n)];
  y = cirq.devices.LineQubit(n);
  circuit = cirq.circuits.Circuit();
  circuit.append(cirq.ops.MatrixGate(n_hadamard)(*x));
  circuit.append(cirq.ops.X(y));
  circuit.append(cirq.ops.H(y));
  idx = oracle(circuit, x, y);
  circuit.append(cirq.ops.MatrixGate(amplitude)(*x));
  circuit.append(cirq.ops.measure_each(*x));
  return circuit, idx;
