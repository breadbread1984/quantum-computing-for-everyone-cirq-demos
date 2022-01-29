#!/usr/bin/python3

from re import search;
from absl import flags, app;
import cirq;
from models import deutsch_jozsa;

FLAGS = flags.FLAGS;

flags.DEFINE_boolean('use_balance', default = False, help = 'whether use balance function as oracle');
flags.DEFINE_integer('n_args', default = 6, help = 'number of arguments of the function');

def main(unused_argv):
  circuit = deutsch_jozsa(FLAGS.n_args, FLAGS.use_balance);
  result = cirq.sim.Simulator().run(program = circuit, repetitions = 1);
  measure = '';
  for i in range(FLAGS.n_args):
    measure += str(int(result.measurements['%d' % i]));
  print('measures of qubits are %s' % measure);
  if search('[^0]', measure) is not None:
    print('the function is a balance function');
  else:
    print('the function is a constant function');
  
if __name__ == "__main__":
  app.run(main);
