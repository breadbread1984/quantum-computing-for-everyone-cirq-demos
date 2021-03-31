#!/usr/bin/python3

import numpy as np;
import cirq;
from absl import flags;
from models import BB84;

FLAGS = flags.FLAGS;
flags.DEFINE_integer("key_length", 5, "expected key length");

def main():

  alice_basis = np.random.randint(0,2,size = (FLAGS.key_length * 4,));
  bob_basis = np.random.randint(0,2,size = (FLAGS.key_length * 4,));
  alice_measures = np.random.randint(0,2,size = (FLAGS.key_length * 4,));

  circuit = BB84(FLAGS.key_length * 4, alice_basis, bob_basis, alice_measures);
  while True:
    result = cirq.Simulator().run(program = circuit, repetitions = 1);
    # 1) what alice knows exclusively
    alice_measures_on_same_basis = [alice_measures[i] for i in range(FLAGS.key_length * 4) if alice_basis[i] == bob_basis[i]];
    # 2) what bob knows exclusively
    bob_measures_on_same_basis = [int(result.measurements[str(i)]) for i in range(FLAGS.key_length * 4) if alice_basis[i] == bob_basis[i]];
    # 3) alice choose half of the alice_key to share with bob to test whether there is an eve eavesdropping
    if len(alice_measures_on_same_basis) < 2: continue;
    # idx is sent from alice to bob
    indices = np.random.choice(range(len(alice_measures_on_same_basis)), len(alice_measures_on_same_basis) // 2, replace = False);
    # 3.1) if no eve exists both alice and bob use the rest of the measures taken on the same basis as symmetric key
    alice_chosed_measures = np.array(alice_measures_on_same_basis)[indices];
    bob_chosed_measures = np.array(bob_measures_on_same_basis)[indices];
    if np.all(alice_chosed_measures == bob_chosed_measures):
      print("no Eve eavesdropping");
      final_alice_key = [alice_measures_on_same_basis[index] for index in range(len(alice_measures_on_same_basis)) if index not in indices];
      final_bob_key = [bob_measures_on_same_basis[index] for index in range(len(bob_measures_on_same_basis)) if index not in indices];
      print("alice's key = ", final_alice_key);
      print("bob's key = ", final_bob_key);
      break;
    else:
      print("detected Eve eavesdropping, do the key distribution process again");
      continue;

if __name__ == "__main__":

  import sys;
  FLAGS(sys.argv)
  main();

