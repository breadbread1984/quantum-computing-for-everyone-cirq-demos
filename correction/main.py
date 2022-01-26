#!/usr/bin/python3

from absl import flags, app;
import cirq;
from models import communication, correction;

FLAGS = flags.FLAGS;

flags.DFEINE_integer('qubit_num', 10, help = 'how many qubit to send');

def main(unused_argv):
  device = cirq.sim.Simulator();
  circuit = communication(FLAGS.qubit_num);
  result = device.run(program = circuit, repetitions = 1);
  correction_code = '';
  for i in range(FLAGS.qubit_num):
    correction_code += int(result.measurements['(3, %d)' % i]);
    correction_code += int(result.measurements['(4, %d)' % i]);
  print('correction code is %s' % correction_code);
  circuit = correction(correction_code);
  result = device.run(program = circuit, repetitions = 1);
  q1,q2,q3 = '','','';
  for i in range(FLAGS.qubit_num):
    q1 += int(result.measurements['(0, %d)' % i]);
    q2 += int(result.measurements['(1, %d)' % i]);
    q3 += int(result.measurements['(2, %d)' % i]);
    assert q1[-1] == q2[-1] and q2[-1] == q3[-1], 'correction failed';
  print('q1: %s' % q1);
  print('q2: %s' % q2);
  print('q3: %s' % q3);


