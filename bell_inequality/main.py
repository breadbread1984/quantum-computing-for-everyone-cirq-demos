#!/usr/bin/python3

from absl import app, flags;
import cirq;
from models import predefined_results, strange_results;

FLAGS = flags.FLAGS;

def add_options():
  flags.DEFINE_boolean('predefined', default = False, help = 'whether the measure results are predefined');

def main(unused_argv):
  if FLAGS.predefined:
    results, probability = predefined_results();
    for key, results in results.items():
      print(key, results);
    print('if results are predefined, the measure is just exposing the results. then the probability of two measure results concide with each other is %f' % probability);
  else:
    probability = strange_results();
    print('if results are defined at measure time. then the probability of two measure results concide with each other is %f' % probability);

if __name__ == "__main__":
  add_options();
  app.run(main);
