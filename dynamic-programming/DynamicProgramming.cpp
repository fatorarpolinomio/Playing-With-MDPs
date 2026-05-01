#include <iostream>

class ValueFunctions {

  double bellmanEquation() { return 0.0; }
};

class PolicyEvaluation {

  void applyPolicyEval(double policy, double threshold) {}
};

class DynamicProg {

  // Input pi, the policy to be evaluated
  // Algorithm parameter: a small threshold theta > 0 determining accuracy of
  // estimation Initialize V (s), for all s in S+ , arbitrarily except that V
  // (terminal) = 0
  void policyEvaluation() {}

  void policyIteration() {}
  void valueIteration() {}
};
