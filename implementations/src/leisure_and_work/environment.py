import aux_funcs as aux
import random

class LW_Environment:
    def __init__ (self, n_works: int = 2):
        self.works = aux.work_collection_generator(n_works)
        self.states = aux.state_collection_creator(self.works)
        self.policy = None # Opcional: função (state, actions) -> trabalho, usada por chooseWork
        self.reset()

    # Volta para o estado inicial
    # Estado inicial: trabalho nulo e nenhum trabalho disponível
    def reset(self):
        self.last_events = [] # Eventos do último passo (informativo, usado pela GUI)
        self.state = self.equivalentState([0, 0, 0, 0], [])

    # Encontra em self.states o estado equivalente (a ordem dos disponíveis não importa
    # e o trabalho nulo sempre faz parte da lista de disponíveis dos estados)
    def equivalentState(self, current_work, available_actions):
        for other_state in self.states:
            listed = [work for work in other_state[1] if work != [0, 0, 0, 0]]
            if current_work == other_state[0] \
               and len(listed) == len(available_actions) and all(work in listed for work in available_actions):
                return [other_state[0], list(other_state[1])]
        return [current_work, list(available_actions)]

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
        events = []

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
        return self.equivalentState(current_work, available_actions)

    # R(s, a, s'): a recompensa do trabalho é paga só no turno em que ele é concluído
    def reward(self, state, action, next_state):
        if state[0] != [0, 0, 0, 0] and next_state[0] == [0, 0, 0, 0]:
            return state[0][1]
        return 0

    def simulateStep(self,state,action):
        nextState = self.nextState(state,action) # nextState já devolve um único estado sorteado
        r = self.reward(state, action, nextState)
        return nextState, r

    def step(self, action = None):
        self.state, r = self.simulateStep(self.state, action)
        return self.state, r






# Pr(S(t+1) = s'| S(t) = s, A(t) = a)
def transfunc_LW(
    target_state : list,
    start_state : list,
    state_list: list,
    action : list):

    current_state = start_state
    # Se o meu trabalho é o trabalho nulo (i.e., caso eu esteja ocioso)
    # E a ação escolhida estiver na lista de disponíveis
    if (current_state[0] == [0, 0, 0, 0]) and action in current_state[1]:

            # Se estiver na lista, então será selecionada
            current_state[0] = action

             # Se a ação não for o nulo, remova ela da lista
            if action != [0, 0, 0, 0]:
                current_state[1].remove(action)

    # Se o trabalho que o agente irá realizar no próximo turno não for o trabalho sendo realizado no
    # estado-alvo, não existe chance de transitar para lá
    if current_state[0] != target_state[0]:
        return 0

    # Computar probabilidades
    prob = 1
    not_show_up_works = state_list # Será transformada na lista de trabalhos que não podem estar disponíveis

    for work in target_state[1]:

        # Transformando na lista de trabalhos que não podem estar disponíveis
        not_show_up_works.remove(work)

        # Caso o trabalho esteja na lista de disponíveis, qual a chance dele não sumir?
        # (queremos que ele não suma)
        if work in current_state[1]:
            prob = prob * (1 - work[4])
        # Caso o trabalho não esteja, qual a chance dele aparecer?
        # (queremos que ele apareça)
        else:
            prob = prob * work[3]

    for work in not_show_up_works:
        # Caso o trabalho esteja na lista de disponíveis, qual a chance dele sumir?
        # (queremos que ele suma)
        if work in current_state[1]:
            prob = prob * work[4]
        # Caso o trabalho não esteja, qual a chance dele não aparecer?
        # (querems que le não apareça)
        else:
            prob = prob * (1 - work[3])

    return prob
