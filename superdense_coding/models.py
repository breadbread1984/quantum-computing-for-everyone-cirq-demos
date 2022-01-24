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
  for i in range(0,len(message),2):
    binary = message[i:i+2];
    if binary == '00':
      circuit.append(cirq.ops.I(alice_qubits[i]));
