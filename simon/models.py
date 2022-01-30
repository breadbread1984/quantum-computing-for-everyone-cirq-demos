#!/usr/bin/python3

from random import shuffle;
import numpy as np;
import cirq;

def oracle(circuit, x, y):
  # NOTE: f(x) = x^y and s == y
  # therefore f(s^x) = s^x^y
  s = np.random.randint(low = 0, high = 2, size = (len(y),));
  for qidx, qy in enumerate(y):
    if s[qidx] == 1:
      circuit.append(cirq.ops.X(qy));
  for qx,qy in zip(x,y):
    circuit.append(cirq.ops.CNOT(qy,qx));
  return s;

def simon(n):
  hadamard = np.array([[np.sqrt(0.5), np.sqrt(0.5)],[np.sqrt(0.5),-np.sqrt(0.5)]]);
  n_hadamard = cirq.linalg.kron(*([hadamard] * n));

  circuit = cirq.circuits.Circuit();
  x = [cirq.devices.LineQubit(i) for i in range(n)];
  y = [cirq.devices.LineQubit(i) for i in range(n,2*n)];
  circuit.append(cirq.ops.MatrixGate(n_hadamard)(*x));
  s = oracle(circuit, x, y);
  circuit.append(cirq.ops.MatrixGate(n_hadamard)(*x));
  circuit.append(cirq.ops.measure_each(*x));
  return circuit, s;
