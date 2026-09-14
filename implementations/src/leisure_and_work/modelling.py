import mdp_algorithms as mdp
import numpy as np


# Função geradora de trabalhos "aleatórios", com diferentes probabilidades
# Input: quantidade de trabalhos a serem incluídos na coleção
# Output: lista preenchida com a quantidade de trabalhos requerida
def work_collection_generator(work_qnt: int):
    rng = np.random.default_rng()
    count = work_qnt
    work_collection = []
    prob_qnt = 1
    while count:
        count -= 1

        # Primeiro um valor é sorteado
        # O valor sorteado deve ser subtraído da quantidade de probabilidade restante
        # O próximo valor deve ser sorteado entre 0 e a nova quantidade de probabilidade restante
        # se estivermos na última iteração, quantidade de prob deve ser o que sobrou
        if count == 0:
            work_prob = prob_qnt
        else:
            work_prob = rng.uniform(0, prob_qnt)
            prob_qnt = prob_qnt - work_prob

        # Definindo nova tupla "trabalho", a recompensa será um valor de uniforme entre 1 e 5
        new_work = (rng.uniform(1, 5),"" , work_prob) # Falta lembrar o que a segunda posição significa
        work_collection.append(new_work) # Adicionando na coleção de trabalhos

    return work_collection

# Função que cria um conjunto de estados com base numa lista de trabalhos pré-existente
# Input: lista de trabalhos
# Output: coleção de estados baseados nos trabalhos pré-existentes
def state_collection_creator(work_collection: list):

    state_collection = []

    for work in work_collection:
        new_state = (work, "") # Falta lembrar o que a segunda posição significa
        state_collection.append(new_state)

    return state_collection

# Função para sortear trabalho
# Input: lista de trabalhos
# Output: Um dos trabalhos da lista de input, definido "aleatoriamente"
def work_radomizer(works: list):
    rng = np.random.default_rng()
    weights = [] # Lista de pesos de cada trabalho
    for work in works:
        weights.append(work[2]) # Adicionando pesos na lista
    random_work = rng.choice(works, p = weights) # Sorteando trabalho com base em peso
    return random_work

w1 = (4, "r1", 0.2)
w2 = (3, "r2", 0.3)
w3 = (2, "r3", 0.5)

work_collection = [w1, w2, w3]

actions = [0, 1] # Negar ou aceitar um trabalho
