#!/usr/bin/python3

from absl import flags, app;
import cirq;
from models import correction;

FLAGS = flags.FLAGS;

flags.DEFINE_integer('qubit_num', 5, help = 'how many qubit to send');

def main(unused_argv):
  circuit = correction(FLAGS.qubit_num);
  result = cirq.sim.Simulator().run(program = circuit, repetitions = 1);
  q1,q2,q3 = '','','';
  for i in range(FLAGS.qubit_num):
    q1 += str(int(result.measurements['(0, %d)' % i]));
    q2 += str(int(result.measurements['(1, %d)' % i]));
    q3 += str(int(result.measurements['(2, %d)' % i]));
    assert q1[-1] == q2[-1] and q2[-1] == q3[-1], 'correction failed';
  print('q1: %s' % q1);
  print('q2: %s' % q2);
  print('q3: %s' % q3);

if __name__ == "__main__":
  app.run(main);

