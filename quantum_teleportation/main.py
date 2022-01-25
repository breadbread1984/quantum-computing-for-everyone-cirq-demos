#!/usr/bin/python3

from absl import flags, app;
import numpy as np;
import cirq;
from models import quantum_teleportation_send, quantum_teleportation_receive;

FLAGS = flags.FLAGS;

flags.DEFINE_integer('qubit_length', 10, help = "how many qubit to send");

def main(unused_argv):
  # NOTE: keep the simulator to keep quantum status between send and receive circuit executions
  device = cirq.Simulator();
  circuit = quantum_teleportation_send(FLAGS.qubit_length);
  result = device.run(program = circuit, repetitions = 1);
  alice_measures = [int(result.measurements['(0, %d)' % (i,)]) for i in range(FLAGS.qubit_length)];
  qubit_measures = [int(result.measurements['(2, %d)' % (i,)]) for i in range(FLAGS.qubit_length)];
  control_bits = '';
  for q1, q2 in zip(qubit_measures, alice_measures):
    if q1 == 0 and q2 == 0: control_bits += '00';
    elif q1 == 0 and q2 == 1: control_bits += '01';
    elif q1 == 1 and q2 == 0: control_bits += '10';
    elif q1 == 1 and q2 == 1: control_bits += '11';
  print('alice generate control bits: %s' % control_bits);
  circuit = quantum_teleportation_receive(control_bits);
  result = device.run(program = circuit, repetitions = 1);
  bob_measures = [int(result.measurements['(1, %d)' % (i,)]) for i in range(FLAGS.qubit_length)];
  assert np.all(np.array(alice_measures) == np.array(bob_measures)), "two circuit execution doesn't use a same qubits context!";

if __name__ == "__main__":
  app.run(main);
