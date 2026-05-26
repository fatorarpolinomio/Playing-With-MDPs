from mdp_python.MDecisionProcess import PyDynamicProgramming

# Dados:
d1 = [1, 2, 3]
d2 = [1, 2]

estados = [1, 2, 3, 4, 5, 6]  # Dizem respeito às posições no tabuleiro
acoes = [1, 2]  # Dizem respeito às escolhas de dados
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

recompensas_por_estado = [-1, -1, -1, -1, -1, 0]

discountRate = 1


prog_dinamica = PyDynamicProgramming(0, discountRate, 7)

prog_dinamica.apply_value_iteration(
    discountRate, 0, 7, transicao_dado1, acoes, recompensas_por_estado, estados
)

print(prog_dinamica)
