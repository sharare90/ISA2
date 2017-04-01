from copy import deepcopy

import pygame

from a_star import AStar



def sign(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


class AStarSimulator(object):
    def __init__(self, start_frame=None):
        self.start_frame = start_frame
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
        self.previous_action_before_simulation = None
        self.actions = {
            0: "Place Wall",
            1: "Choose Start Position",
            2: "Choose End Position",
            3: "Running!!!",
            4: "There is no path to goal."
        }
        self.current_action = 0
        self.hover = 0
        self.size = self.width, self.height = 640, 480
        self.nrows = int(self.height / self.cell_height)
        self.ncols = int(self.width / self.cell_width)
        self.world = [[-1 for i in range(self.ncols)] for j in range(self.nrows)]

        self.menu_width = 200
        self.menu_bg = 255, 255, 255
        self.menu_button_color = 65, 0, 0
        self.menu_button_hover_color = 0, 0, 0
        self.menu_button_text_color = 255, 255, 255

        self.screen = pygame.display.set_mode((self.width + self.menu_width, self.height))
        self.delay_time = 20

        pygame.init()
        self.font = pygame.font.SysFont("monospace", 15)

    def check_quit(self, event):
        if event.type == pygame.QUIT:
            self.playing = False
            self.start_frame.a_star_simulator = None
            pygame.display.quit()

    def place_wall(self, event):
        i = int(event.pos[0] / self.cell_width)
        j = int(event.pos[1] / self.cell_height)
        if self.world[j][i] == -1:
            if self.robot_x != j * self.cell_height or self.robot_y != i * self.cell_width :
                if self.goal_x != j or self.goal_y != i:
                    self.world[j][i] = 0

    def place_start(self, event):
        i = int(event.pos[0] / self.cell_width)
        j = int(event.pos[1] / self.cell_height)
        if self.world[j][i] == -1:
            self.robot_y = i * self.cell_width
            self.robot_x = j * self.cell_height

    def place_end(self, event):
        i = int(event.pos[0] / self.cell_width)
        j = int(event.pos[1] / self.cell_height)
        if self.world[j][i] == -1:
            self.goal_y = i
            self.goal_x = j

    def check_menu_click(self, event):
        x = event.pos[0]
        y = event.pos[1]
        if event.type == pygame.MOUSEMOTION:
            x = self.width + 20
            if 60 < y < 80:
                self.hover = 1
            elif 100 < y < 120:
                self.hover = 2
            elif 140 < y < 160:
                self.hover = 3
            elif 180 < y < 200:
                self.hover = 4
            elif 220 < y < 240:
                self.hover = 5
            else:
                self.hover = 0

        if event.type == pygame.MOUSEBUTTONDOWN and self.current_action != 3:
            if self.width + 20 < x < self.width + 170:
                if 60 < y < 80:
                    self.current_action = 1
                elif 100 < y < 120:
                    self.current_action = 2
                elif 140 < y < 160:
                    self.current_action = 0
                elif 180 < y < 200:
                    self.previous_action_before_simulation = self.current_action
                    self.current_action = 3
                    self.path = self.solve_a_star()
                    if not self.path:
                        self.current_action = 4
                elif 220 < y < 240:
                    self.world = [[-1 for i in range(self.ncols)] for j in range(self.nrows)]

    def check_click(self, event):
        if hasattr(event, 'pos'):
            if event.pos[0] >= self.width:
                self.check_menu_click(event)
            else:
                if self.current_action == 0 and event.type == pygame.MOUSEMOTION and event.buttons == (1, 0, 0):
                    self.place_wall(event)
                elif self.current_action == 1 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.place_start(event)
                elif self.current_action == 2 and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.place_end(event)

    def solve_a_star(self):
        world = deepcopy(self.world)
        x = int(self.robot_x / self.cell_width)
        y = int(self.robot_y / self.cell_height)
        world[x][y] = -1
        a_star = AStar(world, start_point=(x, y), end_point=(self.goal_x, self.goal_y))
        a_star.a_star()
        return a_star.get_path()

    def animate_motion(self):
        if not self.path and self.current_action == 3:
            self.current_action = self.previous_action_before_simulation

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

    def draw_button(self, y, text):
        button_id = int((y - 60) / 40 + 1)
        if button_id == self.hover:
            color = self.menu_button_hover_color
        else:
            color = self.menu_button_color

        label = self.font.render(text, True, self.menu_button_text_color)
        label_rect = label.get_rect()
        label_rect.center = (self.width + 95, y + 10)
        rect = (self.width + 20, y, 150, 20)
        pygame.draw.rect(self.screen, color, rect)
        self.screen.blit(label, label_rect)

    def draw_label(self, y, text):
        label = self.font.render(text, True, self.menu_button_color)
        label_rect = label.get_rect()
        label_rect.center = (self.width + 95, y + 10)
        self.screen.blit(label, label_rect)

    def draw_menu(self):
        pygame.draw.rect(self.screen, self.menu_bg, (self.width, 0, self.menu_width, self.height))
        self.draw_label(20, self.actions[self.current_action])
        self.draw_button(60, "Start Position")
        self.draw_button(100, "End Position")
        self.draw_button(140, "Wall")
        self.draw_button(180, "Start Simulation")
        self.draw_button(220, "Remove all walls")

    def start_simulation(self):
        self.playing = True

        while self.playing:
            pygame.time.delay(self.delay_time)

            self.screen.fill(self.bg_color)
            self.draw_menu()
            self.draw_world()
            self.animate_motion()

            pygame.display.flip()
            for event in pygame.event.get():
                self.check_click(event)
                self.check_quit(event)

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
