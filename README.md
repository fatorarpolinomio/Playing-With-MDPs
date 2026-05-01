# Playing-With-MDPs

A series of experiments with the Markovian Decision Process framework!

The MDP framework is the base of the Reinforcement Learning, and it's extreme flexible!

In this repository, i'll save some experimentations with the [Gymnasium](https://gymnasium.farama.org/) API on Python Scripts and some code refactoring in C++ (just because i like this language and i feel more estimulated). There will be some problems that will get resolved by the methods & algorithms of the framework. This will be the base for my final project of "Leisure & Work", my scientific initiation.

As the time goes, my objetive is to get distance from an already-made API and build my own API to structure my project.

## Agent-Enviroment

A MDP is mostly defined by three finites sets:

### **State (S)**: represents the actual situation of the agent in the enviroment. The simble S+ includes the normal states + terminal state;

### **Action (A)**: the set of all possible decisions that the agent can take. Frequently described by A(s) to indicate that the possible actions can change for each state.

### **Reward (R)**: a numeric value that the enviroment returns after an action, that's feedback (positive or negative) for the agent.

![Agent-Enviroment](/images/mdpFlow.png)

## Tecnologies

### [Gymnasium](https://gymnasium.farama.org/): "An API standard for reinforcement learning with a diverse collection of reference environments."

### [Matplotlib](https://matplotlib.org/): "Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python."

### [Cython](https://cython.org/): "Cython is an optimising static compiler for both the Python programming language and the extended Cython programming language (based on Pyrex). It makes writing C extensions for Python as easy as Python itself."

## Bibliography

### _Reinforcement Learning, An Introduction. Second Edition - Sutton & Barto_
