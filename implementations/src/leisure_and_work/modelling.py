import mdp_algorithms as mdp
import numpy as np
import itertools

# Função que normaliza números para que fiquem entre 0 e 1
# Input: lista com números
# Output: lista com números normalizados
def prob_normalizer(prob_qnt_list : list):
    total = sum(prob_qnt_list)
    for index in range(len(prob_qnt_list)):
        prob_qnt_list[index] = float(prob_qnt_list[index] / total)
    return prob_qnt_list

# Função que gera todos os subconjuntos a partir de uma lista
# Input: lista com um conjunto de elementos
# Output: lista com todos os subconjuntos da lista
def subconj_generator(lista):
    subconjuntos = []
    # Itera sobre todos os tamanhos possíveis, de 0 até o tamanho da lista
    for r in range(len(lista) + 1):
        # Gera combinações de tamanho 'r' e converte em listas
        combinacoes = itertools.combinations(lista, r)
        subconjuntos.extend([list(c) for c in combinacoes])
    return subconjuntos

# Função geradora de trabalhos "aleatórios", com diferentes probabilidades
# Input: quantidade de trabalhos a serem incluídos na coleção
# Output: lista preenchida com a quantidade de trabalhos requerida
def work_collection_generator(work_qnt: int):
    rng = np.random.default_rng()
    count = work_qnt
    work_collection = [[0, 0, 0, 0]] # Inicializando com o trabalho nulo
    prob_finish_list = [] # Lista de chances de finalizar cada trabalho
    prob_showup_list = [] # Lista de chances dos trabalhos aparecerem
    prob_disappear_list = [] # Lista de chances dos trabalhos sumirem

    for count in range(work_qnt):

        # Sortear números -> Normalizar
        finish_prob = rng.uniform(1, 10)
        showup_prob = rng.uniform(1, 10)
        disappear_prob = rng.uniform(1, 10)

        # Adicionando em listas para normalizar depois
        prob_finish_list.append(finish_prob)
        prob_showup_list.append(showup_prob)
        prob_disappear_list.append(disappear_prob)

        # Definindo nova lista "trabalho"
        # new_work[0] = custo
        # new_work[1] = recompensa
        # new_work[2] = se estou fazendo este trabalho, a chance dele ser concluído (geométrica)
        # new_work[3] = chance do trabalho aparecer
        # new_work[4] = chance do trabalho sumir
        new_work = [int(rng.uniform(1, 3)),
            int(rng.uniform(1, 3)),
            finish_prob,
            showup_prob,
            disappear_prob
        ]

        work_collection.append(new_work)

    prob_finish_list = prob_normalizer(prob_finish_list)
    prob_showup_list = prob_normalizer(prob_showup_list)
    prob_disappear_list = prob_normalizer(prob_disappear_list)

    for work_number in range(work_qnt):
        work = work_collection[work_number + 1]
        work[2] = prob_finish_list[work_number]
        work[3] = prob_showup_list[work_number]
        work[4] = prob_disappear_list[work_number]


    return work_collection

# Função que cria um conjunto de estados com base numa lista de trabalhos pré-existente
# Input: lista de trabalhos)work_prob
# Output: coleção de estados baseados nos trabalhos pré-existentes
def state_collection_creator(work_collection: list, max_reward: int):

    state_collection = []
    works_subconj = subconj_generator(work_collection)

    for work in work_collection:
        new_state = []
        new_state.append(work)

        for subconj in works_subconj:
            available_works = []
            if [0, 0, 0, 0] in subconj:
                available_works.append(subconj)
            if [0, 0, 0, 0] not in subconj:
                available_works = [[0, 0, 0, 0]] # O trabalho sempre estará disponível
                available_works.append(subconj)
            new_state.append(available_works)

            for reward in range(max_reward):
                new_state.append(max_reward)
        state_collection.append(new_state)

    return state_collection

# Função para sortear trabalho(s) e adicionar na lista de trabalhos disponíveis
# Input: conjunto de possíveis trabalhos + lista de trabalhos disponíveis
# Output: lista de trabalhos disponíveis atualizada
def update_available_list(works: list, available_works: list):
    rng = np.random.default_rng()
    work_qnt = int(rng.uniform(0, 4))
    if work_qnt > 0:
        for work in range(work_qnt):
            available_works.append(rng.choice(works))

    return available_works


actions = [0, 1] # Negar ou aceitar um trabalho


works = work_collection_generator(2)
print("LISTA DE TRABALHOS:")
for work in works:
    print(work)

states = state_collection_creator(works, 2)

print("LISTA DE ESTADOS - MÁXIMO DE PONTUAÇÃO = 2")
for state in states:
    print("------------")
    print("Trabalho atual: ", state[0])
    print("Trabalhos disponíveis: ", state[1])
    print("Pontuação acumulada: ", state[2])
