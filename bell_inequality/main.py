#!/usr/bin/python3

import numpy as np;
import cirq;
from models import predefined_results, strange_results, measure_network;

def main():
  # 1) predinfed results
  results, probability = predefined_results();
  for key, results in results.items():
    print(key, results);
  print('if results are predefined, the measure is just exposing the results. then the probability of two measure results concide with each other is %f' % probability);
  # 2) strange results
  probability = strange_results();
  print('if results are defined at measure time. then the probability of two measure results concide with each other is %f' % probability);
  # 3) experimental results
  qubit_num = 10; # how many entangled qubit pairs per test
  test_num = 100; # how many tests
  circuit = measure_network(qubit_num);
  results = cirq.Simulator().run(program = circuit, repetitions = test_num);
  same_count = 0;
  total_count = 0;
  for i in range(qubit_num):
    mask = results.measurements['(%d, %d)' % (0, i)] == results.measurements['(%d, %d)' % (1, i)];
    count = np.sum(mask.astype(np.int32));
    same_count += count;
    total_count += test_num;
  print('the probability of same measurements is %f' % (same_count / total_count));

if __name__ == "__main__":
  main();
