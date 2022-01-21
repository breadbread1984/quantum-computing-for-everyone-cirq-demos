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
    results[predefined_measure_results] = list();
    # basises are one among [B1(0),B2(0)], [B1(120),B2(120)], [B1(240), B2(240)]
    for basis1_idx in range(3):
      measure1_result = int(predefined_measure_results[basis1_idx]); # 0> or 1>
      for basis2_idx in range(3):
        measure2_result = int(predefined_measure_results[basis2_idx]); # 0> or 1>
        if measure1_result == measure2_result:
          # two measures are the same
          results[predefined_measure_results].append('A');
          a_counts += 1;
        else:
          # two measures are different
          results[predefined_measure_results].append('D');
          d_counts += 1;
  print(results);
  return a_counts / (a_counts + d_counts);

def strange_results():
  q1 = cirq.devices.LineQubit(0); # q1 = 1*0>+0*1>
  q2 = cirq.devices.LineQubit(1); # q2 = 1*0>+0*1>
  circuit = cirq.circuits.Circuit();
  circuit.append(cirq.ops.H(q1)); # q1 = 1/sqrt(2)*0>+1/sqrt(2)*1>
  circuit.append(cirq.ops.CNOT(q1, q2));
  # q1 odot q2 = 1/sqrt(2)*00> + 0*01> + 0*10> + 1/sqrt(2)*11>
  
