#!/usr/bin/python3

import numpy as np;
import cirq;

def BB84(qubit_num, alice_basises, bob_basises, eve_basises = None):

  # 1) allocation n qubits with 0> value
  qubits = [cirq.devices.LineQubit(i) for i in range(qubit_num)];
  circuit = cirq.circuits.Circuit();
  # 2) initialize qubits according to alice measures
  # alice's qubits
  alice_measures = list();
  for idx, (alice_basis, bob_basis) in enumerate(zip(alice_basises, bob_basises)):
    # alice's measures by alice's random basis
    alice_measures.append(np.random.randint(low = 0, high = 2));
    circuit.append(cirq.ops.I(qubits[idx]) if alice_measures[-1] == 0 else cirq.ops.X(qubits[idx]));
    # if eve presents
    if eve_basises is not None:
      circuit.append(cirq.ops.I(qubits[idx]) if alice_basis == eve_basises[idx] else cirq.ops.H(qubits[idx]));
      # NOTE: currently cirq doesnt support multiple measurements on a same qubit
      circuit.append(cirq.ops.measure_each(*qubits)); # eve measures
      circuit.append(cirq.ops.I(qubits[idx]) if eve_basises[idx] == bob_basis else cirq.ops.H(qubits[idx]));
    else:
      # if alice's basis is the same as bob's basis the measures of both are the same, or measure the quabit from a perpendicular direction
      circuit.append(cirq.ops.I(qubits[idx]) if alice_basis == bob_basis else cirq.ops.H(qubits[idx]));
  circuit.append(cirq.ops.measure_each(*qubits));
  return circuit, alice_measures;
