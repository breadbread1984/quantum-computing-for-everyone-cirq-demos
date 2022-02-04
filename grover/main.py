#!/usr/bin/python3

from absl import flags, app;
import numpy as np;
import cirq;
from models import grover;

FLAGS = flags.FLAGS;
flags.DEFINE_integer('n', default = 2, help = 'number of qubits');

def main(unused_argv):
  circuit, idx = grover(FLAGS.n);
  result = cirq.sim.Simulator().run(program = circuit, repetitions = 1);
  search_result = int(''.join([str(int(result.measurements['%d' % i])) for i in range(FLAGS.n)]),2);
  print('search result: ', search_result);
  print('true result: ', idx);

if __name__ == "__main__":
  app.run(main);
