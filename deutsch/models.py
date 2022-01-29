#!/usr/bin/python3

import cirq;

def const_func(circuit, q1, q2):
  # f(x) = 0, in other words y^f(x)=y
  circuit.append(cirq.ops.I(q1));
  circuit.append(cirq.ops.I(q2));

def balance_func(circuit, q1, q2):
  # f(x) = x
  circuit.append(cirq.ops.CNOT(q1, q2));

def deutsch(use_balance = True):
  oracle = const_func if use_balance == False else balance_func;
  q1 = cirq.devices.LineQubit(0);
  q2 = cirq.devices.LineQubit(1);
  circuit = cirq.circuits.Circuit();
  circuit.append(cirq.ops.X(q2));
  circuit.append(cirq.ops.H(q1));
  circuit.append(cirq.ops.H(q2));
  oracle(circuit, q1, q2);
  circuit.append(cirq.ops.H(q1));
  circuit.append(cirq.measure_each(q1));
  return circuit;
