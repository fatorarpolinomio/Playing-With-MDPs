import numpy as np


def iterative_value_iteration(
    discount_rate: float,
    threshold: float,
    actions: list,
    states: list,
    rewards: list,
    trans_func_per_action: list,
):

    # Vamos inicializar V(s) para todo estado pertencente
    # ao nosso conjunto de estados
    state_values = np.zeros(len(states))

    # Definindo lista de políticas ótimas para cada estado
    optimal_policy = np.zeros(len(states))
    # Definindo um Delta maior que Threshold,
    # para que ele consiga entrar no while
    delta = threshold + 1.0

    # Loop principal
    while delta > threshold:
        delta = 0.0
        for single_state in states:
            # Primeira atribuição dentro do loop
            old_value = state_values[single_state]  # v <- V(s)
            best_action = actions[0]
            # Para o próximo passo, vamos inicializar max_value
            max_value = -1e9
            # Vamos iterar por todas as ações para encontrar a ação
            # que maximiza o valor retornado pela Action Value Function
            for single_action in actions:
                temp = 0.0
                # Rodando a Action Value Function,
                # ao mesmo tempo que pegamos a ação que maximiza o
                # valor retornado
                for single_state_apostrophe in states:
                    matriz = trans_func_per_action[single_action]
                    trans_prob = matriz[int(single_state)][int(single_state_apostrophe)]
                    if trans_prob > 0:
                        expected_value = trans_prob * (
                            rewards[single_state_apostrophe]
                            + (discount_rate * state_values[single_state_apostrophe])
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
    print("Valores de Estado:", state_values)
    return optimal_policy


def vetorial_value_iteration(
    discount_rate: float,
    threshold: float,
    actions: list,
    states: list,
    rewards: list,
    trans_func_per_action: list,
):
    # Preparação dos Dados
    # P vira uma Matriz 3D no formato: (Ações, Estados Atuais, Estados Futuros)
    trans_func_per_action_numpy = np.array(trans_func_per_action)

    # Converte a nossa lista de recompensas para um array
    # da NumPy
    rewards_numpy = np.array(rewards)

    # Inicializando nossos state_values e optimal_policy do mesmo jeito
    state_values = np.zeros(len(states))
    optimal_policy = np.zeros(len(states))

    delta = threshold + 1.0

    # Loop principal de convergência
    while delta > threshold:
        delta = 0.0
        # EQUAÇÃO DE BELLMAN EM 2 LINHAS
        # Passo 1: Calcula o [ R(s') + gama * V(s') ] para todos os estados de uma vez
        v_target = rewards_numpy + (discount_rate * state_values)

        # Passo 2: O Somatório de Bellman!
        expected_value = trans_func_per_action_numpy @ v_target

        # --- EXTRAINDO A POLÍTICA E OS VALORES ---

        # Pega a "nota" da melhor ação para cada estado (axis=0 olha pelas linhas/ações)
        new_V = np.max(expected_value, axis=0)

        # Pega o "índice" (o número) da melhor ação para cada estado
        optimal_policy = np.argmax(expected_value, axis=0)

        # Atualiza o delta checando a maior diferença de V(s) do tabuleiro inteiro
        delta = np.max(np.abs(new_V - state_values))

        # Salva as notas para o próximo loop
        state_values = new_V

    print(f"Valores dos Estados V(s):\n{state_values}")
    return optimal_policy
