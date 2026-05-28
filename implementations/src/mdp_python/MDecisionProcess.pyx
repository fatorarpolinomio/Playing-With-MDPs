from libcpp.vector cimport vector

cdef class PyAgentEnvironment:
    cdef AgentEnvironment* c_ae


    def __cinit__(self, *args, **kwargs):
            if type(self) is PyAgentEnvironment:
                self.c_ae = new AgentEnvironment()

    def __dealloc__(self):
        if self.c_ae is not NULL:
            del self.c_ae

    @property
    def discount_rate(self):
        return self.c_ae.getDiscountRate()

    @discount_rate.setter
    def discount_rate(self, double value):
        self.c_ae.setDiscountRate(value)

    @property
    def reward_return(self):
        return self.c_ae.getRewardReturn()

    @reward_return.setter
    def reward_return(self, double value):
        self.c_ae.setRewardReturn(value)

    @property
    def policy(self):
        return self.c_ae.getPolicy()

    @policy.setter
    def policy(self, double policy):
        self.c_ae.setPolicy(policy)

    @property
    def returns(self):
        return self.c_ae.getReturns()

    @returns.setter
    def returns(self, list returns): # Setter Python deve receber list
        self.c_ae.setReturns(returns)

    @property
    def actions(self):
        return self.c_ae.getActions()

    @actions.setter
    def actions(self, list actions):
        self.c_ae.setActions(actions)

    @property
    def states(self):
        return self.c_ae.getStates()

    @states.setter
    def states(self, list states):
        self.c_ae.setStates(states)

    @property
    def trans_func_per_action(self):
        # Lê do C++ (converte vector 3D para lista do Python automaticamente)
        return self.c_ae.getTransFuncAsVectors()

    @property
    def get_state_values(self):
        return self.c_ae.getStateValues()

    def get_state_value_by_index(self, int index):
        return self.c_ae.getStateValueByIndex(index)

    def set_state_value_by_index(self, int index, double value):
        self.c_ae.setStateValueByIndex(index, value)

    def set_state_values(self, list state_values):
        cdef vector[double] c_values = state_values
        self.c_ae.setStateValues(c_values)

    @trans_func_per_action.setter
    def trans_func_per_action(self, list matrizes):
        # Pega a lista do Python, tipa como vector 3D, e envia pro C++
        cdef vector[vector[vector[double]]] c_matrizes = matrizes
        self.c_ae.setTransFuncFromVectors(c_matrizes)

    def apply_calculate_return(self, double discountRate, double rewardReturn, list returns):
        cdef vector[double] c_returns = returns
        self.c_ae.applyCalculateReturn(discountRate, rewardReturn, c_returns)

    def apply_calculate_policy_prob(self, double action, double state):
        return self.c_ae.applyCalculatePolicyProb(action, state)

    def apply_calculate_trans_func(self, double actions, double start_state, double returns, double states):
        return self.c_ae.applyCalculateTransFunc(actions, start_state, returns, states)


cdef class PyValueFunctions:
    cdef ValueFunctions* c_vf

    def __cinit__(self, *args, **kwargs):
            if type(self) is PyValueFunctions:
                # Ele pega os dois primeiros argumentos (rewardValue e discountRate)
                self.c_vf = new ValueFunctions(args[0], args[1])

    def __dealloc__(self):
        if self.c_vf is not NULL:
            del self.c_vf

    @property
    def reward_value(self):
        return self.c_vf.getRewardValue()

    @reward_value.setter
    def reward_value(self, double value):
        self.c_vf.setRewardValue(value)

    @property
    def transition_function_value(self):
        return self.c_vf.getTransitionFunctionValue()

    @transition_function_value.setter
    def transition_function_value(self, double value):
        self.c_vf.setTransitionFunctionValue(value)

    def action_value_function(self, double state, double action, double discountRate, list currentValues, list returns, list states):
        cdef vector[double] c_currentValues = currentValues
        cdef vector[double] c_returns = returns
        cdef vector[double] c_states = states
        return self.c_vf.actionValueFunction(state, action, discountRate, c_currentValues, c_returns, c_states)

    def apply_bellman_equation(self, double state, double discountRate, double rewardValue, list currentValues, list actions, list returns, list states):
       cdef vector[double] c_currentValues = currentValues
       cdef vector[double] c_actions = actions
       cdef vector[double] c_returns = returns
       cdef vector[double] c_states = states
       return self.c_vf.applyBellmanEquation(state, discountRate, rewardValue, c_currentValues, c_actions, c_returns, c_states)


cdef class PyDynamicProgramming(PyValueFunctions):

    def __cinit__(self, double rewardValue, double discountRate, double threshold):
        # Cast para ValueFunctions* para guardar no ponteiro da classe pai
        self.c_vf = <ValueFunctions*> new DynamicProgramming(rewardValue, discountRate, threshold)



    @property
    def threshold(self):
        return (<DynamicProgramming*>self.c_vf).getThreshold()

    @threshold.setter
    def threshold(self, value):
        (<DynamicProgramming*>self.c_vf).setThreshold(value)

    @property
    def discount_rate(self):
        return (<DynamicProgramming*>self.c_vf).getDiscountRate()

    @discount_rate.setter
    def discount_rate(self, double value):
        (<DynamicProgramming*>self.c_vf).setDiscountRate(value)

    def apply_policy_eval(self, double discountRate, double rewardValue, double threshold, list currentValues, list actions, list returns, list states):

        cdef vector[double] c_currentValues = currentValues
        cdef vector[double] c_returns = returns
        cdef vector[double] c_states = states
        cdef vector[double] c_actions = actions

        (<DynamicProgramming*>self.c_vf).applyPolicyEval(discountRate, rewardValue, threshold, c_currentValues, c_actions, c_returns, c_states)

        return c_currentValues

    def apply_policy_iteration(self, double discountRate, double rewardValue, double threshold, list currentValues, list actions, list returns, list states, list policy_per_state):
        cdef vector[double] c_currentValues = currentValues
        cdef vector[double] c_returns = returns
        cdef vector[double] c_states = states
        cdef vector[double] c_actions = actions
        cdef vector[double] c_policy_per_state = policy_per_state


        (<DynamicProgramming*>self.c_vf).applyPolicyIter(discountRate, rewardValue, threshold, c_currentValues, c_actions, c_returns, c_states, c_policy_per_state)

        return c_currentValues, c_policy_per_state

    def apply_value_iteration(self, double discountRate, double rewardValue, double threshold, list actions, list returns, list states):
        # Converte as listas do Python para os vetores estritos do C++
        cdef vector[double] c_actions = actions
        cdef vector[double] c_returns = returns
        cdef vector[double] c_states = states
        # Chama o motor! O resultado C++ é armazenado num vetor nativo
        cdef vector[double] c_policy = (<DynamicProgramming*>self.c_vf).applyValueIter(
                    discountRate, rewardValue, threshold, c_actions, c_returns, c_states
                )
        # Retorna direto para o Python!
        # O Cython entende que 'c_policy' é um vector e converte para 'list' instantaneamente.
        return c_policy

    def set_trans_func_per_action(self, list matrizes):
        # Converte a lista 3D do Python para o formato vector do C++
        cdef vector[vector[vector[double]]] c_matrizes = matrizes
        # O C++ entende isso perfeitamente graças à herança no .pxd!
        (<DynamicProgramming*>self.c_vf).setTransFuncFromVectors(c_matrizes)


    def set_state_values(self, list state_values):
        # Converte a lista zerada do Python para o vetor C++
        cdef vector[double] c_values = state_values
        # Envia para a memória base usando o nosso cast certeiro!
        (<DynamicProgramming*>self.c_vf).setStateValues(c_values)

    def get_state_values(self):
        return (<DynamicProgramming*>self.c_vf).getStateValues()
