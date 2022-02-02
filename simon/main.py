#!/usr/bin/python3

from absl import app, flags;
import numpy as np;
import cirq;
from models import simon;

FLAGS = flags.FLAGS;
flags.DEFINE_integer('n_args', default = 3, help = 'number of arguments of the function');
flags.DEFINE_integer('repetitions', default = 10, help = 'number of repetitions');

def solve_null_space(A, eps = 1e-15):
  u, s, vh = np.linalg.svd(A);
  null_space = np.compress(s <= eps, vh, axis = 0);
  return null_space;

def main(unused_argv):
  np.random.seed(0);
  circuit = simon(FLAGS.n_args);
  result = cirq.sim.Simulator().run(program = circuit, repetitions = FLAGS.repetitions);
  measures = np.stack([np.squeeze(result.measurements['%d' % i]).astype(np.float32) for i in range(FLAGS.n_args)], axis = 0); # measures.shape = (3, repetitions)
  print("measures = ", measures);
  cov = np.dot(measures, np.transpose(measures));
  vals = np.linalg.eigvals(cov);
  if np.sum((vals != 0).astype(np.int32)) < FLAGS.n_args - 1:
    print('increase repetions to get %d linearly independent equations' % (FLAGS.n_args - 1));
  print('s = ', solve_null_space(measures.T));

if __name__ == "__main__":
  app.run(main);
