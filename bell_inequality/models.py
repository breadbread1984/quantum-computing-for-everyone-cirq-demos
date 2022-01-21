#!/usr/bin/python3

import numpy as np;
import cirq;

def predefined_results():
  measure = lambda basis, superposition: np.dot(np.transpose(basis), superposition);
  superposition = np.transpose([[1/np.sqrt(2),1/np.sqrt(2)]]); # q=1/sqrt(2)*0>+1/sqrt(2)*1>
  basises = [np.array([[1,0],[0,1]]), # [B1(0), B2(0)]
             np.array([[1/2,-np.sqrt(3)/2],[np.sqrt(3)/2,1/2]]), # [B1(120), B2(120)]
             np.array([[-1/2,-np.sqrt(3)/2],[np.sqrt(3)/2,-1/2]]),]; # [B1(240), B2(240)]
  for combination in range(8):
    binary = bin(combination)[2:];
    predefined_measure_results = '0' * (3 - len(binary)) + binary;
    assert len(predefined_measure_results) == 3;
    for basis1 in basises:
      for basis2 in basises:
        

def strange_results():
  q1 = cirq.devices.LineQubit(0); # q1 = 1*0>+0*1>
  q2 = cirq.devices.LineQubit(1); # q2 = 1*0>+0*1>
  circuit = cirq.circuits.Circuit();
  circuit.append(cirq.ops.H(q1)); # q1 = 1/sqrt(2)*0>+1/sqrt(2)*1>
  circuit.append(cirq.ops.CNOT(q1, q2));
  # q1 odot q2 = 1/sqrt(2)*00> + 0*01> + 0*10> + 1/sqrt(2)*11>
  
