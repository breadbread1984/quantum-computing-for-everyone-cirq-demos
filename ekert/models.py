#!/usr/bin/python3

import numpy as np;
import cirq;

def ekert(qubit_num):
  assert qubit_num % 3 == 0;
  alice_qubits = [cirq.devices.GridQubit(0, i) for i in range(qubit_num)];
  bob_qubits = [cirq.devices.LineQubit(1, i) for i in range(qubit_num)];
  circuit = cirq.circuits.Circuit();
  # 1) generate a pair of entangled qubits
  for i in range(qubit_num):
    circuit.append(cirq.ops.H(alice_qubits[i]));
    circuit.append(cirq.ops.CNOT(alice_qubits[i], bob_qubits[i])));
  # q1 odot q2 = 1/sqrt(2)*00> + 1/sqrt(2)*11>
  # 2) measure with random basis
  basises = np.random.randint(low = 0, high = 3, size = (2, qubit_num));
  for i in range(qubit_num):
    if basises[0,i] == 0:
      circuit.append(cirq.ops.I(alice_qubits[i]));
    elif basises[0,i] == 1:
      circuit.append(cirq.ops.ry(-120/180*np.pi)(alice_qubits[i]));
    elif basises[0,i] == 2:
      circuit.append(cirq.ops.ry(-240/180*np.pi)(alice_qubits[i]));
    circuit.append(cirq.ops.measure_each(alice_qubits[i]));
    if basises[1,i] == 0:
      circuit.append(cirq.ops.I(bob_qubits[i]));
    elif basises[1,i] == 1:
      circuit.append(cirq.ops.ry(-120/180*np.pi)(bob_qubits[i]));
    elif basises[1,i] == 2:
      circuit.append(cirq.ops.ry(-240/180*np.pi)(bob_qubits[i]));
    circuit.append(cirq.ops.measure_each(bob_qubits[i]));
  return circuit;

