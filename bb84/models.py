#!/usr/bin/python3

import numpy as np;
import cirq;

def BB84(qubit_num, alice_basis, bob_basis, alice_measures):

  # 1) allocation n qubits with 0> value
  qubits = [cirq.LineQubit(i) for i in range(qubit_num)];
  circuit = cirq.Circuit();
  # 2) initialize qubits according to alice measures
  # alice's qubits
  for idx, basis in enumerate(alice_basis):
    # flip qubits according to measure results
    circuit.append(cirq.I(qubits[idx]) if alice_measures[idx] == 0 else cirq.X(qubits[idx]));
    # change qubits status if basis is on X axis
    circuit.append(cirq.I(qubits[idx]) if basis == 0 else cirq.H(qubits[idx]));
  # bob's measures
  for idx, basis in enumerate(bob_basis):
    # NOTE: actually the measure result is arbitrary if bob uses different basis from alice's
    # the behavior here is not what happens in the real world.
    circuit.append(cirq.I(qubits[idx]) if bob_basis[idx] == alice_basis[idx] else cirq.H(qubits[idx]));
  circuit.append(cirq.measure_each(*qubits));
  return circuit;
