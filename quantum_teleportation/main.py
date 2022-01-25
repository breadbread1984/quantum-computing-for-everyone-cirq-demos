#!/usr/bin/python3

from absl import flags, app;
import cirq;
from models import quantum_teleportation_send, quantum_teleportation_receive;

FLAGS = flags.FLAGS;

flags.DEFINE_integer('qubit_length', 10, help = "how many qubit to send");

def main(unused_argv):
  circuit = quantum_teleportation_send(FLAGS.qubit_length);
  result = cirq.Simulator().run(program = circuit, repetitions = 1);
  alice_measures = [int(result.measurements['(0, %d)' % (i,)]) for i in range(FLAGS.qubit_length)];
  qubit_measures = [int(result.measurements['(2, %d)' % (i,)]) for i in range(FLAGS.qubit_length)];
  message = '';
  for q1, q2 in zip(qubit_measures, alice_measures):
    if q1 == 0 and q2 == 0: message += '00';
    elif q1 == 0 and q2 == 1: message += '01';
    elif q1 == 1 and q2 == 0: message += '10';
    elif q1 == 1 and q2 == 1: message += '11';
  print(message);

if __name__ == "__main__":
  app.run(main);
