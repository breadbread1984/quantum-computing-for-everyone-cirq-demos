#!/usr/bin/python3

import numpy as np;
import cirq;
from absl import flags;
from models import BB84;

FLAGS = flags.FLAGS;
flags.DEFINE_integer("key_length", 5, "expected key length");

def main():

  alice_basises = np.random.randint(0,2,size = (FLAGS.key_length * 4,));
  bob_basises = np.random.randint(0,2,size = (FLAGS.key_length * 4,));

  circuit, alice_measures = BB84(FLAGS.key_length * 4, alice_basises, bob_basises);
  while True:
    result = cirq.Simulator().run(program = circuit, repetitions = 1);
    # 1) what alice knows exclusively
    alice_measures_on_same_basis = [alice_measures[i] for i in range(FLAGS.key_length * 4) if alice_basises[i] == bob_basises[i]];
    # 2) what bob knows exclusively
    bob_measures_on_same_basis = [int(result.measurements[str(i)]) for i in range(FLAGS.key_length * 4) if alice_basises[i] == bob_basises[i]];
    # 3) alice choose half of the alice_key to share with bob to test whether there is an eve eavesdropping
    if len(alice_measures_on_same_basis) < FLAGS.key_length / 2: continue;
    # idx is sent from alice to bob
    indices = np.random.choice(range(len(alice_measures_on_same_basis)), len(alice_measures_on_same_basis) // 2, replace = False);
    alice_chosed_measures = np.array(alice_measures_on_same_basis)[indices]; # alice chooses privately
    bob_chosed_measures = np.array(bob_measures_on_same_basis)[indices]; # bob chooses privately
    if np.all(alice_chosed_measures == bob_chosed_measures):
      # 3.1) if no eve exists both alice and bob use the rest of the measures taken on the same basis as symmetric key
      print("no Eve eavesdropping");
      final_alice_key = [alice_measures_on_same_basis[index] for index in range(len(alice_measures_on_same_basis)) if index not in indices]; # alice chooses privately
      final_bob_key = [bob_measures_on_same_basis[index] for index in range(len(bob_measures_on_same_basis)) if index not in indices]; # bob chooses privately
      print("alice's key = ", final_alice_key);
      print("bob's key = ", final_bob_key);
      break;
    else:
      # 3.2) else do the key distribution process again
      print("detected Eve eavesdropping, do the key distribution process again");
      continue;

if __name__ == "__main__":

  import sys;
  FLAGS(sys.argv)
  main();

