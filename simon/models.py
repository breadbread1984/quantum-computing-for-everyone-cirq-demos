#!/usr/bin/python3

from random import shuffle;
import numpy as np;
import cirq;

def oracle(circuit, x, y):
  # random function
  n = len(x);
  m = np.eye(2**(2 * n));
  np.random.shuffle(m);
  circuit.append(cirq.ops.MatrixGate(m)(*x, *y));
  return m;

def simon(n):
  hadamard = np.array([[np.sqrt(0.5), np.sqrt(0.5)],[np.sqrt(0.5),-np.sqrt(0.5)]]);
  n_hadamard = cirq.linalg.kron(*([hadamard] * n));

  circuit = cirq.circuits.Circuit();
  x = [cirq.devices.LineQubit(i) for i in range(n)];
  y = [cirq.devices.LineQubit(i) for i in range(n,2*n)];
  circuit.append(cirq.ops.MatrixGate(n_hadamard)(*x));
  m = oracle(circuit, x, y);
  circuit.append(cirq.ops.MatrixGate(n_hadamard)(*x));
  circuit.append(cirq.ops.measure_each(*x));
  return circuit, m;
