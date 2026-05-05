#include "MDPs.hpp"

class DynamicProgramming : public ValueFunctions {

private:
  double threshold;

  void PolicyEvaluation(double policy, double threshold) {}
  void PolicyIteration(double threshold) {}
  void ValueIteration(double threshold) {}

public:
  // Construtor
  DynamicProgramming(double rewardValue, double discountRate, double threshold)
      : ValueFunctions(rewardValue, discountRate), threshold(threshold) {}

  void applyPolicyEval(double policy, double threshold) {
    PolicyEvaluation(policy, threshold);
  }
  void applyPolicyIter(double threshold) { PolicyIteration(threshold); }
  void applyValueIter(double threshold) { ValueIteration(threshold); }

  // Getters (em breve, vão para o .hpp)
  double getThreshold() { return threshold; }
  // Setters (em breve, vão para o .hpp)
  void setThreshold(double value) { threshold = value; }
};
