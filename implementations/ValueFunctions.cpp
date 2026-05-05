#include "Eigen/Core"
#include "MDPs.hpp"
#include <Eigen/Dense>
#include <cmath>
#include <iostream>
#include <random>
#include <vector>

ValueFunctions::ValueFunctions(double rewardValue, double discountRate) {
  this->rewardValue = rewardValue;
  this->discountRate = discountRate;
}

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

double ValueFunctions::calculatePolicyProb(double action, double state) {
  return 0.0;
}

double ValueFunctions::calculateTransFunc(double actions, double returns,
                                          double states) {
  return 0.0;
}

double ValueFunctions::bellmanEquation(double state, double discountRate,
                                       double rewardValue,
                                       std::vector<double> currentValues,
                                       std::vector<double> actions,
                                       std::vector<double> returns,
                                       std::vector<double> states) {
  double finalValue = 0;

  for (int i = 0; i < actions.size(); i++) {
    finalValue += calculatePolicyProb(actions[i], state);
    for (int j = 0; j < states.size(); j++) {
      for (int k = 0; k < returns.size(); k++) {
        finalValue +=
            calculateTransFunc(actions[i], returns[k], states[j]) * returns[k];
        finalValue += calculateTransFunc(actions[i], returns[k], states[j]) *
                      discountRate * currentValues[j];
      }
    }
  }

  return finalValue;
}
void ValueFunctions::applyCalculateReturn(double discountRate,
                                          double rewardReturn,
                                          std::vector<double> returns) {
  this->rewardReturn = calculateReturn(discountRate, rewardReturn, returns);
}

void ValueFunctions::applyBellmanEquation(double discountRate,
                                          double rewardReturn,
                                          std::vector<double> returns,
                                          std::vector<double> states,
                                          std::vector<double> actions) {}
