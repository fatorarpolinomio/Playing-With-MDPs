import mdp_algorithms as mdp
import numpy as np

# Função geradora de trabalhos "aleatórios", com diferentes probabilidades
# Input: quantidade de trabalhos a serem incluídos na coleção
# Output: lista preenchida com a quantidade de trabalhos requerida
def work_collection_generator(work_qnt: int):
    rng = np.random.default_rng()
    count = work_qnt
    work_collection = []
    prob_qnt_list = []
    while count:
        count -= 1

        # Sortear números -> Normalizar
        # Sorteando números que funcionarão como probs
        work_prob = rng.uniform(1, 10)
        # Adicionando em uma lista para normalizar depois
        prob_qnt_list.append(work_prob)

        # Definindo nova lista "trabalho"
        new_work = [rng.uniform(1, 5), rng.uniform(1, 5) , work_prob]
        # new_work[0] = custo
        # new_work[1] = recompensa
        # new_work[2] = se estou fazendo este trabalho, a chance dele ser concluído (geométrica)

        work_collection.append(new_work)

    # Normalizando probs (soma total fica 1)
    total = sum(prob_qnt_list)
    for work in work_collection:
        work[2] = float(work[2] / total)

    return work_collection

# Função que cria um conjunto de estados com base numa lista de trabalhos pré-existente
# Input: lista de trabalhos
# Output: coleção de estados baseados nos trabalhos pré-existentes
def state_collection_creator(work_collection: list, max_reward: int):

    state_collection = []
    available_works = [] # Meramente ilustrativo (?)

    # Gera todas as possíveis combinações de trabalhos com recompensas
    for work in work_collection:
        for reward in range(max_reward + 1):
            state_collection.append([work, available_works, reward])
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

works = work_collection_generator(5)
states = state_collection_creator(works, 5)
print("Todos os trabalhos:")
for work in works:
    print(work)
available_works = update_list(works, [])
print("Trabalhos disponíveis:")
print(available_works)
