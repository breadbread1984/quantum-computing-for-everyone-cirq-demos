#!/usr/bin/python3

from re import search;
import numpy as np;
import cirq;

def quantum_teleportation(rotations, measure = False):
  qubit_num = rotations.shape[0];
  alice_qubits = [cirq.devices.GridQubit(0,i) for i in range(qubit_num)];
  bob_qubits = [cirq.devices.GridQubit(1,i) for i in range(qubit_num)];
  qubits = [cirq.devices.GridQubit(2,i) for i in range(qubit_num)];
  circuit = cirq.circuits.Circuit();
  # 1) generate qubits to send
  if len(rotations.shape) == 2:
    for i in range(qubit_num):
      circuit.append(cirq.ops.rx(rotations[i, 0])(qubits[i]));
      circuit.append(cirq.ops.ry(rotations[i, 1])(qubits[i]));
      circuit.append(cirq.ops.rz(rotations[i, 2])(qubits[i]));
  elif len(rotations.shape) == 1:
    for i in range(qubit_num):
      if rotations[i] == 0: circuit.append(cirq.ops.I(qubits[i]));
      else: circuit.append(cirq.ops.X(qubits[i]));
  else:
    raise Exception('dimension of rotations must be either 1 or 2');
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
  # 1,1=>Y=X+Z (can be proved through transform matrix product)
  # NOTE: alice's bit decide whether to rotate bob's qubit around X axis
  # NOTE: qubit's bit decide whether to rotate bob's qubit around Z axis
  for i in range(qubit_num):
    circuit.append(cirq.ops.CX(alice_qubits[i], bob_qubits[i]));
    circuit.append(cirq.ops.CZ(qubits[i], bob_qubits[i]));
  if measure:
    for i in range(qubit_num):
      circuit.append(cirq.ops.measure_each(bob_qubits[i]));
  return circuit;
