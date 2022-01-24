#!/usr/bin/python3

from absl import flags, app;
import cirq;
from models import quantum_teleportation_send, quantum_teleportation_receive;

FLAGS = flags.FLAGS;

flags.DEFINE_integer('qubit_length', 10, help = "how many qubit to send");

def main(unused_argv):
  circuit, bob_qubits = quantum_teleportation_send(FLAGS.qubit_length);
  print(bob_qubits);

if __name__ == "__main__":
  app.run(main);
