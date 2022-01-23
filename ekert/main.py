#!/usr/bin/python3

import numpy as np;
import cirq;
from absl import app, flags;
from models import ekert;

FLAGS = flags.FLAGS;
flags.DEFINE_integer('key_length', 5, "expected key length");
flags.DEFINE_boolean('has_eve', False, "whether eve presents");

def main(unused_argv):
  alice_basises = np.random.randint(low = 0, high = 3, size = (FLAGS.key_length * 3,));
  bob_basises = np.random.randint(low = 0, high = 3, size = (FLAGS.key_length * 3,));  eve_basises = np.random.randint(low = 0, high = 3, size = (FLAGS.key_length * 3,));
  circuit = ekert(FLAGS.key_length * 3, alice_basises, bob_basises);
  result = cirq.Simulator().run(program = circuit, repetitions = 1);

if __name__ == "__main__":
  app.run(main);

