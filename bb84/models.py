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
    # qubits of random status prepared by alice
    circuit.append(cirq.I(qubits[idx]) if alice_measures[idx] == 0 else cirq.X(qubits[idx]));
    # qubits after alice's measures, status changes if the measure is done on X axis
    circuit.append(cirq.I(qubits[idx]) if basis == 0 else cirq.H(qubits[idx]));
  # bob's measures
  for idx, basis in enumerate(bob_basis):
    # qubits after bob's measures, status changes if the measure is done on different basis from alice's
    circuit.append(cirq.I(qubits[idx]) if bob_basis[idx] == 0 else cirq.H(qubits[idx]));
  circuit.append(cirq.measure_each(*qubits));
  return circuit;
