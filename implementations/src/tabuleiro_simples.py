# import numpy as np
import numpy as np
from mdp_python.MDecisionProcess import PyDynamicProgramming

# Dados:
d1 = [1, 2, 3]
d2 = [1, 2]

estados = [0, 1, 2, 3, 4, 5]  # Dizem respeito às posições no tabuleiro
acoes = [0, 1]  # Dizem respeito às escolhas de dados

# Objetivo: partindo da 1, chegar na posição 6 o mais rápido possível

# MDP - Função de transição - p: S x R x R x A -> [0, 1]
# Linha = posição atual no tabuleiro
# Coluna = probabilidade de cair naquela posição jogando o dado
transicao_dado1 = [
    [0, 1 / 3, 1 / 3, 1 / 3, 0, 0],
    [0, 0, 1 / 3, 1 / 3, 1 / 3, 0],
    [0, 0, 0, 1 / 3, 1 / 3, 1 / 3],
    [0, 0, 0, 0, 2 / 3, 1 / 3],
    [0, 0, 0, 1 / 3, 1 / 3, 1 / 3],
    [0, 0, 0, 0, 0, 1],
]

transicao_dado2 = [
    [0, 1 / 2, 1 / 2, 0, 0, 0],
    [0, 0, 1 / 2, 1 / 2, 0, 0],
    [0, 0, 0, 1 / 2, 1 / 2, 0],
    [0, 0, 0, 0, 1 / 2, 1 / 2],
    [0, 0, 0, 0, 1 / 2, 1 / 2],
    [0, 0, 0, 0, 0, 1],
]

trans_func_per_action = [transicao_dado1, transicao_dado2]

recompensas_por_estado = [-1, -1, -1, -1, -1, 0]

discountRate = 1


prog_dinamica = PyDynamicProgramming(0, discountRate, 7)
print("Injetando valores zerados...")
prog_dinamica.set_state_values([0.0] * len(estados))

print("Enviando Matriz de Transição...")
prog_dinamica.set_trans_func_per_action(trans_func_per_action)

print("Iniciando Value Iteration (O C++ vai assumir o controle)...")
print("--- INVESTIGAÇÃO DO VETOR DE TAMANHO 2 ---")
print("Ações cadastradas:", acoes)
print("Qtd de Matrizes de Ação:", len(trans_func_per_action))
print("Estados cadastrados:", estados)
print("Qtd de Recompensas:", len(recompensas_por_estado))
print("------------------------------------------")
politica = prog_dinamica.apply_value_iteration(
    discountRate, 0, 0.0001, acoes, recompensas_por_estado, estados
)

print("Valores dos Estados V(s):", prog_dinamica.get_state_values())

print("Política extraída:", politica)


def value_iteration(discount_rate: float, threshold: float, actions : list, states: list, rewards : list, trans_func_per_action : list):

    # Vamos inicializar V(s) para todo estado pertencente
    # ao nosso conjunto de estados
    state_values = np.zeros(len(states))

    # Definindo um Delta maior que Threshold,
    # para que ele consiga entrar no while
    delta = threshold + 1.0

    # Loop principal
    while delta > threshold:
        delta = 0.0
        for single_state in states:
            # Primeira atribuição dentro do loop
            old_value = state_values[single_state]  # v <- V(s)

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
                    for single_reward in rewards:
                        matriz = trans_func_per_action[single_action]
                        trans_prob = matriz[single_state, single_state_apostrophe]
                        expected_value = trans_prob * (rewards[single_state_apostrophe] + (discount_rate * state_values[single_state_apostrophe]))
                        temp = expected_value
                # Atualizando max_value, se necessário
                if temp > max_value:
                    max_value = temp
            # Atualizando a lista com maior valor
            state_values[single_state] = max_value
            # Pegando o maior valor entre os dois
            delta = max(delta, abs(old_value - state_values[single_state]))

    optimal_policy = np.zeros(len(states))

    for single_state in states:
        max_value = -1e9
        best_action = actions[0]

        for single_action in actions:
            temp =
