#!/usr/bin/python3

from absl import app, flags;
import numpy as np;
import cirq;
from models import simon;

FLAGS = flags.FLAGS;
flags.DEFINE_integer('n_args', default = 3, help = 'number of arguments of the function');
flags.DEFINE_integer('repetitions', default = 10, help = 'number of repetitions');

def main(unused_argv):
  np.random.seed(0);
  circuit, m = simon(FLAGS.n_args);
  result = cirq.sim.Simulator().run(program = circuit, repetitions = FLAGS.repetitions);
  print(result);

if __name__ == "__main__":
  app.run(main);
