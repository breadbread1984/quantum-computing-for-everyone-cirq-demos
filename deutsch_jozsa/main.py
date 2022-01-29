#!/usr/bin/python3

from re import search;
from absl import flags, app;
import cirq;
from models import deutsch_jozsa;

FLAGS = flags.FLAGS;

flags.DEFINE_boolean('use_balance', default = False, help = 'whether use balance function as oracle');
flags.DEFINE_integer('n_args', default = 3, help = 'number of arguments of the function');
flags.DEFINE_integer('repetitions', default = 10, help = 'maximum measure repetitions before make predicate');

def main(unused_argv):
  circuit = deutsch_jozsa(FLAGS.n_args, FLAGS.use_balance);
  result = cirq.sim.Simulator().run(program = circuit, repetitions = FLAGS.repetitions);
  measures = ['' for i in range(FLAGS.repetitions)];
  for i in range(FLAGS.n_args):
    for r in range(FLAGS.repetitions):
      measures[r] += str(int(result.measurements['%d' % i][r]));
  print('measures of qubits in %d repetitions are ' % FLAGS.repetitions, measures);
  for measure in measures:
    if search('[^0]', measure) is not None:
      print('the function is a balance function with error probability 0');
      return;
  print('the function is a constant function with error probability %f' % (0.5**FLAGS.repetitions));
  return;
  
if __name__ == "__main__":
  app.run(main);
