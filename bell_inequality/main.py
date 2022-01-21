#!/usr/bin/python3

from absl import app, flags;
import cirq;
from models import predefined_results, strange_results;

FLAGS = flags.FLAGS;

def add_options():
  flags.DEFINE_boolean('predefined', default = False, help = 'whether the measure results are predefined');

def main(unused_argv):
  if FLAGS.predefined:
    print('if results are predefined, the measure is just exposing the results. then the probability of two measure results concides with each other is %f', predefined_results());
  else:
    pass;

if __name__ == "__main__":
  add_options();
  app.run(main);
