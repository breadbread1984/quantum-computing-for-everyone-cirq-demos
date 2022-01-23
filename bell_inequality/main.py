#!/usr/bin/python3

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
  qubit_num = 10;
  circuit = measure_network(qubit_num);
  results = cirq.Simulator().run(program = circuit, repetitions = 1);
  same_count = 0;
  total_count = 0;
  for i in range(qubit_num):
    if results.measurements['(%d, %d)' % (0, i)] == results.measurements['(%d, %d)' % (1, i)]: same_count += 1;
    total_count += 1;
  print('the probability of same measurements is %f' % (same_count / total_count));

if __name__ == "__main__":
  main();
