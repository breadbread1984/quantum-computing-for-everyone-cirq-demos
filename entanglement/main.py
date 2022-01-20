#!/usr/bin/python3

from absl import app, flags;
from models import entangled_qubits_pair;
import cirq;

def main(unused_argv):
  print('measure q1 first');
  circuit = entangled_qubits_pair(True);
  results = cirq.Simulator().run(program = circuit, repetitions = 10);
  print(results);
  print('measure q2 first');
  circuit = entangled_qubits_pair(False);
  results = cirq.Simulator().run(program = circuit, repetitions = 10);
  print(results);

if __name__ == "__main__":
  app.run(main);
