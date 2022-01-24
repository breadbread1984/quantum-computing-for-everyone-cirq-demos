#!/usr/bin/python3

import numpy as np;
import cirq;
from absl import app, flags;
from models import ekert, same_measures_with_different_basises_probability;

FLAGS = flags.FLAGS;
flags.DEFINE_integer('key_length', 5, "expected key length");
flags.DEFINE_boolean('has_eve', False, "whether eve presents");

def main(unused_argv):
  alice_basises = np.random.randint(low = 0, high = 3, size = (FLAGS.key_length * 3,));
  bob_basises = np.random.randint(low = 0, high = 3, size = (FLAGS.key_length * 3,));  
  eve_basises = np.random.randint(low = 0, high = 3, size = (FLAGS.key_length * 3,));
  circuit = ekert(FLAGS.key_length * 3, alice_basises, bob_basises, eve_basises if FLAGS.has_eve else None);
  # 1) alice and bob measure entangled qubit pair with their independendly selected basises
  result = cirq.Simulator().run(program = circuit, repetitions = 1);
  # 2) both send their basises to each other, and choose the measures with the same basises
  alice_measures_on_same_basis = [int(result.measurements['(0, %d)' % (i,)]) for i in range(FLAGS.key_length * 3) if alice_basises[i] == bob_basises[i]];
  bob_measures_on_same_basis = [int(result.measurements['(1, %d)' % (i,)]) for i in range(FLAGS.key_length * 3) if alice_basises[i] == bob_basises[i]];
  assert np.all(np.array(alice_measures_on_same_basis) == np.array(bob_measures_on_same_basis));
  # 3) calculate the probability of both alice and bob get the same measure when they choose different basis
  probability = same_measures_with_different_basises_probability();
  print("expected probability of both alice and bob get the same measure when they choose different basis is %f" % probability);
  alice_measures_on_different_basis = [int(result.measurements['(0, %d)' % (i,)]) for i in range(FLAGS.key_length * 3) if alice_basises[i] != bob_basises[i]];
  bob_measures_on_different_basis = [int(result.measurements['(1, %d)' % (i,)]) for i in range(FLAGS.key_length * 3) if alice_basises[i] != bob_basises[i]];
  same_count = np.sum((np.array(alice_measures_on_different_basis) == np.array(bob_measures_on_different_basis)).astype(np.int32));
  total_count = len(alice_measures_on_different_basis);
  print('actual probability of both alice and bob get the same measure when they choose different basis is %f' % (same_count / total_count));

if __name__ == "__main__":
  app.run(main);

