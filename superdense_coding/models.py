#!/usr/bin/python3

from re import search;
import cirq;

def superdense_coding(message = None):
  assert len(message) % 2 == 0 and search('[^01]', message) is None;
  qubit_num = len(message) // 2;
  alice_qubits = [cirq.devices.GridQubit(0,i) for i in range(qubit_num)];
  bob_qubits = [cirq.devices.GridQubit(1,i) for i in range(qubit_num)];
  circuit = cirq.circuits.Circuit();
  # 1) generate a pair of entangled qubits
  for i in range(qubit_num):
    circuit.append(cirq.ops.H(alice_qubits[i]));
    circuit.append(cirq.ops.CNOT(alice_qubits[i], bob_qubits[i]));
  # 2) alice send every 2bit by sending one qubit to bob
  for i in range(0,len(message),2):
    binary = message[i:i+2];
    qidx = i // 2;
    if binary == '00':
      circuit.append(cirq.ops.I(alice_qubits[qidx]));
    elif binary == '01':
      circuit.append(cirq.ops.X(alice_qubits[qidx]));
    elif binary == '10':
      circuit.append(cirq.ops.Z(alice_qubits[qidx]));
    elif binary == '11':
      circuit.append(cirq.ops.Y(alice_qubits[qidx]));
    else:
      raise Exception('invalid symbol in message');
  # 3) bob receive 2bit per one qubit
  for i in range(qubit_num):
    circuit.append(cirq.ops.CNOT(alice_qubits[i], bob_qubits[i]));
    circuit.append(cirq.ops.H(alice_qubits[i]));
  circuit.append(cirq.ops.measure_each(*alice_qubits));
  circuit.append(cirq.ops.measure_each(*bob_qubits));
  return circuit;

