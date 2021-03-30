#!/usr/bin/python3

import numpy as np;
import cirq;
from absl import flags;
from models import BB84;

FLAGS = flags.FLAGS;
flags.DEFINE_integer("key_length", 10, "expected key length");

def main():

  alice_basis = np.random.randint(0,2,size = (FLAGS.key_length * 4,));
  bob_basis = np.random.randint(0,2,size = (FLAGS.key_length * 4,));
  alice_measures = np.random.randint(0,2,size = (FLAGS.key_length * 4,));

  circuit = BB84(FLAGS.key_length * 4, alice_basis, bob_basis, alice_measures);
  result = cirq.Simulator().run(program = circuit, repetitions = 1);
  obtained_key = [int(result.measurements[str(i)]) for i in range(FLAGS.key_length * 4) if alice_basis[i] == bob_basis[i]];
  print(obtained_key);

if __name__ == "__main__":

  import sys;
  FLAGS(sys.argv)
  main();

