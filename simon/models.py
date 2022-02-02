#!/usr/bin/python3

from random import shuffle;
import numpy as np;
import cirq;

def oracle(circuit, x, y):
  # NOTE: f(x) = x^(x^y)=y (independent of x) if s == 1, therefore, f(s^x) = y
  #       f(x) = x^y if s == 0, therefore, f(s^x) = (0^x)^y = x^y
  # therefore, f(x) = f(s^x), no matter s = 0 or 1
  n = len(x);
  s = np.random.randint(low = 0, high = 2, size = (n,));
  for i in range(n):
    circuit.append(cirq.ops.CNOT(x[i], y[i]));
    if s[i] == 1:
      circuit.append(cirq.ops.CNOT(x[i], y[i]));
  circuit.append(cirq.ops.SWAP(x[-1],y[-2]));

def simon(n):
  hadamard = np.array([[np.sqrt(0.5), np.sqrt(0.5)],[np.sqrt(0.5),-np.sqrt(0.5)]]);
  n_hadamard = cirq.linalg.kron(*([hadamard] * n));

  circuit = cirq.circuits.Circuit();
  x = [cirq.devices.LineQubit(i) for i in range(n)];
  y = [cirq.devices.LineQubit(i) for i in range(n,2*n)];
  circuit.append(cirq.ops.MatrixGate(n_hadamard)(*x));
  oracle(circuit, x, y);
  circuit.append(cirq.ops.MatrixGate(n_hadamard)(*x));
  circuit.append(cirq.ops.measure_each(*x));
  return circuit;
