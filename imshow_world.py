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


def show_a_star(a_star, robot_i, robot_j):
    number_of_rows = len(a_star.world)
    number_of_columns = len(a_star.world[0])
    # plt.pcolor(world, edgecolors='k', linewidths=2, cmap='RdYlBu', vmin=0.0, vmax=1.0)
    path = a_star.get_path()
    for i in range(number_of_rows):
        for j in range(number_of_columns):
            c = 'black'
            if (i, j) in a_star.g_scores:
                g_score = a_star.g_scores[(i, j)]
                h_score = a_star.calculate_h((i, j))
                f_score = g_score + h_score
                c = 'blue'
            else:
                g_score = 'No G'
                f_score = 'No F'

            c = 'red' if (i, j) in path else c
            if (i, j) == a_star.start_point:
                c = 'green'
            if (i, j) == a_star.end_point:
                c = 'yellow'
            if a_star.world[i][j] == 0:
                plt.text(
                    j,
                    number_of_rows - 1 - i,
                    "Wall",
                    color='brown'
                )
            else:
                plt.text(
                    j,
                    number_of_rows - 1 - i,
                    "g: {} \n h: {} \n f: {}".format(g_score, h_score, f_score),
                    color=c
                )
            # if world[i][j] == 0:
            #     plt.text(j, i, '0')
            # elif world[i][j] == 256:
            #     plt.text(j, i, '-1')
            # elif world[i][j] == 100:
            #     plt.text(j, i, '100')

    # plt.text(robot_j, number_of_rows - 1 - robot_i, '****', color='G')
    plt.xticks(range(number_of_columns + 1))
    plt.yticks(range(number_of_rows + 1))
    plt.show()
