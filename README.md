# Introduction

this repository contains implements of algorithms introduced in book [Quantum Computing for Everyone](https://mitpress.mit.edu/books/quantum-computing-everyone).

# prerequisite packages

install prerequisite packages with the following command

```shell
pip3 install -r requirements.txt
```

# algorithms

| Algorithm | chapter in book | description | location |
|-----------|-----------------|-------------|-----------|
| BB84      | 3.12 Alice, Bob, Eve and the BB84 protocol | quantum key distribution algorithm | [link](./bb84) |
| entangled qubit pair | 4.7 Using the CNOT Gate to Entangle Qubits | entangled qubit pair generation | [link](./entanglement) |
| bell's inequality | 5.5 Bell's Inequality | the inequality to prove quantum mechanics agains classical explanation | [link](./bell_inequality) |
| Ekert | 5.9 The Ekert Protocol for Quantum Key Distribution | quantum key distribution algorithm | [link](./ekert) |
| Super Dense Coding | 7.9 Superdense Coding | algorithm for sending bits by qubits | [link](./superdense_coding) |
| Quantum Teleportation | 7.10 Quantum Teleportation | algorithm for sending qubits by bits | [link](./quantum_teleportation) |
| Correction | 7.11 Correction | algorithm to correct flips during communication | [link](./correction) |
| Deutsch | 8.4 Deutsch's Algorithm | algorithm proving the superior of quantum computing | [link](./deutsch) |
| Deutsch-jozsa | 8.6 Deutsch-Jozsa's Algorithm | extension of Deutsch to function of multiple inputs | [link](./deutsch_jozsa) |
| Simon | 8.7 Simon's Algorithm | one of the bounded quantum poly-nomial problems (BQP) | [list](./simon) |
| Grover | 9.2 Grover's Algorithm | data retrieval algorithm which can find the data in one try | [list](./grover) |
