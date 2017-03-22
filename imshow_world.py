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





