#!/usr/bin/python3

import numpy as np;
import cirq;

def same_measures_with_different_basises_probability():
  probability = 0;
  measure = lambda basis, superposition: np.dot(np.transpose(basis), superposition);
  status = np.transpose([[1/np.sqrt(2), 1/np.sqrt(2)]]);
  basises = [np.array([[1,0],[0,1]]),
             np.array([[1/2, -np.sqrt(3)/2],[np.sqrt(3)/2, 1/2]]),
             np.array([[-1/2, -np.sqrt(3)/2],[np.sqrt(3)/2, -1/2]]),];
  for idx1, basis1 in enumerate(basises):
    for idx2, basis2 in enumerate(basises):
      if idx1 == idx2: continue; # skip measurement with a same basis
      combination_probability = 1/len(basises) * 1/len(basises);
      # measure0 = 0> measure1 = 0>
      measure1 = basis1[:,0:1]; # measure1.shape = (2,1)
      measure2 = measure(basis2, measure1); # measure2.shape = (2,1)
      prob1 = measure2[0,0] ** 2;
      # measure0 = 1> measure1 = 1>
      measure1 = basis1[:,1:2]; # measure1.shape = (2,1)
      measure2 = measure(basis2, measure1); # measure2.shape = (2,1)
      prob2 = measure2[1,0] ** 2;
      # NOTE: both measure results are 0 or 1
      probability += combination_probability * (0.5 * prob1 + 0.5 * prob2);
  return probability;

def ekert(qubit_num, alice_basises, bob_basises, eve_basises = None):
  assert qubit_num % 3 == 0;
  alice_qubits = [cirq.devices.GridQubit(0, i) for i in range(qubit_num)];
  bob_qubits = [cirq.devices.GridQubit(1, i) for i in range(qubit_num)];
  circuit = cirq.circuits.Circuit();
  # 1) generate a pair of entangled qubits
  for i in range(qubit_num):
    circuit.append(cirq.ops.H(alice_qubits[i]));
    circuit.append(cirq.ops.CNOT(alice_qubits[i], bob_qubits[i]));
  # q1 odot q2 = 1/sqrt(2)*00> + 1/sqrt(2)*11>
  # 2) measure with random basis
  for i in range(qubit_num):
    if eve_basises is not None:
      # NOTE: if eve presents the measure results of alice and bob are known (or predefined)
      # so the probability of alice and bob getting the same meeasure with probability 2/3
      if eve_basises[i] == 0:
        circuit.append(cirq.ops.I(alice_qubits[i]));
      elif eve_basises[i] == 1:
        circuit.append(cirq.ops.ry(-120/180*np.pi)(alice_qubits[i]));
      elif eve_basises[i] == 2:
        circuit.append(cirq.ops.ry(-240/180*np.pi)(alice_qubits[i]));
      # NOTE: currently cirq doesnt support multiple measurements on a same qubit
      circuit.append(cirq.ops.measure_each(alice_qubits[i]));
    if alice_basises[i] == 0:
      circuit.append(cirq.ops.I(alice_qubits[i]));
    elif alice_basises[i] == 1:
      circuit.append(cirq.ops.ry(-120/180*np.pi)(alice_qubits[i]));
    elif alice_basises[i] == 2:
      circuit.append(cirq.ops.ry(-240/180*np.pi)(alice_qubits[i]));
    circuit.append(cirq.ops.measure_each(alice_qubits[i]));
    if bob_basises[i] == 0:
      circuit.append(cirq.ops.I(bob_qubits[i]));
    elif bob_basises[i] == 1:
      circuit.append(cirq.ops.ry(-120/180*np.pi)(bob_qubits[i]));
    elif bob_basises[i] == 2:
      circuit.append(cirq.ops.ry(-240/180*np.pi)(bob_qubits[i]));
    circuit.append(cirq.ops.measure_each(bob_qubits[i]));
  return circuit;

