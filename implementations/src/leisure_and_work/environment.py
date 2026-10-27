import modelling as model

class LW_Environment:
    def __init__ (self, x : int, y : int):
        self.state = (0, 0)
        self.goal = (x, y)
        states = model.state_collection_creator(model.work_collection_generator(2), 5)

    def reset(self):
        self.state = (0, 0)

    def reward(self, state, action):
        pass

    def simulateStep(self,state,action):
        pass

    def step(self, action):
        self.state, r = self.simulateStep(self.state, action)
        return self.state, r
