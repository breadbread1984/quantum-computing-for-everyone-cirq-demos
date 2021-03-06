#!/usr/bin/python3

import numpy as np;
import cirq;

def predefined_results():
  results = dict();
  a_counts = 0;
  d_counts = 0;
  for combination in range(8):
    binary = bin(combination)[2:];
    predefined_measure_results = '0' * (3 - len(binary)) + binary;
    assert len(predefined_measure_results) == 3;
    results[predefined_measure_results] = dict();
    # basises are one among [B1(0),B2(0)], [B1(120),B2(120)], [B1(240), B2(240)]
    for basis1_idx in range(3):
      measure1_result = int(predefined_measure_results[basis1_idx]); # 0> or 1>
      for basis2_idx in range(3):
        measure2_result = int(predefined_measure_results[basis2_idx]); # 0> or 1>
        basises = 'B(%d) B(%d)' % (basis1_idx * 120, basis2_idx * 120);
        if measure1_result == measure2_result:
          # two measures are the same
          results[predefined_measure_results][basises] = 'A';
          a_counts += 1;
        else:
          # two measures are different
          results[predefined_measure_results][basises] = 'D';
          d_counts += 1;
  return results, a_counts / (a_counts + d_counts);

def strange_results():
  probability = 0;
  measure = lambda basis, superposition: np.dot(np.transpose(basis), superposition);
  status = np.transpose([[1/np.sqrt(2), 1/np.sqrt(2)]]);
  basises = [np.array([[1,0],[0,1]]),
             np.array([[1/2, -np.sqrt(3)/2],[np.sqrt(3)/2, 1/2]]),
             np.array([[-1/2, -np.sqrt(3)/2],[np.sqrt(3)/2, -1/2]]),];
  for basis1 in basises:
    for basis2 in basises:
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

def measure_network(qubit_num):
  q1 = [cirq.devices.GridQubit(0, i) for i in range(qubit_num)]; # q1 = 1*0>+0*1>
  q2 = [cirq.devices.GridQubit(1, i) for i in range(qubit_num)]; # q2 = 1*0>+0*1>
  circuit = cirq.circuits.Circuit();
  # 1) generate a pair of entangled qubits
  for i in range(qubit_num):
    circuit.append(cirq.ops.H(q1[i])); # q1 = 1/sqrt(2)*0>+1/sqrt(2)*1>
    circuit.append(cirq.ops.CNOT(q1[i], q2[i]));
  # q1 odot q2 = 1/sqrt(2)*00> + 0*01> + 0*10> + 1/sqrt(2)*11>
  # 2) measure with random two basises
  basises = np.random.randint(low = 0, high = 3, size = (2, qubit_num));
  for i in range(qubit_num):
    if basises[0,i] == 0:
      circuit.append(cirq.ops.I(q1[i]));
    elif basises[0,i] == 1:
      circuit.append(cirq.ops.ry(-120/180*np.pi)(q1[i]));
    elif basises[0,i] == 2:
      circuit.append(cirq.ops.ry(-240/180*np.pi)(q1[i]));
    circuit.append(cirq.ops.measure_each(q1[i]));
    if basises[1,i] == 0:
      circuit.append(cirq.ops.I(q2[i]));
    elif basises[1,i] == 1:
      circuit.append(cirq.ops.ry(-120/180*np.pi)(q2[i]));
    elif basises[1,i] == 2:
      circuit.append(cirq.ops.ry(-240/180*np.pi)(q2[i]));
    circuit.append(cirq.ops.measure_each(q2[i]));
  return circuit;
