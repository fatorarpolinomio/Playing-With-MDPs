
#include "MDecisionProcess.hpp"

#include <vector>

// Este construtor provavelmente será alterado
ValueFunctions::ValueFunctions(double rewardValue, double discountRate) {
  this->rewardValue = rewardValue;
  this->setDiscountRate(discountRate);
}

// Equação de Bellman para a função de valor.
// Ela expressa a relação entre o valor de um estado e os valores dos estados
// sucessivos
double ValueFunctions::bellmanEquation(double state, double discountRate,
                                       double rewardValue,
                                       std::vector<double> currentValues,
                                       std::vector<double> actions,
                                       std::vector<double> returns,
                                       std::vector<double> states) {
  double finalValue = 0;

  // Primeiro Loop: somatório da probabilidade de tomar a ação "i"
  // no estado "state" sob uma política em específico
  for (int i = 0; i < actions.size(); i++) {
    double policyProb = applyCalculatePolicyProb(actions[i], state);
    double actionExpectedValue = 0;
    // Loop duplo: representa o somatório dado para todos os outros
    // estados e todas as recompensas
    for (int j = 0; j < states.size(); j++) {
      for (int k = 0; k < returns.size(); k++) {

        double transProb =
            applyCalculateTransFunc(actions[i], state, returns[k], states[j]);
        // Para ficar mais palatável, decidi "distribuir" a calculateTransFunc()
        // para os membros dos colchetes da equação
        actionExpectedValue += transProb * returns[k];

        // Aqui, para evitar a chamada recursiva, consultaremos uma tabela
        // de valores
        actionExpectedValue += transProb * discountRate * currentValues[j];
      }
    }
    finalValue += policyProb * actionExpectedValue;
  }
  return finalValue;
}

// Equação de Valor de Ação (Q-Value)
// "Qual o retorno esperado se eu tomar a ação 'action' no estado 'state'?"
double ValueFunctions::actionValueFunction(
    double state, double action, double discountRate,
    const std::vector<double> &currentValues,
    const std::vector<double> &returns, const std::vector<double> &states) {

  double expectedValue = 0;

  // Um único loop: Varremos os estados futuros (s')
  for (int j = 0; j < states.size(); j++) {

    // Qual a chance de ir do 'state' para o estado futuro 'j' usando a
    // 'action'?
    double transProb = applyCalculateTransFunc(action, state, 0, states.at(j));

    // O agente ganha a recompensa do estado futuro + o valor descontado dele
    expectedValue +=
        transProb * (returns.at(j) + (discountRate * currentValues.at(j)));
  }

  return expectedValue;
}

// Método da interface pública, apenas para aplicar a equação
double ValueFunctions::applyBellmanEquation(double state, double discountRate,
                                            double rewardValue,
                                            std::vector<double> currentValues,
                                            std::vector<double> actions,
                                            std::vector<double> returns,
                                            std::vector<double> states) {
  return ValueFunctions::bellmanEquation(state, discountRate, rewardValue,
                                         currentValues, actions, returns,
                                         states);
}
