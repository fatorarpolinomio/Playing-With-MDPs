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
