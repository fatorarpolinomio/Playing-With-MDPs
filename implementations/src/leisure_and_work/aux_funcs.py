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

    # Fase de higiene
    subconjuntos.remove([]) # Retirando o conjunto vazio
    remover_do_subconj = []
    for sc in subconjuntos:
        if [0, 0, 0, 0] not in sc:
            remover_do_subconj.append(sc) # Salvar em uma lista pra não ter problema com loop
    for elemento in remover_do_subconj:
        subconjuntos.remove(elemento)

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
# Input: lista de trabalhos e o teto de recompensa
# Output: coleção de estados baseados nos trabalhos pré-existentes
def state_collection_creator(work_collection: list):

    state_collection = []
    works_subconj = subconj_generator(work_collection)

    for current_work in work_collection:
        for subconj in works_subconj:
            available_works = []

            for work in subconj:
                available_works.append(work)

            new_state = [current_work, available_works]
            state_collection.append(new_state)

    return state_collection

# Função para sortear trabalho(s) e adicionar na lista de trabalhos disponíveis
# Input: conjunto de possíveis trabalhos + lista de trabalhos disponíveis
# Output: lista de trabalhos disponíveis atualizada
def add_in_available_list(work_collection: list, available_works: list):

    probs = np.array([work[3] for work in work_collection], dtype=float)

    # Realiza o sorteio
    binomial_results = np.random.binomial(n=1, p=probs)
    mask = binomial_results.astype(bool)

    final_result = [work for work, selecionado in zip(work_collection, mask) if selecionado]

    for work in final_result:
        if work not in available_works:
            available_works.append(work)

    return available_works

# Função para sortear se cada trabalho da lista sairá da lista
# Input: lista de trabalhos disponíveis
# Output: lista de trabalhos disponíveis atualizada
def remove_from_available_list(available_works : list):

    if not available_works:
        return []

    probs = np.array([work[4] for work in available_works], dtype=float)

    # Realiza o sorteio
    binomial_results = np.random.binomial(n=1, p=probs)
    mask = binomial_results.astype(bool)

    # O operador [:] substitui os elementos da lista original "in-place"
    # Mantemos apenas os trabalhos onde 'remover' é False
    available_works[:] = [work for work, remover in zip(available_works, mask) if not remover]

    return available_works

def finish_work(trabalho: list):
    # O índice 2 contém a chance geométrica de conclusão
    prob_conclusao = trabalho[2]

    # Sorteia se o trabalho foi concluído (1) ou não (0)
    resultado_sorteio = np.random.binomial(n=1, p=prob_conclusao)

    if resultado_sorteio == 1:
        # Trabalho finalizado: retorna a lista zerada e a recompensa (índice 1)
        return [0, 0, 0, 0], trabalho[1]

    # Caso não seja concluído, o estado do trabalho se mantém e a recompensa é 0
    return trabalho, 0
