#!/usr/bin/python3

import numpy as np;
import cirq;
from absl import flags;
from models import BB84;

FLAGS = flags.FLAGS;
flags.DEFINE_integer("qubit_num", 10, "number of qubits");

def main():

  alice_basis = np.random.randint(0,2,size = (FLAGS.qubit_num,));
  bob_basis = np.random.randint(0,2,size = (FLAGS.qubit_num,));
  alice_measures = np.random.randint(0,2,size = (FLAGS.qubit_num,));

  circuit = BB84(FLAGS.qubit_num, alice_basis, bob_basis, alice_measures);
  result = cirq.Simulator().run(program = circuit, repetitions = 1);
  print(result);

if __name__ == "__main__":

  main();

