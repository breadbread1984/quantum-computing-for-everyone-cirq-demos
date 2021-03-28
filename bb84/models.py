#!/usr/bin/python3

import numpy as np;
import cirq;

def BB84(qubit_num):

  circuit = cirq.Circuit();
  alice_basis = np.random.randint(0,2,size = (qubit_num,));
  bob_basis = np.random.randint(0,2,size = (qubit_num,));
  alice_measures = np.random.randint(0,2,size = (qubit_num,));
  qubits = [cirq.LineQubit(i) for i in range(qubit_num)];
  # alice's qubits
  for idx, basis in enumerate(alice_basis):
    if alice_measures[idx] == 1:
      circuit.append(cirq.X(qubits[idx]));
    if basis == 1:
      circuit.append(cirq.H(qubits[idx]));
  # bob's measures

