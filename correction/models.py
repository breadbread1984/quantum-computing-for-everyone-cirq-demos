#!/usr/bin/python3

from re import search;
import numpy as np;
import cirq;

def correction(qubit_num):
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
  # 5) correction qubits
  for i in range(qubit_num):
    # 11 => flip q1
    circuit.append(cirq.ops.CCNOT(cirq.devices.GridQubit(3, i), cirq.devices.GridQubit(4, i), cirq.devices.GridQubit(0, i)));
    # 10 => flip q2
    circuit.append(cirq.ops.CNOT(cirq.devices.GridQubit(3, i), cirq.devices.GridQubit(4, i)));
    circuit.append(cirq.ops.CCNOT(cirq.devices.GridQubit(3, i), cirq.devices.GridQubit(4, i), cirq.devices.GridQubit(1, i)));
    circuit.append(cirq.ops.CNOT(cirq.devices.GridQubit(3, i), cirq.devices.GridQubit(4, i))); # reset control signal
    # 01 => flip q3
    circuit.append(cirq.ops.CNOT(cirq.devices.GridQubit(4, i), cirq.devices.GridQubit(3, i)));
    circuit.append(cirq.ops.CCNOT(cirq.devices.GridQubit(3, i), cirq.devices.GridQubit(4, i), cirq.devices.GridQubit(2, i)));
    circuit.append(cirq.ops.CNOT(cirq.devices.GridQubit(4, i), cirq.devices.GridQubit(3, i))); # reset control signal, do or not has nothing to do with outsome, this line can be removed
  # 6) measure to verify
  for i in range(qubit_num):
    circuit.append(cirq.ops.measure_each(cirq.devices.GridQubit(0, i)));
    circuit.append(cirq.ops.measure_each(cirq.devices.GridQubit(1, i)));
    circuit.append(cirq.ops.measure_each(cirq.devices.GridQubit(2, i)));
  return circuit;
