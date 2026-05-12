#ifndef MDPs_HPP
#define MDPs_HPP

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
  std::vector<double> currentValues; // Tabela de valores para iterar

  double calculateReturn(double discountRate, double rewardReturn,
                         std::vector<double> returns);
  double calculatePolicyProb(double action, double state);
  double bellmanEquation(double state, double discountRate, double rewardValue,
                         std::vector<double> currentValues,
                         std::vector<double> actions,
                         std::vector<double> returns,
                         std::vector<double> states);
  double actionValueFunction(double state, double action,
                             std::vector<double> currentValues,
                             std::vector<double> actions,
                             std::vector<double> returns,
                             std::vector<double> states);

public:
  double calculateTransFunc(double actions, double returns, double states);
  // Construtor
  ValueFunctions(double rewardValue, double discountRate);
  // Getters
  double getRewardValue() { return rewardValue; }
  double getDiscountRate() { return discountRate; }
  double getRewardReturn() { return rewardReturn; }
  double getPolicy() { return policy; }
  double getTransitionFunctionValue() { return transitionFunctionValue; }
  std::vector<double> getReturns() { return returns; }
  std::vector<double> getActions() { return actions; }
  std::vector<double> getStates() { return states; }

  // Setters
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
                            std::vector<double> returns);
  double applyBellmanEquation(double state, double discountRate,
                              double rewardValue,
                              std::vector<double> currentValues,
                              std::vector<double> actions,
                              std::vector<double> returns,
                              std::vector<double> states);
};

// Algoritmos de programação dinâmica para avaliação de política
class DynamicProgramming : public ValueFunctions {

private:
  double threshold; // Limite de convergência para os métodos de avaliação de
                    // política

  void PolicyEvaluation(double discountRate, double rewardValue,
                        double threshold, std::vector<double> &currentValues,
                        std::vector<double> actions,
                        std::vector<double> returns,
                        std::vector<double> states);
  void PolicyIteration(double discountRate, double rewardValue,
                       double threshold, std::vector<double> &currentValues,
                       std::vector<double> actions, std::vector<double> returns,
                       std::vector<double> states,
                       std::vector<double> &policyPerState);
  void ValueIteration(double discountRate, double rewardValue, double threshold,
                      std::vector<double> &currentValues,
                      std::vector<double> actions, std::vector<double> returns,
                      std::vector<double> states);

public:
  // Construtor
  DynamicProgramming(double rewardValue, double discountRate, double threshold);

  void applyPolicyEval(double discountRate, double rewardValue,
                       double threshold, std::vector<double> &currentValues,
                       std::vector<double> actions, std::vector<double> returns,
                       std::vector<double> states) {
    PolicyEvaluation(discountRate, rewardValue, threshold, currentValues,
                     actions, returns, states);
  }
  void applyPolicyIter(double discountRate, double rewardValue,
                       double threshold, std::vector<double> &currentValues,
                       std::vector<double> actions, std::vector<double> returns,
                       std::vector<double> states,
                       std::vector<double> &policyPerState) {
    PolicyIteration(discountRate, rewardValue, threshold, currentValues,
                    actions, returns, states, policyPerState);
  }
  void applyValueIter(double discountRate, double rewardValue, double threshold,
                      std::vector<double> &currentValues,
                      std::vector<double> actions, std::vector<double> returns,
                      std::vector<double> states) {
    ValueIteration(discountRate, rewardValue, threshold, currentValues, actions,
                   returns, states);
  }

  // Getters
  double getThreshold() { return threshold; }
  // Setters
  void setThreshold(double value) { threshold = value; }
};

#endif // MDPs_HPP
