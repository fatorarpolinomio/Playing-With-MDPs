#include "MDPs.hpp"
#include <algorithm>
#include <cmath>
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

// TODO: Ajeitar a parte da equação de Bellman (Pergunta: qual a diferença?)
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
      double bestActionValue = -1e9; // Começa com um valor bem baixo
      double bestAction = actions[0];

      // Simulamos cada ação possível para ver qual é a melhor
      for (double action : actions) {
        double expectedActionValue = 0;

        // Calcula a soma (probabilidade * (recompensa + desconto *
        // valor_futuro))
        for (int j = 0; j < states.size(); j++) {
          for (int k = 0; k < returns.size(); k++) {
            double transProb =
                calculateTransFunc(action, returns[k], states[j]);
            expectedActionValue +=
                transProb * (returns[k] + discountRate * currentValues[j]);
          }
        }

        // Faz o papel do argmax: guarda a ação que deu o maior resultado
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

// TODO: Ajeitar a parte da equação de Bellman
// Eu sem entender nada
void DynamicProgramming::ValueIteration(double discountRate, double rewardValue,
                                        double threshold,
                                        std::vector<double> &currentValues,
                                        std::vector<double> actions,
                                        std::vector<double> returns,
                                        std::vector<double> states) {
  // Inicializa maior que o threshold para entrar no while
  double delta = threshold + 1.0;
  // Encontra o maior valor de "a", que será usado como parâmetro
  auto maxAction = std::max_element(actions.begin(), actions.end());

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
