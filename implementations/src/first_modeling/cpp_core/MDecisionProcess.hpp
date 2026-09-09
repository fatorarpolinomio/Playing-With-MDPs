#pragma once

#include <Eigen/Dense>
#include <vector>

class AgentEnvironment {
private:
  double discountRate;
  double rewardReturn;
  double policy;
  std::vector<double> returns;
  std::vector<double> actions;
  std::vector<double> states;
  std::vector<Eigen::MatrixXd> transFuncPerAction;
  std::vector<double> stateValues; // Lista de pontuações

  double calculateReturn(double discountRate, double rewardReturn,
                         std::vector<double> returns);

  // Essas aqui vão mudar para cada problema que estaremos modelando
  // Dependendo da situação, já teremos tudo tabelado na forma de uma matriz
  // Para cenários onde teremos um grande quantidade de probalidades,
  // teremos que "automatizar" na forma de um algoritmo
  //
  // Essas funções vão se basear em consulta à matriz de transição
  double calculatePolicyProb(double action, double state);
  double calculateTransFunc(double action, double startState, double returns,
                            double states,
                            std::vector<Eigen::MatrixXd> &transFuncPerAction);

public:
  // Getters
  std::vector<std::vector<std::vector<double>>> getTransFuncAsVectors();
  double getDiscountRate() { return discountRate; }
  double getRewardReturn() { return rewardReturn; }
  double getPolicy() { return policy; }
  std::vector<double> getReturns() { return returns; }
  std::vector<double> getActions() { return actions; }
  std::vector<double> getStates() { return states; }
  const std::vector<double> &getStateValues() const { return stateValues; }
  double getStateValueByIndex(int index) { return stateValues[index]; }

  // Setters
  void setTransFuncFromVectors(
      const std::vector<std::vector<std::vector<double>>> &matrizes3D);
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
  void setStateValues(std::vector<double> stateValues) {
    this->stateValues = stateValues;
  }
  void setStateValueByIndex(int index, double value) {
    this->stateValues[index] = value;
  }

  void applyCalculateReturn(double discountRate, double rewardReturn,
                            std::vector<double> returns);
  double applyCalculatePolicyProb(double action, double state);
  double applyCalculateTransFunc(double action, double startState,
                                 double returns, double states);
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
                             const std::vector<double> &currentValues,
                             const std::vector<double> &returns,
                             const std::vector<double> &states);
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
  std::vector<double> ValueIteration(double discountRate, double rewardValue,
                                     double threshold,
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
  std::vector<double> applyValueIter(double discountRate, double rewardValue,
                                     double threshold,
                                     std::vector<double> actions,
                                     std::vector<double> returns,
                                     std::vector<double> states) {
    return ValueIteration(discountRate, rewardValue, threshold, actions,
                          returns, states);
  }

  // Getters
  double getThreshold() { return threshold; }
  // Setters
  void setThreshold(double value) { threshold = value; }
};
