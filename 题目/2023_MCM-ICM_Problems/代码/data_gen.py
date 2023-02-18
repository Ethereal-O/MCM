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
                                                                                                                  255, 0): 'lightBlue', (255, 255, 255): 'white', (5000, 5000, 5000):'sb', (0, 0, 0):'black'}  # , (165, 169, 169):'deepGray', (204, 204, 204):'lightGray'
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


if __name__ == '__main__':
    changedir()
    getStatus('map_human.jpg')
