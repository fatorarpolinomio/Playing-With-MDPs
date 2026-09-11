import algorithms
import numpy as np

def work_generator():
    rng = np.random.default_rng()
    reward = rng.uniform(1, 5)
    wear = rng.uniform(1, 5)
    work = [reward, wear]
    return work


print(work_generator())
actions = [0, 1] # Negar ou aceitar um trabalho
