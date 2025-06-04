import numpy as np

class Agent:
  #def __init__(self):

  def select_action(self, available_actions, num_modules):
    actions_to_take = {}

    for m in range(1,num_modules+1):
      actions_to_take[m] = np.where(available_actions[m])[0] + 1

    module = np.random.randint(1,m+1)
    actions = actions_to_take[module]

    while len(actions) < 1:
      module = np.random.randint(1,m+1)
      actions = actions_to_take[module]

    return (module, actions[np.random.randint(len(actions))])
