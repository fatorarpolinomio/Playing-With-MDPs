#include <Eigen/Dense>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>

class TransitionFunction {};

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
};

class PolicyEvaluation {

  void applyPolicyEval(double policy, double threshold) {}
};
