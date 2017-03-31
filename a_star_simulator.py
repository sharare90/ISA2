from copy import deepcopy

from a_star import AStar
import pygame


def sign(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


class AStarSimulator(object):
    def __init__(self):
        self.temporary_goal_point = None
        self.path = None
        self.simulation_step = 5
        self.wall_color = 0, 0, 100
        self.robot_color = 100, 0, 0
        self.goal_color = 100, 100, 100
        self.playing = False
        self.placing_wall = True
        self.bg_color = 0, 100, 0
        self.cell_width = 10
        self.cell_height = 10
        self.robot_x, self.robot_y = 1 * self.cell_width, 1 * self.cell_height
        self.goal_x, self.goal_y = 32, 55

        self.size = self.width, self.height = 640, 480
        self.nrows = int(self.height / self.cell_height)
        self.ncols = int(self.width / self.cell_width)
        self.world = [[-1 for i in range(self.ncols)] for j in range(self.nrows)]

        self.screen = pygame.display.set_mode(self.size)
        self.delay_time = 20

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

    def solve_a_star(self):
        world = deepcopy(self.world)
        x = int(self.robot_x / self.cell_width)
        y = int(self.robot_y / self.cell_height)
        world[x][y] = -1
        a_star = AStar(world, start_point=(x, y), end_point=(self.goal_x, self.goal_y))
        a_star.a_star()
        return a_star.get_path()

    def check_right_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and not self.path:
            self.placing_wall = False
            self.path = self.solve_a_star()
            if not self.path:
                print('There is no path to goal.')

    def animate_motion(self):
        if self.path and not self.temporary_goal_point:
            point = self.path[0]
            del self.path[0]
            self.temporary_goal_point = (point[0] * self.cell_width, point[1] * self.cell_height)

        if self.temporary_goal_point:
            delta_x = sign(self.temporary_goal_point[0] - self.robot_x)
            delta_y = sign(self.temporary_goal_point[1] - self.robot_y)
            if delta_x == 0 and delta_y == 0:
                self.temporary_goal_point = None
            self.robot_x += delta_x * self.simulation_step
            self.robot_y += delta_y * self.simulation_step

    def start_simulation(self):
        self.playing = True

        while self.playing:
            pygame.time.delay(self.delay_time)
            for event in pygame.event.get():
                self.check_quit(event)
                self.check_click(event)
                self.check_right_click(event)

            self.screen.fill(self.bg_color)
            self.draw_world()
            self.animate_motion()

            pygame.display.flip()

    def draw_wall(self, i, j):
        rect = [self.cell_width * i, self.cell_height * j, self.cell_width, self.cell_height]
        pygame.draw.rect(self.screen, self.wall_color, rect)

    def draw_robot(self, robot_top_left_x, robot_top_left_y):
        rect = [
            robot_top_left_x,
            robot_top_left_y,
            self.cell_width,
            self.cell_height,
        ]
        pygame.draw.ellipse(self.screen, self.robot_color, rect)

    def draw_goal(self, i, j):
        rect = [self.cell_width * i, self.cell_height * j, self.cell_width, self.cell_height]
        pygame.draw.ellipse(self.screen, self.goal_color, rect)

    def draw_world(self):
        for i in range(self.ncols):
            for j in range(self.nrows):
                if self.world[j][i] == 0:
                    self.draw_wall(i, j)
        self.draw_goal(self.goal_y, self.goal_x)
        self.draw_robot(self.robot_y, self.robot_x)

        pygame.display.flip()


AStarSimulator()
