import numpy as np
import random
import matplotlib.pyplot as plt
import sys
sys.setrecursionlimit(2000)


def dfs(map, i, j, num):
    o = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    if num > 700:
        return map
    if i == 0:
        if j == 0:
            return dfs(map, i+1, j+1, num)
        else:
            return dfs(map, i+1, j, num)

    if j == 0:
        return dfs(map, i, j+1, num)

    if i == map.shape[0]:
        if j == map.shape[1]:
            return dfs(map, i-1, j-1, num)
        else:
            return dfs(map, i-1, j, num)

    if j == map.shape[1]:
        return dfs(map, i, j-1, num)

    if (map[i][j] == 1):
        num = num-1
    map[i][j] = 1
    index = int(random.random()*4)
    new_i = i + o[index][0]
    new_j = j + o[index][1]
    return dfs(map, new_i, new_j, num+1)


def genMap(shape):
    map = np.zeros(shape)
    start_i = 0
    start_j = 0
    for i in range(map.shape[0]):
        if start_i > 0:
            break
        for j in range(map.shape[1]):
            if random.random() > 0.999:
                start_i = i
                start_j = j
                break

    start_i = map.shape[0]//2
    start_j = map.shape[1]//2
    map = dfs(map, start_i, start_j, 0)
    print(map, start_i, start_j, np.sum(map))

    plt.imshow(map, cmap="Greens")
    plt.waitforbuttonpress()
    np.savetxt("data_random.txt", map, fmt='%f', delimiter=',')
    return map


def getMap():
    return np.loadtxt("data_random.txt", delimiter=',')


def randomData(map, min, max, file):
    data = np.zeros(map.shape)
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i][j] == 1:
                data[i][j] = int(random.random()*(max-min))+min
            else:
                data[i][j] = max

    np.savetxt(file, data, fmt='%f', delimiter=',')
    return data


def randomHumanData(map, min, max, file):
    data = np.zeros(map.shape)
    for i in range(map.shape[0]):
        for j in range(map.shape[1]):
            if map[i][j] == 1 and random.random() > 0.9:
                data[i][j] = 7

    np.savetxt(file, data, fmt='%f', delimiter=',')
    return data


if __name__ == "__main__":
    # map = genMap((70, 80))
    map = getMap()

    randomData(map, 0, 5, "data_random_grass.jpg.txt")
    randomData(map, 0, 5, "data_random_herbivores.jpg.txt")
    randomData(map, 0, 5, "data_random_carnivores.jpg.txt")
    randomHumanData(map, 0, 7, "data_random_human.jpg.txt")
