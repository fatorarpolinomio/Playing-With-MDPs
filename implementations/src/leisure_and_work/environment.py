import modelling as aux
import random

class LW_Environment:
    def __init__ (self, current_work : list, available_works: list, reward: int):
        # Estado inicial: trabalho nulo, nenhum disponível, nenhuma recompensa acumulada
        self.state = [[0, 0, 0, 0], [], 0]
        self.goal = [current_work, available_works, reward]
        self.works = aux.work_collection_generator(2)
        self.states = aux.state_collection_creator(self.works, 2)
        self.actions = self.state[1] # As ações partem do estado atual do agente A(s)

    # Volta para o estado inicial
    def reset(self):
        self.state = [[0, 0, 0, 0], [], 0]

    def chooseWork(self, state : list, actions: list):
        pass

    def nextState(self, state, action):

        current_work = self.state[0]
        score = self.state[2]

        # Terminando (ou não) o trabalho
        current_work, score_result = aux.finish_work(current_work)
        score = score + score_result

        # Definindo forma dos trabalhos disponíveis
        available_actions = self.actions
        # Trabalho(s) aparecendo
        available_actions = aux.add_in_available_list(self.works, available_actions)
        # Trabalho(s) sumindo
        available_actions = aux.remove_from_available_list(available_actions)

        if current_work == [0, 0, 0, 0]:
            chooseWork()

        # Encontrando novo estado equivalente ao atual
        for other_state in self.states:
            if current_work == other_state[0] and available_actions == other_state[1] and self.state[2] == other_state[2]:
                self.state = other_state

        return self.state

    def reward(self, state, action):
        if state == self.goal:
            return 0
        else:
            return -1

    def simulateStep(self,state,action):
        r = self.reward(state, action)
        nextStates = self.nextState(state,action)
        return random.choices( list( nextStates.keys() ), weights = list( nextStates.values() ), k=1 )[0], r

    def step(self, action):
        self.state, r = self.simulateStep(self.state, action)
        return self.state, r
