#!/usr/bin/python3

from re import search;
import numpy as np;
import cirq;

def communication(qubit_num):
  circuit = cirq.circuits.Circuit();
  # 1) generate q1 odot q2 odot q3 = 1/sqrt(2)*000>+1/sqrt(2)*111>
  for i in range(qubit_num):
    # 1.1) generate q1 = 1/sqrt(2)*0>+1/sqrt(2)*1>
    circuit.append(cirq.ops.H(cirq.devices.GridQubit(0, i)));
    # 1.2) entangle first and second qubit
    circuit.append(cirq.ops.CNOT(cirq.devices.GridQubit(0, i), cirq.devices.GridQubit(1, i)));
    # 1.3) entangle first and thrid qubit
    circuit.append(cirq.ops.CNOT(cirq.devices.GridQubit(0, i), cirq.devices.GridQubit(2, i)));
  # 2) create random flip to one of the first three qubits
  flip_idx = list()
  for i in range(qubit_num):
    qidx = np.random.randint(low = 0, high = 3);
    circuit.append(cirq.ops.X(cirq.devices.GridQubit(qidx, i)));
    flip_idx.append(qidx);
  '''
  for i in range(qubit_num):
    circuit.append(cirq.ops.measure_each(cirq.devices.GridQubit(0, i)));
    circuit.append(cirq.ops.measure_each(cirq.devices.GridQubit(1, i)));
    circuit.append(cirq.ops.measure_each(cirq.devices.GridQubit(2, i)));
  '''
  # 3) create odd and even correction
  for i in range(qubit_num):
    # 2.1) entangle first qubit and first correction qubit
    circuit.append(cirq.ops.CNOT(cirq.devices.GridQubit(0, i), cirq.devices.GridQubit(3, i)));
    # 2.2) entangle second qubit and first correction qubit
    circuit.append(cirq.ops.CNOT(cirq.devices.GridQubit(1, i), cirq.devices.GridQubit(3, i)));
    # 2.3) entangle first qubit and second correction qubit
    circuit.append(cirq.ops.CNOT(cirq.devices.GridQubit(0, i), cirq.devices.GridQubit(4, i)));
    # 2.4) entangle thrid qubit and second correction qubit
    circuit.append(cirq.ops.CNOT(cirq.devices.GridQubit(2, i), cirq.devices.GridQubit(4, i)));
  # 4) measure correction qubits
  for i in range(qubit_num):
    circuit.append(cirq.ops.measure_each(cirq.devices.GridQubit(3, i)));
    circuit.append(cirq.ops.measure_each(cirq.devices.GridQubit(4, i)));
  return circuit, flip_idx;

def correction(correction_code):
  assert len(correction_code)%2 == 0 and search('[^01]', correction_code) is None;
  qubit_num = len(correction_code) // 2;
  circuit = cirq.circuits.Circuit();
  for i in range(qubit_num):
    cc = correction_code[i*2:(i+1)*2];
    if cc == '00': continue;
    elif cc == '11':
      circuit.append(cirq.ops.X(cirq.devices.GridQubit(0, i)));
    elif cc == '10':
      circuit.append(cirq.ops.X(cirq.devices.GridQubit(1, i)));
    elif cc == '01':
      circuit.append(cirq.ops.X(cirq.devices.GridQubit(2, i)));
  for i in range(qubit_num):
    circuit.append(cirq.ops.measure_each(cirq.devices.GridQubit(0, i)));
    circuit.append(cirq.ops.measure_each(cirq.devices.GridQubit(1, i)));
    circuit.append(cirq.ops.measure_each(cirq.devices.GridQubit(2, i)));
  return circuit;

