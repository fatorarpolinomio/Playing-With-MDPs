import numpy as np

def transition_function():
    pass

def action_value_function(
    discount_rate: float,
    threshold: float,
    action: int,
    states: list,
    rewards: list,
    temp: float
):
    pass


# Algoritmo adaptado da versão do livro Reinforcement Learning
def value_iteration(
    discount_rate: float,
    threshold: float,
    actions: list[int],
    states: list,
    rewards: list
):
    # Vamos inicializar V(s) para todo estado
    # pertencente ao conjunto de estados

    state_values = np.zeros(len(states))

    # Lista de políticas ótimas para cada estado
    optimal_policy = np.zeros(len(states))

    # Definindo um Delta maior que Threshold,
    # para ele conseguir entrar no while
    delta = threshold + 1.0

    # Loop principal
    while delta > threshold:
        delta = 0.0

        for single_state in states:
            # v <- V(s)
            old_value = state_values[single_state]
            best_action = actions[0]
            max_value = -1e9

            # Vamos iterar por todas as ações para encontrar a ação
            # que maximiza o valor retornado pela Action Value Function
            for single_action in actions:
                temp = 0.0
                # Rodando a Action Value Function,
                # ao mesmo tempo que pegamos a ação que maximiza o
                # valor retornado
                # for single_state_aps in states:
                for single_state_aps in states:
                    trans_prob = transition_function() # haverão argumentos em breve

                    expected_value = trans_prob * (
                        rewards[single_state_aps]
                        + (discount_rate * state_values[single_state_aps])
                    )
                    temp += expected_value
                # Atualizando max_value e best_action, se necessário
                if temp > max_value:
                    max_value = temp
                    best_action = single_action
            # Atualizando a política ótima
            optimal_policy[single_state] = best_action
            # Atualizando a lista com maior valor
            state_values[single_state] = max_value
            # Pegando o maior valor entre os dois
            delta = max(delta, abs(old_value - state_values[single_state]))
    return optimal_policy
