#!/usr/bin/python3

from absl import app, flags;
import cirq;
from models import simon;

FLAGS = flags.FLAGS;
flags.DEFINE_integer('n_args', default = 3, help = 'number of arguments of the function');

def main(unused_argv):
  circuit = simon(FLAGS.n_args);
  result = cirq.sim.Simulator().run(program = circuit, repetitions = 1);
  print(result);

if __name__ == "__main__":
  app.run(main);
