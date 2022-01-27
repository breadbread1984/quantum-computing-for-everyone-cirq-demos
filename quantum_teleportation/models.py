#!/usr/bin/python3

from re import search;
import numpy as np;
import cirq;

def quantum_teleportation(qubit_num):
  alice_qubits = [cirq.devices.GridQubit(0,i) for i in range(qubit_num)];
  bob_qubits = [cirq.devices.GridQubit(1,i) for i in range(qubit_num)];
  qubits = [cirq.devices.GridQubit(2,i) for i in range(qubit_num)];
  dx = np.random.uniform(low = 0, high = np.pi, size = (qubit_num,));
  dy = np.random.uniform(low = 0, high = np.pi, size = (qubit_num,));
  dz = np.random.uniform(low = 0, high = 2 * np.pi, size = (qubit_num,));
  circuit = cirq.circuits.Circuit();
  # 1) prepare qubits to send
  for i in range(qubit_num):
    circuit.append(cirq.ops.rx(dx[i])(qubits[i]));
    circuit.append(cirq.ops.ry(dy[i])(qubits[i]));
    circuit.append(cirq.ops.rz(dz[i])(qubits[i]));
  # 2) generate a pair of entangled qubits
  for i in range(qubit_num):
    circuit.append(cirq.ops.H(alice_qubits[i]));
    circuit.append(cirq.ops.CNOT(alice_qubits[i], bob_qubits[i]));
  # 3) alice's qubit and qubit to send send to inverse bell gate
  for i in range(qubit_num):
    circuit.append(cirq.ops.CNOT(qubits[i], alice_qubits[i]));
    circuit.append(cirq.ops.H(qubits[i]));
  circuit.append(cirq.ops.measure_each(*(qubits + alice_qubits)));
  # 4) restore qubits status
  # qubit, alice_qubit
  # 0,0=>I
  # 0,1=>X
  # 1,0=>Z
  # 1,1=>Y=X+Z
  # NOTE: alice's bit decide whether to rotate bob's qubit around X axis
  # NOTE: qubit's bit decide whether to rotate bob's qubit around Z axis
  for i in range(qubit_num):
    circuit.append(cirq.ops.CX(alice_qubits[i], bob_qubits[i]));
    circuit.append(cirq.ops.CZ(qubits[i], bob_qubits[i]));
  return circuit, np.stack([dx,dy,dz], axis = -1);

