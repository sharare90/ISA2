from q_learning import QLearning
import pygame


class QLearningSimulator(object):
    def __init__(self, q_learning):
        self.playing = False
        self.q_learning = q_learning
        self.q_learning.train(
            learning_rate=0.9,
            discount_factor=0.9,
            number_of_steps=150,
            number_of_episodes=1000
        )

        self.world = q_learning.world
        self.size = self.width, self.height = 640, 480

        self.state_width = self.width / len(self.world[0])
        self.state_height = self.height / len(self.world)

        self.delay_time = 500

        self.bg_color = 0, 100, 0
        self.item_colors = {
            -1: (0, 0, 0),
            100: (0, 0, 255),
            0: (0, 255, 0)
        }
        self.item_thickness = {
            -1: 0,
            100: 0,
            0: 2
        }
        self.screen = pygame.display.set_mode(self.size)

        robot_image = pygame.image.load("images/Squirrel.png")
        self.robot = pygame.transform.scale(robot_image, (64, 48))
        self.robot_rect = self.robot.get_rect()

        self.start_simulation((9, 0))

    def start_simulation(self, start_position):
        self.playing = True
        pygame.init()

        self.q_learning.location = start_position

        while self.playing:
            pygame.time.delay(self.delay_time)
            for event in pygame.event.get():
                self.check_quit(event)

            self.screen.fill(self.bg_color)
            self.draw_world()
            self.draw_robot(*self.q_learning.location)
            pygame.display.flip()
            self.q_learning.best_step()

    def check_quit(self, event):
        if event.type == pygame.QUIT:
            self.playing = False

    def draw_robot(self, i, j):
        top_left = (self.state_width * j, self.state_height * i)
        self.robot_rect = [*top_left, self.state_width, self.state_height]
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
            (*top_left, self.state_width, self.state_height),
            thickness
        )

file_name = "./board.txt"
q_learning = QLearning("./board.txt")

QLearningSimulator(q_learning)


