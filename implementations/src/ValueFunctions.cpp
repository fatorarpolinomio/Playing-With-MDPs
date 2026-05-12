#include "Eigen/Core"
#include "MDPs.hpp"
#include <Eigen/Dense>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>

// Este construtor provavelmente será alterado
ValueFunctions::ValueFunctions(double rewardValue, double discountRate) {
  this->rewardValue = rewardValue;
  this->discountRate = discountRate;
}

// Isso aqui é para calcular o Gt
double ValueFunctions::calculateReturn(double discountRate, double rewardReturn,
                                       std::vector<double> returns) {
  this->rewardReturn = 0;
  double tempDiscount = discountRate;
  for (int i = 0; i < returns.size(); i++) {
    tempDiscount = pow(discountRate, i);
    this->rewardReturn += tempDiscount * returns[i];
  }
  return rewardReturn;
}

// Essa aqui mudará para cada problema
double ValueFunctions::calculatePolicyProb(double action, double state) {
  return 0.0;
}

// Essa aqui vai mudar para cada problema que estaremos modelando
// Dependendo da situação, já teremos tudo tabelado na forma de uma matriz
// Para cenários onde teremos um grande quantidade de probalidades,
// teremos que "automatizar" na forma de um algoritmo
double ValueFunctions::calculateTransFunc(double actions, double returns,
                                          double states) {
  return 0.0;
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
    double policyProb = calculatePolicyProb(actions[i], state);
    double actionExpectedValue = 0;
    // Loop duplo: representa o somatório dado para todos os outros
    // estados e todas as recompensas
    for (int j = 0; j < states.size(); j++) {
      for (int k = 0; k < returns.size(); k++) {

        double transProb =
            calculateTransFunc(actions[i], returns[k], states[j]);
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

// TODO: implementar isso aqui e alterar nos algoritmos de
//  programação dinâmica
double ValueFunctions::actionValueFunction(double state, double action,
                                           std::vector<double> currentValues,
                                           std::vector<double> actions,
                                           std::vector<double> returns,
                                           std::vector<double> states) {
  return 0.0;
}

// Método da interface pública, apenas para aplicar o método
void ValueFunctions::applyCalculateReturn(double discountRate,
                                          double rewardReturn,
                                          std::vector<double> returns) {
  this->rewardReturn = calculateReturn(discountRate, rewardReturn, returns);
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
