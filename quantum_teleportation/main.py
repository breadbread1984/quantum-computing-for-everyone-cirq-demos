#!/usr/bin/python3

from absl import flags, app;
import numpy as np;
import cirq;
from models import quantum_teleportation;

FLAGS = flags.FLAGS;

flags.DEFINE_integer('qubit_length', 10, help = "how many qubit to send");

def main(unused_argv):
  # NOTE: keep the simulator to keep quantum status between send and receive circuit executions
  device = cirq.Simulator();
  # 1) teleport classical bits
  x_flips = np.random.randint(low = 0, high = 2, size = (FLAGS.qubit_length,));
  print('send qubits: ', x_flips);
  circuit = quantum_teleportation(x_flips, measure = True);
  result = device.run(program = circuit, repetitions = 1);
  # get measure results to verify the teleportation
  qubits = '';
  for i in range(FLAGS.qubit_length):
    qubits += str(int(result.measurements('(1, %d)' % i)));
  print('received qubits: ', qubits);
  # 2) teleport qubits
  rotations = np.random.uniform(low = (0, 0, 0), high = (np.pi, np.pi, 2 * np.pi), size = (FLAGS.qubit_length,3));
  circuit = quantum_teleportation(rotations);
  result = device.run(program = circuit, repetitions = 1);

if __name__ == "__main__":
  app.run(main);
