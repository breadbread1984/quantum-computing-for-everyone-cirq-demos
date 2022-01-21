#!/usr/bin/python3

import cirq;

def entangled_qubits_pair(measure_q1_first = True):
  q1 = cirq.devices.LineQubit(0); # q1 = 1*0>+0*1>
  q2 = cirq.devices.LineQubit(1); # q2 = 1*0>+0*1>
  circuit = cirq.circuits.Circuit();
  circuit.append(cirq.ops.H(q1)); # q1 = 1/sqrt(2)*0>+1/sqrt(2)*1>
  circuit.append(cirq.ops.CNOT(q1, q2));
  # q1 odot q2 = 1/sqrt(2)*00> + 0*01> + 0*10> + 1/sqrt(2)*11>
  if measure_q1_first:
    circuit.append(cirq.ops.measure_each(q1));
    circuit.append(cirq.ops.measure_each(q2));
  else:
    circuit.append(cirq.ops.measure_each(q2));
    circuit.append(cirq.ops.measure_each(q1));
  return circuit;

if __name__ == "__main__":
  pair_entangled_qubits();
