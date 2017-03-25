import matplotlib.pyplot as plt


def show_world(world, robot_i, robot_j):
    number_of_rows = len(world)
    number_of_columns = len(world[0])
    # plt.pcolor(world, edgecolors='k', linewidths=2, cmap='RdYlBu', vmin=0.0, vmax=1.0)

    for i in range(number_of_rows):
        for j in range(number_of_columns):
            plt.text(j, number_of_rows - 1 - i, world[i][j])
            # if world[i][j] == 0:
            #     plt.text(j, i, '0')
            # elif world[i][j] == 256:
            #     plt.text(j, i, '-1')
            # elif world[i][j] == 100:
            #     plt.text(j, i, '100')

    plt.text(robot_j, number_of_rows - 1 - robot_i, '****', color='G')
    plt.xticks(range(number_of_columns + 1))
    plt.yticks(range(number_of_rows + 1))
    plt.show()


if __name__ == '__main__':
    import pygame
    from pygame.constants import USEREVENT

    pygame.init()
    size = width, height = 640, 480
    color = 0, 100, 0
    screen = pygame.display.set_mode(size)

    robot = pygame.image.load("images/Squirrel.png")
    robot = pygame.transform.scale(robot, (64, 48))

    robot_rect = robot.get_rect()

    playing = True
    while playing:
        pygame.time.delay(500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            # elif event.type == USEREVENT and event.code == 'MENU':
            #     print(event.name)
            #     print(event.item_id)
            #     print(event.text)
            #     if (event.name, event.text) == ('Main', 'Quit'):
            #         playing = False

        robot_rect = robot_rect.move((64, 0))

        screen.fill(color)
        screen.blit(robot, robot_rect)

        pygame.display.flip()

    quit()
