#!/usr/bin/python3

from re import search;
import numpy as np;
import cirq;
from absl import app, flags;
from models import superdense_coding;

FLAGS = flags.FLAGS;
flags.DEFINE_string('message', default = None, help = 'message to send');

def main(unused_argv):
  assert search('[^01]', FLAGS.message) is None, "can only send string composed of 0 and 1";
  assert len(FLAGS.message) % 2 == 0, "length of the message must be even";
  circuit = superdense_coding(FLAGS.message);
  result = cirq.Simulator().run(program = circuit, repetitions = 1);
  received_message = '';
  for i in range(len(FLAGS.message) // 2):
    q1 = result.measurements['(0, %d)' % i];
    q2 = result.measurements['(1, %d)' % i];
    if q1 == 0 and q2 == 0: received_message += '00';
    elif q1 == 0 and q2 == 1: received_message += '01';
    elif q1 == 1 and q2 == 0: received_message += '10';
    elif q1 == 1 and q2 == 1: received_message += '11';
  print('bob received message: %s' % received_message);

if __name__ == "__main__":
  app.run(main);

