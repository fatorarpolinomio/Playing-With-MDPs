import aux_funcs as aux
import random

class LW_Environment:
    def __init__ (self, current_work : list, available_works: list, reward: int, n_works: int = 2, max_reward: int = None):
        self.goal = [current_work, available_works, reward]
        self.max_reward = reward if max_reward is None else max_reward # Teto da pontuação (espaço de estados)
        self.works = aux.work_collection_generator(n_works)
        self.states = aux.state_collection_creator(self.works, self.max_reward)
        self.policy = None # Opcional: função (state, actions) -> trabalho, usada por chooseWork
        self.reset()

    # Volta para o estado inicial
    # Estado inicial: trabalho nulo, nenhum disponível, nenhuma recompensa acumulada
    def reset(self):
        self.last_events = [] # Eventos do último passo (informativo, usado pela GUI)
        self.state = self.equivalentState([0, 0, 0, 0], [], 0)

    def isGoal(self, state):
        # Se a minha pontuação é maior ou igual o meu objetivo, eu cheguei no meu objetivo
        return state[2] >= self.goal[2]

    # Encontra em self.states o estado equivalente (a ordem dos disponíveis não importa
    # e o trabalho nulo sempre faz parte da lista de disponíveis dos estados)
    def equivalentState(self, current_work, available_actions, score):
        for other_state in self.states:
            listed = [work for work in other_state[1] if work != [0, 0, 0, 0]]
            if current_work == other_state[0] and score == other_state[2] \
               and len(listed) == len(available_actions) and all(work in listed for work in available_actions):
                return [other_state[0], list(other_state[1]), other_state[2]]
        return [current_work, list(available_actions), score]

    # Ponto único de decisão: valida a escolha externa (GUI, agente) ou, na ausência dela,
    # delega para self.policy (ou sorteia). O trabalho nulo [0, 0, 0, 0] (ócio) é uma opção válida.
    def chooseWork(self, state : list, actions: list, choice = None):
        if not actions:
            return None
        if choice is None:
            choice = self.policy(state, actions) if self.policy else random.choice(actions)
        if choice not in actions:
            raise ValueError("O trabalho escolhido não está disponível")
        return choice

    def nextState(self, state, action = None):

        current_work = state[0]
        score = state[2]
        events = []

        # Estado-meta é absorvente
        if self.isGoal(state):
            self.last_events = []
            return [current_work, list(state[1]), score]

        # Definindo forma dos trabalhos disponíveis (cópia, sem o trabalho nulo)
        available_actions = [work for work in state[1] if work != [0, 0, 0, 0]]

        # Ocioso: é obrigado a escolher entre os trabalhos disponíveis ou o trabalho nulo (ócio)
        picked = False
        if current_work == [0, 0, 0, 0]:
            options = [[0, 0, 0, 0]] + available_actions
            current_work = self.chooseWork(state, options, action)
            if current_work == [0, 0, 0, 0]:
                events.append(("idle", current_work))
            else:
                available_actions.remove(current_work) # O trabalho aceito sai da lista
                events.append(("picked", current_work))
                picked = True

        # Terminando (ou não) o trabalho (não no mesmo turno em que foi selecionado)
        if not picked:
            working = current_work
            current_work, score_result = aux.finish_work(current_work)
            score = min(score + score_result, self.max_reward)
            if working != [0, 0, 0, 0] and current_work == [0, 0, 0, 0]:
                events.append(("finished", working, score_result))

        # Trabalho(s) sumindo (só os que já estavam na lista no início do turno)
        previous = list(available_actions)
        available_actions = aux.remove_from_available_list(list(previous))
        events += [("disappeared", work) for work in previous if work not in available_actions]

        # Trabalho(s) aparecendo (os que acabaram de sumir não reaparecem no mesmo turno)
        before = list(available_actions)
        available_actions = aux.add_in_available_list([work for work in self.works if work not in previous], available_actions)
        events += [("appeared", work) for work in available_actions if work not in before]

        self.last_events = events

        # Encontrando novo estado equivalente ao atual
        return self.equivalentState(current_work, available_actions, score)

    def reward(self, state, action):
        if self.isGoal(state):
            return 0
        else:
            return -1

    def simulateStep(self,state,action):
        r = self.reward(state, action)
        nextState = self.nextState(state,action) # nextState já devolve um único estado sorteado
        return nextState, r

    def step(self, action = None):
        self.state, r = self.simulateStep(self.state, action)
        return self.state, r
