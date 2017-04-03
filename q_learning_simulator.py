from q_learning import QLearning
import pygame


class QLearningSimulator(object):
    def __init__(self, q_learning, delay_time, root_frame=None, action_policy=None, show_q=True, learning_rate=0.9,
                 discount_factor=0.9, number_of_steps=150, number_of_episodes=1000, train_simulation=True):
        pygame.init()
        self.root_frame = root_frame
        self.playing = False
        self.show_q = show_q
        self.q_learning = q_learning
        self.is_simulating_training = False

        self.minimum = self.find_min()
        self.maximum = self.find_max()

        print(self.minimum)
        print(self.maximum)

        self.world = q_learning.world

        infoObject = pygame.display.Info()
        self.size = self.width, self.height = infoObject.current_w - 100, infoObject.current_h - 100

        self.state_width = self.width / len(self.world[0])
        self.state_height = self.height / len(self.world)

        self.q_ellipse_width = self.state_width / 3
        self.q_ellipse_height = self.state_height / 3

        self.delay_time = delay_time

        self.bg_color = 0, 100, 0
        self.item_colors = {
            0: (0, 0, 0),
            100: (0, 0, 255),
            -1: (0, 255, 0)
        }
        self.item_thickness = {
            0: 0,
            100: 0,
            -1: 2
        }
        self.screen = pygame.display.set_mode(self.size)

        robot_image = pygame.image.load("images/Squirrel.png")
        robot_width = int(self.width / len(self.world[0]))
        robot_height = int(self.height / len(self.world))
        self.robot = pygame.transform.scale(robot_image, (robot_width, robot_height))
        self.robot_rect = self.robot.get_rect()

        self.font_size = 10
        self.font = pygame.font.SysFont("Arial", self.font_size)
        self.quited = False

        if train_simulation:
            self.simulate_train(
                learning_rate=learning_rate,
                discount_factor=discount_factor,
                number_of_steps=number_of_steps,
                number_of_episodes=number_of_episodes,
                action_policy=action_policy
            )
        else:
            self.q_learning.train(
                learning_rate=learning_rate,
                discount_factor=discount_factor,
                number_of_steps=number_of_steps,
                number_of_episodes=number_of_episodes,
                action_policy=action_policy
            )

        # self.start_simulation((9, 0))

    def simulate_train(self, learning_rate, discount_factor, number_of_steps, number_of_episodes, action_policy):
        self.is_simulating_training = True
        self.playing = True

        self.q_learning.action_policy = action_policy
        self.q_learning.number_of_steps = number_of_steps
        self.q_learning.number_of_episodes = number_of_episodes
        self.q_learning.learning_rate = learning_rate
        self.q_learning.discount_factor = discount_factor

        for i in range(self.q_learning.number_of_episodes):
            from random import randrange
            random_number = randrange(len(self.q_learning.not_wall_cells))
            self.q_learning.location = self.q_learning.not_wall_cells[random_number]
            count = 0
            while self.playing and count < self.q_learning.number_of_steps and \
                    self.q_learning.world[self.q_learning.location[0]][self.q_learning.location[1]] != 100:

                self.screen.fill(self.bg_color)
                self.draw_world()
                if self.show_q:
                    self.draw_q()
                self.draw_robot(*self.q_learning.location)
                pygame.display.flip()

                self.q_learning.step()
                count += 1
                for event in pygame.event.get():
                    self.check_quit(event)
            if not self.quited:
                pygame.time.delay(1000)

        self.is_simulating_training = False

    def start_simulation(self, start_position):
        self.playing = True
        self.q_learning.location = start_position

        while self.playing:
            pygame.time.delay(self.delay_time)

            self.screen.fill(self.bg_color)
            self.draw_world()
            if self.show_q:
                self.draw_q()
            self.draw_robot(*self.q_learning.location)
            pygame.display.flip()
            self.q_learning.best_step()
            for event in pygame.event.get():
                self.check_click(event)
                self.check_quit(event)

    def draw_q(self):
        actions = self.q_learning.available_actions()

        for i in range(len(self.q_learning.Q)):
            for j in range(len(self.q_learning.Q[i])):
                for k in range(len(actions)):
                    center_i = self.state_height * i + self.state_height / 2
                    center_j = self.state_width * j + self.state_width / 2
                    x, y = center_j, center_i

                    if k == actions.index("L") or k == actions.index("R"):
                        y -= self.q_ellipse_height / 2
                        if k == actions.index("L"):
                            x -= 3 * self.q_ellipse_width / 2
                        else:
                            x += self.q_ellipse_width / 2
                    else:
                        x -= self.q_ellipse_width / 2
                        if k == actions.index("U"):
                            y -= 3 * self.q_ellipse_height / 2
                        else:
                            y += self.q_ellipse_height / 2

                    ellipse_color = self.calculate_heat_map(self.q_learning.Q[i][j][k])
                    pygame.draw.ellipse(self.screen, ellipse_color, [x, y, self.q_ellipse_width, self.q_ellipse_height])

                    text = "{:0.2f}".format(self.q_learning.Q[i][j][k])
                    label = self.font.render(text, 1, (255, 255, 255))
                    self.screen.blit(
                        label,
                        (
                            x + self.q_ellipse_width / 2 - len(text) / 2,
                            y + self.q_ellipse_height / 2 - self.font_size / 2
                        )
                    )

    def find_min(self):
        min_value = 10000000
        for i in self.q_learning.Q:
            for j in i:
                for k in j:
                    if k < min_value:
                        min_value = k
        return min_value

    def find_max(self):
        max_value = - 100000000
        for i in self.q_learning.Q:
            for j in i:
                for k in j:
                    if k > max_value:
                        max_value = k
        return max_value

    def calculate_heat_map(self, value):
        self.maximum = self.find_max()
        self.minimum = self.find_min()
        if self.maximum == self.minimum:
            r, g, b = 0, 255, 0
        else:
            ratio = 2 * (value - self.minimum) / (self.maximum - self.minimum)
            r = int(max(0, 255 * (1 - ratio)))
            g = int(max(0, 255 * (ratio - 1)))
            b = 255 - r - g
        return r, g, b

    def check_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            i = int(event.pos[1] / self.state_height)
            j = int(event.pos[0] / self.state_width)
            if self.world[i][j] != 0:
                self.q_learning.location = (i, j)

    def check_quit(self, event):
        if event.type == pygame.QUIT:
            self.quited = True
            self.playing = False
            self.root_frame.q_learning_simulator = None
            pygame.display.quit()

    def draw_robot(self, i, j):
        top_left = (self.state_width * j, self.state_height * i)
        self.robot_rect = [top_left[0], top_left[1], self.state_width, self.state_height]
        self.screen.blit(self.robot, self.robot_rect)

    def draw_world(self):
        for i in range(len(self.world)):
            for j in range(len(self.world[i])):
                self.draw_rectangle(i, j, self.world[i][j])

    def draw_rectangle(self, i, j, item):
        top_left = (self.state_width * j, self.state_height * i)
        color = self.item_colors[item]
        thickness = self.item_thickness[item]
        pygame.draw.rect(
            self.screen,
            color,
            (top_left[0], top_left[1], self.state_width, self.state_height),
            thickness
        )


if __name__ == '__main__':
    file_name = "./board.txt"
    q_learning = QLearning("./board.txt", is_stochastic=True)

    QLearningSimulator(q_learning, delay_time=100)


