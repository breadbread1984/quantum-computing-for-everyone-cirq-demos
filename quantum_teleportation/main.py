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
  circuit, rotations = quantum_teleportation(FLAGS.qubit_length);
  result = device.simulate(program = circuit);

if __name__ == "__main__":
  app.run(main);
