#include "MDecisionProcess.hpp"
#include <algorithm>
#include <cmath>
#include <iostream>
#include <vector>

DynamicProgramming::DynamicProgramming(double rewardValue, double discountRate,
                                       double threshold)
    : ValueFunctions(rewardValue, discountRate), threshold(threshold) {}

// "Se eu seguir sempre essa estratégia,
// quanto de recompensa vou acumular saindo de cada estado?"
void DynamicProgramming::PolicyEvaluation(double discountRate,
                                          double rewardValue, double threshold,
                                          std::vector<double> &currentValues,
                                          std::vector<double> actions,
                                          std::vector<double> returns,
                                          std::vector<double> states) {
  // Inicializa maior que o threshold para entrar no while
  double delta = threshold + 1.0;
  while (delta > threshold) {
    delta = 0.0;
    for (int i = 0; i < states.size(); i++) {
      double value = currentValues[i];
      currentValues[i] =
          applyBellmanEquation(states[i], discountRate, rewardValue,
                               currentValues, actions, returns, states);
      // Atualiza o delta com a maior diferença encontrada NESTA varredura
      delta = std::max(delta, std::abs(value - currentValues[i]));
    }
  }
}

// Passando policyPerState por referência (&) e retornando void
void DynamicProgramming::PolicyIteration(double discountRate,
                                         double rewardValue, double threshold,
                                         std::vector<double> &currentValues,
                                         std::vector<double> actions,
                                         std::vector<double> returns,
                                         std::vector<double> states,
                                         std::vector<double> &policyPerState) {
  while (true) {
    // Policy Evaluation (Avalia a política atual)
    PolicyEvaluation(discountRate, rewardValue, threshold, currentValues,
                     actions, returns, states);

    bool policyStable = true;

    // Policy Improvement (Melhora a política)
    for (int i = 0; i < states.size(); i++) {
      double oldAction = policyPerState[i];

      // Variáveis para encontrar a melhor ação para ESTE estado
      double bestActionValue = -1e9;
      double bestAction = actions[0];

      for (double action : actions) {

        double expectedActionValue = actionValueFunction(
            states[i], action, discountRate, currentValues, returns, states);

        if (expectedActionValue > bestActionValue) {
          bestActionValue = expectedActionValue;
          bestAction = action;
        }
      }

      // Atualiza a política com a melhor ação encontrada
      policyPerState[i] = bestAction;

      // Verifica se a política mudou
      if (oldAction != policyPerState[i]) {
        policyStable = false;
      }
    }

    // Critério de parada: se a política não mudou, terminamos.
    // Como currentValues e policyPerState são referências, as mudanças
    // já estão salvas, basta dar um return vazio.
    if (policyStable) {
      return;
    }
  }
}

std::vector<double> DynamicProgramming::ValueIteration(
    double discountRate, double rewardValue, double threshold,
    std::vector<double> actions, std::vector<double> returns,
    std::vector<double> states) {
  // Inicializa maior que o threshold para entrar no while
  double delta = threshold + 1.0;

  std::vector<double> initialValues(states.size(), 0.0);
  std::vector<double> optimalPolicy(states.size(), 0.0);
  this->setStateValues(initialValues);

  while (delta > threshold) {
    delta = 0.0;

    // Varremos todos os estados
    for (int i = 0; i < states.size(); i++) {
      double oldValue = this->getStateValueByIndex(i);
      double max_value = -1e9;
      double best_action = actions.at(0);

      for (double action : actions) {
        double temp =
            actionValueFunction(states.at(i), action, discountRate,
                                this->getStateValues(), returns, states);
        std::cout << "Estado: " << states[i] << " | Acao: " << action
                  << " | Valor Temp: " << temp << std::endl;
        if (temp > max_value) {
          max_value = temp;
          best_action = action;
        }
      }
      // V(s) <- max_a...
      this->setStateValueByIndex(i, max_value);
      optimalPolicy[i] = best_action;
      // Atualiza o delta com a maior diferença encontrada NESTA varredura)
      delta =
          std::max(delta, std::abs(oldValue - this->getStateValueByIndex(i)));
    }
  }

  return optimalPolicy;
}
