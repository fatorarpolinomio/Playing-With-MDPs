#ifndef MDPs_HPP
#define MDPs_HPP

#include <vector>

class AgentEnvironment {
private:
  double discountRate;
  double rewardReturn;
  double policy;
  std::vector<double> returns;
  std::vector<double> actions;
  std::vector<double> states;

public:
  double calculateReturn(double discountRate, double rewardReturn,
                         std::vector<double> returns);

  // Essas aqui vão mudar para cada problema que estaremos modelando
  // Dependendo da situação, já teremos tudo tabelado na forma de uma matriz
  // Para cenários onde teremos um grande quantidade de probalidades,
  // teremos que "automatizar" na forma de um algoritmo
  virtual double calculatePolicyProb(double action, double state);
  virtual double calculateTransFunc(double actions, double returns,
                                    double states);

  // Getters
  double getDiscountRate() { return discountRate; }
  double getRewardReturn() { return rewardReturn; }
  double getPolicy() { return policy; }
  std::vector<double> getReturns() { return returns; }
  std::vector<double> getActions() { return actions; }
  std::vector<double> getStates() { return states; }

  // Setters
  void setDiscountRate(double discountRate) {
    this->discountRate = discountRate;
  }
  void setRewardReturn(double rewardReturn) {
    this->rewardReturn = rewardReturn;
  }
  void setPolicy(double value) { policy = value; }
  void setReturns(std::vector<double> returns) { this->returns = returns; }
  void setActions(std::vector<double> actions) { this->actions = actions; }
  void setStates(std::vector<double> states) { this->states = states; }
  void applyCalculateReturn(double discountRate, double rewardReturn,
                            std::vector<double> returns);
};

class ValueFunctions : public AgentEnvironment {
private:
  double rewardValue;
  double transitionFunctionValue;
  std::vector<double> currentValues; // Tabela de valores para iterar

  double bellmanEquation(double state, double discountRate, double rewardValue,
                         std::vector<double> currentValues,
                         std::vector<double> actions,
                         std::vector<double> returns,
                         std::vector<double> states);

public:
  double actionValueFunction(double state, double action, double discountRate,
                             std::vector<double> currentValues,
                             std::vector<double> returns,
                             std::vector<double> states);
  // Construtor
  ValueFunctions(double rewardValue, double discountRate);
  // Getters
  double getRewardValue() { return rewardValue; }
  double getTransitionFunctionValue() { return transitionFunctionValue; }

  // Setters
  void setRewardValue(double value) { rewardValue = value; }
  void setTransitionFunctionValue(double value) {
    transitionFunctionValue = value;
  }

  // Aplicando métodos
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
  double ValueIteration(double discountRate, double rewardValue,
                        double threshold, std::vector<double> &currentValues,
                        std::vector<double> actions,
                        std::vector<double> returns,
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
