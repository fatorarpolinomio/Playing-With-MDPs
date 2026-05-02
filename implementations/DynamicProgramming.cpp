#include "Eigen/Core"
#include <Eigen/Dense>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>

class ValueFunctions {
private:
  double rewardValue;
  double discountRate;
  double rewardReturn;
  double policy;
  double transitionFunctionValue;
  std::vector<double> returns;
  std::vector<double> actions;
  std::vector<double> states;

  double calculateReturn(double discountRate, double rewardReturn,
                         std::vector<double> returns) {
    this->rewardReturn = 0;
    double tempDiscount = discountRate;
    for (int i = 0; i < returns.size(); i++) {
      tempDiscount = pow(discountRate, i);
      this->rewardReturn += tempDiscount * returns[i];
    }
    return rewardReturn;
  }

  // Fazer
  double calculatePolicyProb(double action, double state) { return 0.0; }

  // Fazer
  double calculateTransFunc(double actions, double returns, double states) {
    return 0.0;
  }

  // Preciso ajeitar algumas coisas, mas pelo menos o esqueleto conceitual tá
  // feito Provavelmente, terei que implementar algoritmos de programação
  // dinâmica mesmo, como backtracking porque a complexidade de tempo vai
  // explodir aqui
  double bellmanEquation(double state, double discountRate, double rewardValue,
                         std::vector<double> actions,
                         std::vector<double> returns,
                         std::vector<double> states) {
    double policyValue = 0;
    for (double action : actions) {
      policyValue += calculatePolicyProb(action, state);
    }

    double transitionFunctionValue = 0;
    for (double eachState : states) {
      // Tá meio esquisito
      transitionFunctionValue +=
          discountRate *
          bellmanEquation(eachState, discountRate, rewardValue, actions,
                          returns, states) *
          calculateTransFunc(actions[0], returns[0], eachState);
    }
    for (double reward : returns) {
      // Tá meio esquisito
      transitionFunctionValue +=
          reward * calculateTransFunc(actions[0], reward, states[0]);
    }

    return policyValue * transitionFunctionValue;
  }

public:
  // Construtor
  ValueFunctions(double rewardValue, double discountRate) {
    this->rewardValue = rewardValue;
    this->discountRate = discountRate;
  }
  // Getters (em breve, vão para o .hpp)
  double getRewardValue() { return rewardValue; }
  double getDiscountRate() { return discountRate; }
  double getRewardReturn() { return rewardReturn; }
  double getPolicy() { return policy; }
  double getTransitionFunctionValue() { return transitionFunctionValue; }
  std::vector<double> getReturns() { return returns; }
  std::vector<double> getActions() { return actions; }
  std::vector<double> getStates() { return states; }

  // Setters (em breve, vão para o .hpp)
  void setRewardValue(double value) { rewardValue = value; }
  void setDiscountRate(double value) { discountRate = value; }
  void setRewardReturn(double value) { rewardReturn = value; }
  void setPolicy(double value) { policy = value; }
  void setTransitionFunctionValue(double value) {
    transitionFunctionValue = value;
  }
  void setReturns(std::vector<double> value) { returns = value; }
  void setActions(std::vector<double> value) { actions = value; }
  void setStates(std::vector<double> value) { states = value; }

  // Aplicando métodos
  void applyCalculateReturn(double discountRate, double rewardReturn,
                            std::vector<double> returns) {
    this->rewardReturn = calculateReturn(discountRate, rewardReturn, returns);
  }
  void applyBellmanEquation(double discountRate, double rewardReturn,
                            std::vector<double> returns,
                            std::vector<double> states,
                            std::vector<double> actions) {}
};

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
