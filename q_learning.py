from imshow_world import show_world
from random import randrange


class QLearning(object):
    def __init__(self, file_name, is_stochastic):
        self.action_policy = None
        self.world = QLearning.read_data(file_name)
        self.nrows = len(self.world)
        self.ncols = len(self.world[0])
        self.location = (0, 0)
        self.Q = [[[0 for i in range(4)] for j in range(self.ncols)] for k in range(self.nrows)]
        self.number_of_steps = None
        self.number_of_episodes = None
        self.learning_rate = None
        self.discount_factor = None
        self.is_stochastic = is_stochastic

    def best_step(self):
        if self.world[self.location[0]][self.location[1]] != 100:
            self.transition(action=self.best_action())

    @staticmethod
    def read_data(file_name):
        world = []
        with open(file_name) as f:
            for line in f:
                world.append([int(i) for i in line.split()])
        return world

    def in_the_world(self, location):
        return -1 < location[0] < self.nrows and -1 < location[1] < self.ncols

    def reward(self, location):
        if self.in_the_world(location):
            return self.world[location[0]][location[1]]
        return -100

    def available_actions(self):
        return 'LRUD'

    def get_new_location(self, action):
        if action == 'L':
            return self.location[0], self.location[1] - 1
        elif action == 'R':
            return self.location[0], self.location[1] + 1
        elif action == 'U':
            return self.location[0] - 1, self.location[1]
        elif action == 'D':
            return self.location[0] + 1, self.location[1]

    def transition(self, action):
        if not self.is_stochastic:
            return self.normal_transition(action)
        else:
            return self.stochastic_transition(action)

    def normal_transition(self, action):
        new_location = self.get_new_location(action)
        new_location_reward = self.reward(new_location)
        if self.transition_is_ok(new_location):
            self.location = new_location
        return new_location_reward

    def stochastic_transition(self, action):
        random_generated_number = randrange(100 + 1) / 100.0
        if random_generated_number <= 0.6:
            return self.normal_transition(action)
        elif 0.6 < random_generated_number <= 0.7:
            return -1.0
        else:
            other_actions = self.available_actions().replace(action, "")
            new_action = other_actions[randrange(3)]
            return self.normal_transition(new_action)

    def transition_is_ok(self, location):
        if self.in_the_world(location) and self.world[location[0]][location[1]] != -1:
            return True
        return False

    def best_action(self):
        actions_q = self.Q[self.location[0]][self.location[1]]
        return self.available_actions()[actions_q.index(max(actions_q))]

    def get_action(self):
        # Return 0, 1, 2, 3 for L, R, U, D
        if self.action_policy == 'epsilon-policy':
            epsilon = 0.9
            random_generated_number = randrange(100)
            if random_generated_number > epsilon * 100:
                action = self.best_action()
                return self.available_actions().index(action)
            else:
                return randrange(4)
        return randrange(4)

    def step(self):
        previous_location = self.location
        action = self.get_action()
        # print('Moving {action_letter} ...'.format(action_letter=self.available_actions()[action]))

        immediate_reward = self.transition(self.available_actions()[action])
        # print('Reward: {reward}'.format(reward=immediate_reward))

        old_q_value = self.Q[previous_location[0]][previous_location[1]][action]
        best_action = self.available_actions().index(self.best_action())
        best_action_q = self.Q[self.location[0]][self.location[1]][best_action]

        self.Q[previous_location[0]][previous_location[1]][action] = old_q_value + self.learning_rate * (
            immediate_reward + self.discount_factor * best_action_q - old_q_value
        )

    def episode(self):
        self.location = (0, 0)
        count = 0
        while count < self.number_of_steps and self.world[self.location[0]][self.location[1]] != 100:
            self.step()
            count += 1

    def train(self, learning_rate, discount_factor, number_of_steps, number_of_episodes, action_policy=None):
        self.action_policy = action_policy
        self.number_of_steps = number_of_steps
        self.number_of_episodes = number_of_episodes
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        for i in range(self.number_of_episodes):
            self.episode()

    def demo(self):
        show_world(self.world, *self.location)


if __name__ == '__main__':
    q = QLearning("./board.txt", is_stochastic=True)
    q.train(learning_rate=0.9, discount_factor=0.9, number_of_steps=150, number_of_episodes=10000)
    # print(q.in_the_world(q.location))
    # print(q.transition('L'))
    # print(q.transition('R'))
    # print(q.transition('U'))
    # print(q.transition('R'))
    # print(q.transition('R'))
    # print(q.transition('D'))
    # print(q.transition('D'))
    # print(q.transition('D'))
    # print(q.transition('D'))
    # print(q.transition('L'))
    # print(q.transition('R'))
    # print(q.transition('R'))
    # print(q.transition('R'))
    # print(q.transition('R'))
    # print(q.transition('R'))
    # print(q.transition('U'))
    # print(q.transition('U'))
    # print(q.transition('U'))
    # print(q.location)

    l = [[0 for i in range(10)] for j in range(10)]
    r = [[0 for i in range(10)] for j in range(10)]
    u = [[0 for i in range(10)] for j in range(10)]
    d = [[0 for i in range(10)] for j in range(10)]

    for i in range(10):
        for j in range(10):
            l[i][j] = float("{0:.2f}".format(q.Q[i][j][0]))
            r[i][j] = float("{0:.2f}".format(q.Q[i][j][1]))
            u[i][j] = float("{0:.2f}".format(q.Q[i][j][2]))
            d[i][j] = float("{0:.2f}".format(q.Q[i][j][3]))

    show_world(l, *q.location)
    show_world(r, *q.location)
    show_world(u, *q.location)
    show_world(d, *q.location)
