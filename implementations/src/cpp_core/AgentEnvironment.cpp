#include "MDecisionProcess.hpp"
#include <cmath>

// Isso aqui é para calcular o Gt
double AgentEnvironment::calculateReturn(double discountRate,
                                         double rewardReturn,
                                         std::vector<double> returns) {
  this->rewardReturn = 0;
  double tempDiscount = discountRate;
  for (int i = 0; i < returns.size(); i++) {
    tempDiscount = pow(discountRate, i);
    this->rewardReturn += tempDiscount * returns[i];
  }
  return rewardReturn;
}

// Método da interface pública, apenas para aplicar o método
void AgentEnvironment::applyCalculateReturn(double discountRate,
                                            double rewardReturn,
                                            std::vector<double> returns) {
  this->setRewardReturn(calculateReturn(discountRate, rewardReturn, returns));
}
