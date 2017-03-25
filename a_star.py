from imshow_world import show_world
from heapq import heappush, heappop


class AStar(object):
    def __init__(self, file_name, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point
        self.world = AStar.read_data(file_name)
        self.nrows = len(self.world)
        self.ncols = len(self.world[0])
        self.closed = []
        self.current_point = start_point
        self.min_heap = []
        heappush(self.min_heap, (self.calculate_cost(self.current_point), self.current_point))

    @staticmethod
    def read_data(file_name):
        world = []
        with open(file_name) as f:
            for line in f:
                world.append([int(i) for i in line.split()])
        return world

    @staticmethod
    def calculate_distance(first_node, second_node):
        # return (first_node[0] - second_node[0]) ** 2 + (first_node[1] - second_node[1]) ** 2
        return abs(first_node[0] - second_node[0]) + abs(first_node[1] - second_node[1])

    def find_neighbors(self):
        left = self.current_point[0], self.current_point[1] - 1
        right = self.current_point[0], self.current_point[1] + 1
        up = self.current_point[0] - 1, self.current_point[1]
        down = self.current_point[0] + 1, self.current_point[1]
        neighbors = []
        if min([0 <= x < self.nrows for x in left]):
            neighbors.append(left)
        if min([0 <= x < self.nrows for x in right]):
            neighbors.append(right)
        if min([0 <= x < self.nrows for x in up]):
            neighbors.append(up)
        if min([0 <= x < self.nrows for x in down]):
            neighbors.append(down)
        return neighbors

    def calculate_g(self, point):
        return AStar.calculate_distance(self.start_point, point)

    def calculate_h(self, point):
        return AStar.calculate_distance(point, self.end_point)

    def calculate_cost(self, neighbor):
        g = self.calculate_g(neighbor)
        h = self.calculate_h(neighbor)
        f = g + h
        return int(str(f) + str(h) + str(g))

    def calculate_min_f(self):
        return heappop(self.min_heap)

    def a_star(self):
        self.closed.append(self.current_point)
        while self.min_heap:
            self.current_point = self.calculate_min_f()[1]
            print(self.current_point)
            print(self.calculate_cost(self.current_point))
            if self.current_point == self.end_point:
                break

            neighbors = self.find_neighbors()
            for neighbor in neighbors:
                if self.world[neighbor[0]][neighbor[1]] < 0 or (neighbor in self.closed):
                    continue

                self.closed.append(neighbor)
                heappush(self.min_heap, (self.calculate_cost(neighbor), neighbor))



if __name__ == '__main__':
    q = AStar("./board.txt", (9, 0), (1, 8))
    q.a_star()
    show_world(q.world, *q.current_point)
