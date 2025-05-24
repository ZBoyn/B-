
class pro3Env:
    def __init__(self):
        self.state = None
        self.action_space = None
        self.observation_space = None
        self.reward_range = None
        self.spec = None
        self.metadata = None
        self.unwrapped = None
        self.np_random = None
        self._max_episode_steps = None
        self._elapsed_steps = 0

    def reset(self):
        pass

    def step(self, action):
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        pass