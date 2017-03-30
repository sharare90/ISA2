from a_star import AStar
import pygame


class AStarSimulator(object):
    def __init__(self):
        self.wall_color = 0, 0, 100
        self.robot_color = 100, 0, 0
        self.goal_color = 100, 100, 100
        self.playing = False
        self.placing_wall = True
        self.bg_color = 0, 100, 0
        self.cell_width = 10
        self.cell_height = 10

        self.size = self.width, self.height = 640, 480
        self.nrows = int(self.height / self.cell_height)
        self.ncols = int(self.width / self.cell_width)
        self.world = [[-1 for i in range(self.ncols)] for j in range(self.nrows)]

        self.world[10][10] = -2
        self.world[32][55] = 100

        self.screen = pygame.display.set_mode(self.size)
        self.delay_time = 1000

        pygame.init()
        self.start_simulation()

    def check_quit(self, event):
        if event.type == pygame.QUIT:
            self.playing = False

    def place_wall(self, event):
        i = int(event.pos[0] / self.cell_width)
        j = int(event.pos[1] / self.cell_height)
        self.world[j][i] = 0

    def check_click(self, event):
        if self.placing_wall and event.type == pygame.MOUSEMOTION and event.buttons == (1, 0, 0):
            self.place_wall(event)

    def check_right_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            self.placing_wall = False
            print("we should give the world to a star to find the answer to this question.")

    def start_simulation(self):
        self.playing = True

        while self.playing:
            # pygame.time.delay(self.delay_time)
            for event in pygame.event.get():
                self.check_quit(event)
                self.check_click(event)
                self.check_right_click(event)

            self.screen.fill(self.bg_color)
            self.draw_world()
            pygame.display.flip()

    def draw_wall(self, i, j):
        rect = [self.cell_width * i, self.cell_height * j, self.cell_width, self.cell_height]
        pygame.draw.rect(self.screen, self.wall_color, rect)

    def draw_robot(self, i, j):
        rect = [self.cell_width * i, self.cell_height * j, self.cell_width, self.cell_height]
        pygame.draw.ellipse(self.screen, self.robot_color, rect)

    def draw_goal(self, i, j):
        rect = [self.cell_width * i, self.cell_height * j, self.cell_width, self.cell_height]
        pygame.draw.ellipse(self.screen, self.goal_color, rect)

    def draw_world(self):
        for i in range(self.ncols):
            for j in range(self.nrows):
                if self.world[j][i] == 0:
                    self.draw_wall(i, j)
                elif self.world[j][i] == -2:
                    self.draw_robot(i, j)
                elif self.world[j][i] == 100:
                    self.draw_goal(i, j)


AStarSimulator()
