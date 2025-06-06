from base_agent import Agent

class RandomSearchAgent(Agent):
    def __init__(self, max_steps=1000):
        super().__init__()
        self.max_steps = max_steps
        self.steps_taken = 0
        self.success = False

    def search(self, ogm):
        ogm.init_actions()

        while self.steps_taken < self.max_steps:
            possible_actions = ogm.calc_possible_actions()
            module, action = self.select_action(possible_actions, len(ogm.modules))
            ogm.take_action(module, action)
            self.steps_taken += 1

            if ogm.check_final():
                self.success = True
                print(f"Goal reached in {self.steps_taken} steps!")
                return True

        print(f"Failed to reach goal in {self.max_steps} steps.")
        return False
    
