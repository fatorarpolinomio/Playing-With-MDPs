import MDecisionProcess
from libcpp.vector cimport vector

cdef class PyValueFunctions:
    cdef ValueFunctions* c_vf

    def __cinit__(self, double rewardValue, double discountRate):
        # Evita instanciar se estivermos a ser chamados por uma subclasse
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

    def action_value_function(self, double state, double discountRate, double rewardValue, list currentValues, list actions, list returns, list states):
        return self.c_dp.actionValueFunction(state, discountRate, rewardValue, currentValues, actions, returns, states)

    def apply_bellman_equation(self, double state, double discountRate, double rewardValue, list currentValues, list actions, list returns, list states):
       cdef vector[double] c_currentValues = currentValues
       cdef vector[double] c_actions = actions
       cdef vector[double] c_returns = returns
       cdef vector[double] c_states = states
       return self.c_vf.applyBellmanEquation(state, discountRate, rewardValue, c_currentValues, c_actions, c_returns, c_states)

cdef class PyDynamicProgramming(PyValueFunctions):
    cdef DynamicProgramming* c_dp

    def __cinit__(self, double rewardValue, double discountRate, double threshold):
        self.c_dp = new DynamicProgramming(rewardValue, discountRate, threshold)

    def __dealloc__(self):
        del self.c_dp

    # Métodos get/set expostos para o Python
    @property
    def threshold(self):
        return self.c_dp.getThreshold()

    @threshold.setter
    def threshold(self, value):
        self.c_dp.setThreshold(value)

    def apply_policy_eval(self, double discountRate, double rewardValue, double threshold, list currentValues, list actions, list returns, list states):
        cdef vector[double] c_currentValues
        cdef vector[double] c_returns
        cdef vector[double] c_states
        cdef vector[double] c_actions


        self.c_dp.applyPolicyEval(discountRate, rewardValue, threshold, c_currentValues, c_actions, c_returns, c_states)

        return c_currentValues

    def apply_policy_iteration(self, double discountRate, double rewardValue, double threshold, list currentValues, list actions, list returns, list states, list policy_per_state):
        cdef vector[double] c_currentValues
        cdef vector[double] c_returns
        cdef vector[double] c_states
        cdef vector[double] c_actions
        cdef vector[double] c_policy_per_state

        self.c_dp.applyPolicyIteration(discountRate, rewardValue, threshold, c_currentValues, c_actions, c_returns, c_states, c_policy_per_state)

        return c_currentValues, c_policy_per_state

    def apply_value_iteration(self, double discountRate, double rewardValue, double threshold, list currentValues, list actions, list returns, list states):
        cdef vector[double] c_currentValues
        cdef vector[double] c_returns
        cdef vector[double] c_states
        cdef vector[double] c_actions

        self.c_dp.applyValueIteration(discountRate, rewardValue, threshold, c_currentValues, c_actions, c_returns, c_states)

        return c_currentValues
