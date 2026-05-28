#include "MDecisionProcess.hpp"
#include <Eigen/Dense>
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

double AgentEnvironment::calculatePolicyProb(double action, double state) {
  return 0.0;
}

// A tabela das probabilidades de transição muda com base nas ações. Se eu
// escolher tomar uma ação, uma tabela específica para aquela ação deverá ser
// usada para recuperar a probabilidade de transição correspondente ao estado
// atual e ao estado de destino. Portanto, é necessário passar como argumento um
// array de matrizes. Cada índice do array corresponde a uma ação, e cada matriz
// contém as probabilidades de transição para cada par de estados (startState,
// state).
double AgentEnvironment::calculateTransFunc(
    double action, double startState, double returns, double states,
    std::vector<Eigen::MatrixXd> &transFuncPerAction) {
  // Convertemos os 'doubles' para índices inteiros válidos
  size_t indiceAcao = static_cast<size_t>(action);
  size_t linhaOrigem = static_cast<size_t>(startState);
  size_t colunaDestino = static_cast<size_t>(states);

  // O .at() vai travar se a Ação não existir na lista de matrizes
  auto &matriz = transFuncPerAction.at(indiceAcao);

  // Trava de segurança manual para o Eigen (já que o NDEBUG está ativado)
  if (linhaOrigem >= matriz.rows() || colunaDestino >= matriz.cols()) {
    std::string erro =
        "ERRO EIGEN: Tentou acessar Linha " + std::to_string(linhaOrigem) +
        ", Coluna " + std::to_string(colunaDestino) + ". Mas a matriz eh " +
        std::to_string(matriz.rows()) + "x" + std::to_string(matriz.cols());
    throw std::out_of_range(erro);
  }
  // Acessando e retornando a probabilidade de transição correspondente
  return matriz(linhaOrigem, colunaDestino);
}

// Método da interface pública, apenas para aplicar o método
void AgentEnvironment::applyCalculateReturn(double discountRate,
                                            double rewardReturn,
                                            std::vector<double> returns) {
  this->setRewardReturn(calculateReturn(discountRate, rewardReturn, returns));
}

double AgentEnvironment::applyCalculatePolicyProb(double action, double state) {
  return applyCalculatePolicyProb(action, state);
}
double AgentEnvironment::applyCalculateTransFunc(double action,
                                                 double startState,
                                                 double returns,
                                                 double states) {
  return calculateTransFunc(action, startState, returns, states,
                            transFuncPerAction);
}

// Esta função será importante para fazer a interface com o python
// como o cython não lida muito bem com o Eigen, damos uma volta e passamos o
// array de matrizes na forma de lista de listas de listas (3D)
// Ela funcionará como getter para a transFuncPerAction
std::vector<std::vector<std::vector<double>>>
AgentEnvironment::getTransFuncAsVectors() {
  std::vector<std::vector<std::vector<double>>> resultado;

  for (const auto &matriz : transFuncPerAction) {
    std::vector<std::vector<double>> matriz_vector(
        matriz.rows(), std::vector<double>(matriz.cols()));
    for (int i = 0; i < matriz.rows(); ++i) {
      for (int j = 0; j < matriz.cols(); ++j) {
        matriz_vector[i][j] = matriz(i, j);
      }
    }
    resultado.push_back(matriz_vector);
  }
  return resultado;
}

// Esta função será importante para fazer a interface com o python
// como o cython não lida muito bem com o Eigen, damos uma volta e passamos o
// array de matrizes na forma de lista de listas de listas (3D)
// Ela funcionará como setter para a transFuncPerAction
void AgentEnvironment::setTransFuncFromVectors(
    const std::vector<std::vector<std::vector<double>>> &matrizes3D) {
  this->transFuncPerAction.clear(); // Limpa a memória anterior

  // Varre cada "ação" (cada matriz)
  for (size_t a = 0; a < matrizes3D.size(); ++a) {
    size_t linhas = matrizes3D[a].size();
    size_t colunas = matrizes3D[a][0].size();

    // Cria a matriz Eigen
    Eigen::MatrixXd matriz(linhas, colunas);

    // Preenche os valores
    for (size_t i = 0; i < linhas; ++i) {
      for (size_t j = 0; j < colunas; ++j) {
        matriz(i, j) = matrizes3D[a][i][j];
      }
    }
    this->transFuncPerAction.push_back(matriz);
  }
}
