import algorithms
import numpy as np


# Protótipo de uma função geradora "aleatória"
def collection_generator(work_qnt: int):
    rng = np.random.default_rng()
    count = work_qnt
    work_collection = []
    ceiling = 1
    while count:

        # Tudo bugado aqui
        # ----------
        if count == 0:
            work_prob = 1 - ceiling
        else:
            work_prob = rng.uniform(0, ceiling)
            ceiling = work_prob
        # ----------

        new_work = (rng.uniform(1, 5),"" , work_prob)
        work_collection.append(new_work)
        count -= 1

    return work_collection

# Função para sortear trabalho
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

print(collection_generator(2))


actions = [0, 1] # Negar ou aceitar um trabalho
