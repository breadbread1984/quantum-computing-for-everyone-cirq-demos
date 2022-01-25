#!/usr/bin/python3

from re import search;
import numpy as np;
import cirq;

def quantum_teleportation_send(qubit_num):
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
  return circuit, np.stack([dx, dy, dz], axis = -1);

def quantum_teleportation_receive(control_bits):
  assert search('[^01]', control_bits) is None and len(control_bits) % 2 == 0;
  qubit_num = len(control_bits) // 2;
  bob_qubits = [cirq.devices.GridQubit(1,i) for i in range(qubit_num)];
  circuit = cirq.circuits.Circuit();
  # 1) post process
  # NOTE: quantum teleportation occurs here, but cannot leave circuit without measuring bob's qubits 
  # so cannot show the teleported qubit status to you.
  for i in range(0, len(control_bits), 2):
    bits = control_bits[i:i+2];
    qidx = i // 2;
    if bits == '00': circuit.append(cirq.ops.I(bob_qubits[qidx]));
    elif bits == '01': circuit.append(cirq.ops.X(bob_qubits[qidx]));
    elif bits == '10': circuit.append(cirq.ops.Z(bob_qubits[qidx]));
    elif bits == '11': circuit.append(cirq.ops.Y(bob_qubits[qidx]));
  # FIXME: circuit must contain measure operation
  circuit.append(cirq.ops.measure_each(*bob_qubits));
  return circuit;