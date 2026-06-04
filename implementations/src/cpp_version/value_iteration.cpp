#include <Eigen/Dense>
#include <cmath>
#include <vector>

std::vector<double> iterative_value_iteration(
    double discount_rate, double threshold, std::vector<double> actions,
    std::vector<double> rewards, std::vector<double> states,
    std::vector<std::vector<std::vector<double>>> trans_func_per_action) {

  // Inicializa vetor para guardar a pontuação de cada estado
  std::vector<double> state_values(states.size(), 0.0);

  // Inicializa vetor para guardar a política ótima para cada estado
  std::vector<double> optimal_policy(states.size(), 0.0);

  // Inicializa o delta com valor maior que o threshold para ele entrar no while
  double delta = threshold + 1.0;

  // Loop principal
  while (delta > threshold) {

    // Valor inicial correto para o delta
    delta = 0.0;

    // Iterando para cada estado
    for (int i = 0; i < states.size(); i++) {

      // Salvando pontuação "antiga"
      double oldValue = state_values[i];

      // Inicializando com valor bem pequeno
      double max_value = -1e9;

      // Inicializando a partir do primeiro estado
      double best_action = actions.at(0);

      // Vamos iterar por todas as ações para encontrar aquela
      // que maximiza o valor retornado pela Action Value Function
      for (int j = 0; j < actions.size(); j++) {

        double temp = 0.0;

        // Rodando a Action Value Function,
        // ao mesmo tempo que pegamos a ação que maximiza o
        // valor retornado
        for (int k = 0; k < states.size(); k++) {
          auto matrix = trans_func_per_action[actions[j]];
          auto trans_prob = matrix[i][k];
          if (trans_prob > 0) {
            auto expected_value =
                trans_prob * (rewards[k] + (discount_rate * state_values[k]));
            temp += expected_value;
          }
        }

        // Atualizando max_value e best_action, se necessário
        if (temp > max_value) {
          max_value = temp;
          best_action = actions[j];
        }
      }
      // Atualizando a política ótima para o estado em questão
      optimal_policy[i] = best_action;

      // Atualizando a pontuação do estado
      state_values[i] = max_value;

      // Pegando o maior valor entre delta e o módulo do valor anterior menos o
      // atual
      delta = std::max(delta, std::abs(oldValue - state_values[i]));
    }
  }

  return optimal_policy;
}

std::vector<double> vetorial_value_iteration(
    double discount_rate, double threshold, std::vector<double> actions,
    std::vector<double> states, std::vector<double> rewards,
    std::vector<std::vector<std::vector<double>>> trans_func_per_action) {

  // Inicializa vetor para guardar a pontuação de cada estado
  Eigen::VectorXd state_values = Eigen::VectorXd::Zero(states.size());

  // Inicializa vetor para guardar a política ótima para cada estado
  Eigen::VectorXd optimal_policy = Eigen::VectorXd::Zero(states.size());

  double delta = threshold + 1.0;
}
