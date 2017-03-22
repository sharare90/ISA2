
def read_data(file_name):
    world = []
    with open(file_name) as f:
        for line in f:
            world.append([int(i) for i in line.split()])
    return world

data_address = "./board.txt"
print(read_data(data_address))
