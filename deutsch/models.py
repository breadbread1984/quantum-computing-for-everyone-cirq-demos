#!/usr/bin/python3

import cirq;

def const_func(circuit, q1, q2):
  # f(x) = 
  circuit.append(cirq.ops.CNOT(q1, q2)); # q1 odot (q1 ^ q2)
  circuit.append(cirq.ops.X(q2)); # 

def balance_func(circuit, q1, q2):
  # f(x) = x
  circuit.append(cirq.ops.CNOT(q1, q2));

def deutsch(oracle = const_func):
  circuit = cirq.circuits.Circuit();
  q1 = cirq.devices.LineQubit(0);
  q2 = cirq.devices.LineQubit(1);

