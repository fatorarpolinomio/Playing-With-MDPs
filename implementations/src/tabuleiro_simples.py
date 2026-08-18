# import numpy as np
import numpy as np
from mdp_python.MDecisionProcess import PyDynamicProgramming
import python_version.value_iteration as vi
import python_version.trans_func as tf

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
    [0, 1 / 3, 1 / 3, 1 / 3,   0,     0],
    [0,   0,   1 / 3, 1 / 3, 1 / 3,   0],
    [0,   0,     0,   1 / 3, 1 / 3, 1 / 3],
    [0,   0,     0,     0,   2 / 3, 1 / 3],
    [0,   0,     0,   1 / 3, 1 / 3, 1 / 3],
    [0,   0,     0,     0,     0,     1],
]

transicao_dado2 = [
    [0, 1 / 2, 1 / 2,   0,     0,     0],
    [0,   0,   1 / 2, 1 / 2,   0,     0],
    [0,   0,     0,   1 / 2, 1 / 2,   0],
    [0,   0,     0,     0,   1 / 2, 1 / 2],
    [0,   0,     0,     0,   1 / 2, 1 / 2],
    [0,   0,     0,     0,     0,     1],
]

trans_func_per_action = [transicao_dado1, transicao_dado2]

recompensas_por_estado = [-1, -1, -1, -1, -1, 0]

discountRate = 1

politica_otima = vi.iterative_value_iteration(discountRate, 0.0001, acoes, estados, recompensas_por_estado, trans_func_per_action)

print("Printando versão iterativa")
print(politica_otima)

# print("Printando v2")
# politica_otima2 = vi.iterative_value_iteration_v2(discountRate, 0.0001, acoes, estados, recompensas_por_estado, trans_func_per_action)
# print(politica_otima2)

print("Printando exemplo pra debug:")

for number in [0, 1, 2, 3, 4, 5]:
    line = []
    for estado in estados:
        # print(f"Para o caso {number} -> {estado}")
        line.append(tf.transition_function(number, estado, 5, estados, d2))
    print(line)
