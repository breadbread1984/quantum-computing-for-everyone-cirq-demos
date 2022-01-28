#!/usr/bin/python3

from absl import flags, app;
import cirq;
from models import deutsch;

FLAGS = flags.FLAGS;

flags.DEFINE_boolean('use_balance', default = False, help = 'whether use balance function as oracle');

def main(unused_argv):
  circuit = deutsch(FLAGS.use_balance);
  result = cirq.sim.Simulator.run(program = circuit, repetitions = 1);
  print('measure %d' % int(result.measurements['0']));

if __name__ == "__main__":
  app.run(main);
