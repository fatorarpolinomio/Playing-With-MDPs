from libcpp.vector cimport vector

cdef class PyAgentEnvironment:
    cdef AgentEnvironment* c_ae


    def __cinit__(self):
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

    def apply_calculate_return(self, double discountRate, double rewardReturn, list returns):
        cdef vector[double] c_returns = returns
        return self.c_ae.calculateReturn(discountRate, rewardReturn, c_returns)


cdef class PyValueFunctions:
    cdef ValueFunctions* c_vf

    def __cinit__(self, double rewardValue, double discountRate):
        if type(self) is PyValueFunctions:
            self.c_vf = new ValueFunctions(rewardValue, discountRate)

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

    def apply_value_iteration(self, double discountRate, double rewardValue, double threshold, list currentValues, list actions, list returns, list states):
        cdef vector[double] c_currentValues = currentValues
        cdef vector[double] c_returns = returns
        cdef vector[double] c_states = states
        cdef vector[double] c_actions = actions


        (<DynamicProgramming*>self.c_vf).applyValueIter(discountRate, rewardValue, threshold, c_currentValues, c_actions, c_returns, c_states)

        return c_currentValues
