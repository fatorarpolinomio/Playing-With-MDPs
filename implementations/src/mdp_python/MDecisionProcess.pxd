from libcpp.vector cimport vector

cdef extern from "MDecisionProcess.hpp":
    cdef cppclass AgentEnvironment:
        double calculateReturn(double discountRate, double rewardReturn,
                     vector[double] returns);
        double calculatePolicyProb(double action, double state);
        double calculateTransFunc(double actions, double returns,
                                double states);
        double getDiscountRate()
        double getRewardReturn()
        double getPolicy()
        vector[double] getReturns()
        vector[double] getActions()
        vector[double] getStates()
        void setDiscountRate(double discountRate)
        void setRewardReturn(double rewardReturn)
        void setPolicy(double value)
        void setReturns(vector[double] returns)
        void setActions(vector[double] actions)
        void setStates(vector[double] states)

    cdef cppclass ValueFunctions(AgentEnvironment):
        double actionValueFunction(double state, double action, double discountRate,
                             vector[double] currentValues,
                             vector[double] returns,
                             vector[double] states);
        ValueFunctions(double rewardValue, double discountRate) except +

        double getRewardValue()
        double getTransitionFunctionValue()

        void setRewardValue(double value)
        void setTransitionFunctionValue(double value)

        void applyCalculateReturn(double discountRate, double rewardReturn,
        vector[double] returns);
        double applyBellmanEquation(double state, double discountRate,
        double rewardValue,
        vector[double] currentValues,
        vector[double] actions,
        vector[double] returns,
        vector[double] states);


    cdef cppclass DynamicProgramming(ValueFunctions):
        DynamicProgramming(double rewardValue, double discountRate, double threshold) except +
        void applyPolicyEval(double discountRate, double rewardValue,
                      double threshold, vector[double] &currentValues,
                      vector[double] actions, vector[double] returns,
                      vector[double] states);
        void applyPolicyIter(double discountRate, double rewardValue,
                      double threshold, vector[double] &currentValues,
                      vector[double] actions, vector[double] returns,
                      vector[double] states,
                      vector[double] &policyPerState);
        void applyValueIter(double discountRate, double rewardValue, double threshold,
                     vector[double] &currentValues,
                     vector[double] actions, vector[double] returns,
                     vector[double] states);
        double getThreshold()
        void setThreshold(double value)
