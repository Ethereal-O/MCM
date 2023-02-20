import cv2
import numpy as np


def changedir():
    import os
    import sys
    os.chdir(sys.path[0])
    return sys.path[0]


def getStatus(path):
    if path != 'map_herbivores.jpg':
        dic = {(32, 32, 255): 'red', (5, 190, 254): 'orange', (184, 255, 255): 'yellow', (16, 251, 16): 'green', (255,
                                                                                                                  255, 0): 'lightBlue', (255, 255, 255): 'white', (5000, 5000, 5000): 'sb', (0, 0, 0): 'black'}  # , (165, 169, 169):'deepGray', (204, 204, 204):'lightGray'
    else:
        dic = {(32, 32, 255): 'red', (5, 190, 254): 'orange', (184, 255, 255): 'yellow', (16, 251, 16): 'green', (255,
                                                                                                                  255, 0): 'lightBlue', (255, 255, 255): 'white', (204, 204, 204): 'lightGray'}  # , (165, 169, 169):'deepGray',

    img = cv2.imread(path)
    beginPoint = (99, 31)
    res = list()
    for lin in range(70):
        tmpRes = list()
        for col in range(80):
            tmp = dict()
            tmp.clear()
            error = np.zeros(8)
            for x in range(6):
                for y in range(6):
                    cur = img[x + beginPoint[1] + lin *
                              6, y + beginPoint[0] + col * 6]
                    i = 0
                    for color in dic.keys():
                        if color[0] > 20 or color[1] > 20 or color[2] > 20:
                            error[i] = error[i] + abs(color[0] - cur[0]) + abs(
                                color[1] - cur[1]) + abs(color[2] - cur[2])
                            i = i + 1
            curErr = 1000000
            i = 0
            curRes = -1
            for each in dic.keys():
                if (error[i] < curErr):
                    curErr = error[i]
                    cur = each
                    curRes = i
                i = i + 1
            for each in dic.items():
                for x in range(6):
                    for y in range(6):
                        img[x + beginPoint[1] + lin * 6, y +
                            beginPoint[0] + col * 6] = cur
            tmpRes.append(curRes)
        res.append(tmpRes)
    cv2.rectangle(
        img, beginPoint, (beginPoint[0] + 80 * 6, beginPoint[1] + 70 * 6), (255, 0, 0), 1, 4)
    # cv2.imshow(path, img)
    # cv2.waitKey()
    # print(res)

    np.savetxt("data_"+path+".txt", res, fmt='%f', delimiter=',')
    return res


def getHumansData():
    cells = np.array(np.loadtxt(
        "data_map_human.jpg.txt", delimiter=',')).reshape((70, 80))
    for i in range(cells.shape[0]):
        for j in range(cells.shape[1]):
            if cells[i][j] == 7:
                cells[i][j] = 1
            else:
                cells[i][j] = 0
    return cells


def caculateDistance(i, j, l, r):
    return (i-l)*(i-l)+(j-r)*(j-r)


def caculateHumansEffect(humans_cells, mode="normal"):
    human_effect_cells = np.zeros(humans_cells.shape)
    for i in range(human_effect_cells.shape[0]):
        for j in range(human_effect_cells.shape[1]):
            for l in range(humans_cells.shape[0]):
                for r in range(humans_cells.shape[1]):
                    if humans_cells[l][r] == 1:
                        human_effect = caculateDistance(
                            i, j, l, r)
                        if human_effect == 0:
                            human_effect_cells[i][j] += 10
                        else:
                            human_effect_cells[i][j] += 1/human_effect
    human_effect_pos = human_effect_cells > np.mean(human_effect_cells)
    if mode == "normal":
        human_effect_cells = human_effect_cells-np.mean(human_effect_cells)
        np.savetxt("./human_effect/human_effect_cells_"+mode+".txt",
                   human_effect_cells, fmt='%f', delimiter=',')
        np.savetxt("./human_effect/human_effect_pos_"+mode+".txt",
                   human_effect_pos, fmt='%f', delimiter=',')
        return human_effect_cells, human_effect_pos
    if mode == "elec":
        human_effect_cells = human_effect_cells-np.mean(human_effect_cells)
        human_effect_cells[human_effect_cells > 0] = 1000
        np.savetxt("./human_effect/human_effect_cells_"+mode+".txt",
                   human_effect_cells, fmt='%f', delimiter=',')
        np.savetxt("./human_effect/human_effect_pos_"+mode+".txt",
                   human_effect_pos, fmt='%f', delimiter=',')
        return human_effect_cells, human_effect_pos
    if mode == "random":
        np.savetxt("./human_effect/human_effect_cells_"+mode+".txt",
                   human_effect_cells, fmt='%f', delimiter=',')
        np.savetxt("./human_effect/human_effect_pos_"+mode+".txt",
                   human_effect_pos, fmt='%f', delimiter=',')
        return human_effect_cells, human_effect_pos
    else:
        human_effect_cells *= 10
        np.savetxt("./human_effect/human_effect_cells_"+mode+".txt",
                   human_effect_cells, fmt='%f', delimiter=',')
        np.savetxt("./human_effect/human_effect_pos_"+mode+".txt",
                   human_effect_pos, fmt='%f', delimiter=',')
        return human_effect_cells, human_effect_pos


if __name__ == '__main__':
    changedir()
    caculateHumansEffect(getHumansData(), "normal")
    caculateHumansEffect(getHumansData(), "elec")
    caculateHumansEffect(getHumansData(), "random")
    caculateHumansEffect(getHumansData(), "hunt")
