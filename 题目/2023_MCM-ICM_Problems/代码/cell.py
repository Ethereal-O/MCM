import numpy as np
import math
import cv2
import matplotlib.pyplot as plt


class Check(object):
    def isRayIntersectsSegment(poi, s_poi, e_poi):
        if s_poi[1] == e_poi[1]:
            return False
        if s_poi[1] > poi[1] and e_poi[1] > poi[1]:
            return False
        if s_poi[1] < poi[1] and e_poi[1] < poi[1]:
            return False
        if s_poi[1] == poi[1] and e_poi[1] > poi[1]:
            return False
        if e_poi[1] == poi[1] and s_poi[1] > poi[1]:
            return False
        if s_poi[0] < poi[0] and e_poi[1] < poi[1]:
            return False

        xseg = e_poi[0]-(e_poi[0]-s_poi[0]) * \
            (e_poi[1]-poi[1])/(e_poi[1]-s_poi[1])
        if xseg < poi[0]:
            return False
        return True

    def isPoiWithinPoly(poi, poly):
        sinsc = 0
        for i in range(len(poly)-1):  # [0,len-1]
            s_poi = poly[i]
            e_poi = poly[i+1]
            if Check.isRayIntersectsSegment(poi, s_poi, e_poi):
                sinsc += 1

        return True if sinsc % 2 == 1 else False


class Part(object):
    def __init__(self, national_part, animal_part, farm_part, migaration_part):
        self.national_part = national_part
        self.animal_part = animal_part
        self.farm_part = farm_part
        self.migaration_part = migaration_part


class Cellular(object):
    def __init__(self):
        # 应对策略
        self.strategy = "normal"
        self.isExtendProtect = True

        self.grass_cells = ProcessData.getGrassData()
        self.herbivores_cells = ProcessData.getHerbivoresData()
        self.carnivores_cells = ProcessData.getCarnivoresData()
        self.humans_cells = ProcessData.getHumansData()
        self.human_effect_cells, self.human_effect_pos = Caculate.caculateHumansEffect(
            self.humans_cells, self.strategy)

        segmentation = ProcessData.getSegmentationData(self.isExtendProtect)
        self.part = Part(
            segmentation[0], segmentation[1], segmentation[2], segmentation[3])
        self.mask = self.grass_cells
        self.timer = 0

        # 效益
        if self.strategy == "normal":
            self.human_cost = 0
        elif self.strategy == "elec":
            self.human_cost = 20000
        else:
            self.human_cost = 50000

    def update_state(self):
        self.grass_cells, self.herbivores_cells, self.carnivores_cells, self.human_cost = Caculate.caculateAll(
            self)
        self.timer += 1

    def visulize(self, cells):
        return np.array([0 if self.mask[i][j] <= 0 else cells[i][j] for i in range(
            cells.shape[0]) for j in range(cells.shape[1])]).reshape(cells.shape)

    def plot_state(self):
        plt.title('Iter :{}'.format(self.timer))
        plt.imshow(self.grass_cells)
        plt.show()

    def update_and_plot(self, n_iter):
        self.month = [i + 1 for i in range(n_iter)]
        self.grass_history = np.zeros(n_iter)
        self.herbivores_history = np.zeros(n_iter)
        self.carnivores_history = np.zeros(n_iter)
        plt.ion()
        for i in range(n_iter):
            self.grass_history[i] = np.sum(self.grass_cells)
            self.herbivores_history[i] = np.sum(self.herbivores_cells)
            self.carnivores_history[i] = np.sum(self.carnivores_cells)
            plt.title('Iter :{}'.format(self.timer))
            plt.subplot(231)
            plt.imshow(self.visulize(self.grass_cells), cmap="Greens")
            plt.subplot(232)
            plt.imshow(self.visulize(self.herbivores_cells), cmap="Blues")
            plt.subplot(233)
            plt.imshow(self.visulize(self.carnivores_cells), cmap="Reds")
            plt.subplot(234)
            plt.plot(self.month, self.grass_history)
            plt.subplot(235)
            plt.plot(self.month, self.herbivores_history)
            plt.subplot(236)
            plt.plot(self.month, self.carnivores_history)

            # plt.imshow(self.humans_cells, cmap="Accent")
            self.update_state()
            plt.pause(0.2)
        plt.ioff()


class ProcessData(object):
    def getGrassData():
        cells = np.array(ProcessData.getStatus(
            "data_map_grass.jpg.txt")).reshape((70, 80))
        for i in range(cells.shape[0]):
            for j in range(cells.shape[1]):
                if cells[i][j] == 5:
                    cells[i][j] = 0
                elif cells[i][j] == 4:
                    cells[i][j] = 0.01*20*0.64
                elif cells[i][j] == 3:
                    cells[i][j] = 0.01*40*0.64
                elif cells[i][j] == 2:
                    cells[i][j] = 0.01*60*0.64
                elif cells[i][j] == 1:
                    cells[i][j] = 0.01*80*0.64
                elif cells[i][j] == 0:
                    cells[i][j] = 0.01*100*0.64
                else:
                    cells[i][j] = 0
        return cells

    def getHerbivoresData():
        cells = np.array(ProcessData.getStatus(
            "data_map_herbivores.jpg.txt")).reshape((70, 80))
        for i in range(cells.shape[0]):
            for j in range(cells.shape[1]):
                if cells[i][j] == 5:
                    cells[i][j] = 0
                elif cells[i][j] == 4:
                    cells[i][j] = 600*0.64/600
                elif cells[i][j] == 3:
                    cells[i][j] = 1000*0.64/600
                elif cells[i][j] == 2:
                    cells[i][j] = 6000*0.64/600
                elif cells[i][j] == 1:
                    cells[i][j] = 20000*0.64/600
                elif cells[i][j] == 0:
                    cells[i][j] = 286430*0.64/600
                else:
                    cells[i][j] = 0
        return cells

    def getCarnivoresData():
        cells = np.array(ProcessData.getStatus(
            "data_map_carnivores.jpg.txt")).reshape((70, 80))
        for i in range(cells.shape[0]):
            for j in range(cells.shape[1]):
                if cells[i][j] == 5:
                    cells[i][j] = 0
                elif cells[i][j] == 4:
                    cells[i][j] = 60*0.64/80
                elif cells[i][j] == 3:
                    cells[i][j] = 100*0.64/80
                elif cells[i][j] == 2:
                    cells[i][j] = 200*0.64/80
                elif cells[i][j] == 1:
                    cells[i][j] = 400*0.64/80
                elif cells[i][j] == 0:
                    cells[i][j] = 1600*0.64/80
                else:
                    cells[i][j] = 0
        return cells

    def getHumansData():
        cells = np.array(ProcessData.getStatus(
            "data_map_human.jpg.txt")).reshape((70, 80))
        for i in range(cells.shape[0]):
            for j in range(cells.shape[1]):
                if cells[i][j] == 7:
                    cells[i][j] = 1
                else:
                    cells[i][j] = 0
        return cells

    def getSegmentationData(isExtendProtect=False):
        national_part = [(40, 0), (25, 20), (50, 60), (65, 50), (40, 0)]
        animal_part = [(25, 20), (13, 32), (38, 67), (50, 60), (25, 20)]
        farm_part = [(13, 32), (0, 50), (35, 70), (38, 67), (13, 32), ]
        national_expand_part = [(40, 0), (20, 25), (45, 65), (65, 50), (40, 0)]
        animal_reduct_part = [(20, 25), (13, 32), (38, 67), (45, 65), (20, 25)]
        migaration_part = [[(50, 20), (40, 20), (40, 30), (50, 30), (50, 20)], [(
            40, 30), (30, 30), (30, 40), (40, 40), (40, 30)], [(50, 40), (40, 40), (40, 50), (50, 50), (50, 40)]]
        if isExtendProtect:
            return national_expand_part, animal_reduct_part, farm_part, migaration_part
        else:
            return national_part, animal_part, farm_part, migaration_part

    def getStatus(path):
        return np.loadtxt(path, delimiter=',')


class Caculate(object):
    k = 0.15  # 0.05-0.2 # the rainfall constant
    # k = 0.1  # 0.05-0.2 # the rainfall constant
    theta = 6  # 周期
    alpha = 0.0002  # 0.00005-0.00025 # 食草动物对草的影响
    fei = 5  # 迁出率
    delta = 5  # 迁入率
    yita = 0.25  # 0.1-0.2草对食草动物的影响
    gama = 0.002  # 0.0005-0.003 # 逻辑斯蒂系数
    omiga = 0.04  # 0.05-0.2 # 食草动物被捕食率
    psi = 0.05  # 0.02-0.025 # 食肉动物自然死亡率
    v = 0.0001  # 0.0001-0.0005 # 食肉动物捕食效率
    w = 0.6  # 草生长系数
    n1 = 0.001  # 食草动物自我竞争影响
    n2 = 0.001  # 食肉动物自我竞争影响
    # human_effect_herbivores = 0
    # human_effect_carnivores = 0
    human_effect_herbivores = -0.05
    human_effect_carnivores = -0.005
    migration_rates = 1
    migration_num = 300
    migration_grass_rates = 0.2
    grass_cost_rate = 0.01
    herbivores_cost_rate = 0.01
    carnivores_cost_rate = 0.01
    grass_protect_rate = 0.01
    herbivores_protect_rate = 0.1
    carnivores_protect_rate = 0.01
    national_protect = 2
    animal_protect = 1
    farm_protect = 0
    t = 0

    def caculateAll(cellular):
        Caculate.t += 1/12
        return Caculate.caculateGrass(cellular.grass_cells, cellular.herbivores_cells, cellular.carnivores_cells, cellular.human_effect_cells, cellular.part
                                      ), Caculate.caculateHerbivores(cellular.grass_cells, cellular.herbivores_cells, cellular.carnivores_cells, cellular.human_effect_cells, cellular.part
                                                                     ), Caculate.caculateCarnivores(cellular.grass_cells, cellular.herbivores_cells, cellular.carnivores_cells, cellular.human_effect_cells, cellular.part
                                                                                                    ), Caculate.caculateHumanCost(cellular.grass_cells, cellular.herbivores_cells, cellular.carnivores_cells, cellular.human_effect_pos, cellular.human_cost)

    def caculateGrass(grass_cells, herbivores_cells, carnivores_cells, human_effect_cells, part):
        grass_neighbor = Caculate.getNeighborNum(grass_cells)
        herbivores_neighbor = Caculate.getNeighborNum(herbivores_cells)

        for i in range(grass_cells.shape[0]):
            for j in range(grass_cells.shape[1]):
                motion = Caculate.k*math.sin(Caculate.theta*Caculate.t)*(grass_cells[i][j]/np.max(grass_cells)) * \
                    grass_neighbor[i][j] - Caculate.alpha * \
                    herbivores_neighbor[i][j] + \
                    Caculate.w * \
                    grass_cells[i][j] + Caculate.getProtectGain(
                        i, j, part, "Grass")*grass_neighbor[i][j] + Caculate.caculateGrassMigration(part)*grass_cells[i][j]

                grass_cells[i][j] = min(max(grass_cells[i][j] + motion, 0), 1)

        return grass_cells

    def caculateHerbivores(grass_cells, herbivores_cells, carnivores_cells, human_effect_cells, part):
        grass_neighbor = Caculate.getNeighborNum(grass_cells)
        herbivores_neighbor = Caculate.getNeighborNum(herbivores_cells)
        carnivores_neighbor = Caculate.getNeighborNum(carnivores_cells)

        for i in range(grass_cells.shape[0]):
            for j in range(grass_cells.shape[1]):
                if herbivores_neighbor[i][j] == 0:
                    index = 1
                else:
                    index = math.exp(max(min(-grass_neighbor[i]
                                             [j]/herbivores_neighbor[i][j], 10), -10))
                motion = Caculate.yita*grass_neighbor[i][j]*herbivores_neighbor[i][j] + Caculate.gama*herbivores_cells[i][j] - \
                    Caculate.omiga * \
                    carnivores_neighbor[i][j]*herbivores_neighbor[i][j] - \
                    Caculate.fei*index + Caculate.delta * \
                    (1-index) + Caculate.human_effect_herbivores * \
                    human_effect_cells[i][j] * herbivores_neighbor[i][j] - \
                    Caculate.n1 * \
                    herbivores_neighbor[i][j]*herbivores_neighbor[i][j] + Caculate.getProtectGain(
                        i, j, part, "Herbivores")*herbivores_neighbor[i][j]
                # + Caculate.caculateMigration(i, j, part)

                # print(Caculate.fei*index + Caculate.delta * (1-index))

                herbivores_cells[i][j] = max(
                    herbivores_cells[i][j] + motion, 0)
        return herbivores_cells

    def caculateCarnivores(grass_cells, herbivores_cells, carnivores_cells, human_effect_cells, part):
        herbivores_neighbor = Caculate.getNeighborNum(herbivores_cells)
        carnivores_neighbor = Caculate.getNeighborNum(carnivores_cells)

        for i in range(grass_cells.shape[0]):
            for j in range(grass_cells.shape[1]):
                motion = -Caculate.psi * \
                    carnivores_neighbor[i][j] + Caculate.v * \
                    herbivores_neighbor[i][j]*carnivores_neighbor[i][j] + \
                    Caculate.human_effect_carnivores * \
                    human_effect_cells[i][j] * carnivores_neighbor[i][j] - \
                    Caculate.n1 * \
                    carnivores_neighbor[i][j]*carnivores_neighbor[i][j] + Caculate.getProtectGain(
                        i, j, part, "Carnivores")*carnivores_neighbor[i][j]
                carnivores_cells[i][j] = max(
                    carnivores_cells[i][j] + motion, 0)

        return carnivores_cells

    def caculateHumansEffect(humans_cells, mode="normal"):
        human_effect_cells = np.zeros(humans_cells.shape)
        for i in range(human_effect_cells.shape[0]):
            for j in range(human_effect_cells.shape[1]):
                for l in range(humans_cells.shape[0]):
                    for r in range(humans_cells.shape[1]):
                        if humans_cells[l][r] == 1:
                            human_effect = Caculate.caculateDistance(
                                i, j, l, r)
                            if human_effect == 0:
                                human_effect_cells[i][j] += 10
                            else:
                                human_effect_cells[i][j] += 1/human_effect
        human_effect_pos = human_effect_cells > np.mean(human_effect_cells)
        if mode == "normal":
            human_effect_cells = human_effect_cells-np.mean(human_effect_cells)
            return human_effect_cells, human_effect_pos
        if mode == "elec":
            human_effect_cells = human_effect_cells-np.mean(human_effect_cells)
            human_effect_cells[human_effect_cells > 0] = 1000
            return human_effect_cells, human_effect_pos
        else:
            human_effect_cells *= 10
            return human_effect_cells, human_effect_pos

    def caculateDistance(i, j, l, r):
        return (i-l)*(i-l)+(j-r)*(j-r)

    def caculateMigration(i, j, part):
        if int((Caculate.t*12) % 12) == 7:
            if Check.isPoiWithinPoly((i, j), part.migaration_part[0]):
                return Caculate.migration_rates*Caculate.migration_num*1.5
        if int((Caculate.t*12) % 12) == 8:
            if Check.isPoiWithinPoly((i, j), part.migaration_part[0]):
                return -Caculate.migration_rates*Caculate.migration_num
            if Check.isPoiWithinPoly((i, j), part.migaration_part[1]):
                return Caculate.migration_rates*Caculate.migration_num*1.5
        if int((Caculate.t*12) % 12) == 11:
            if Check.isPoiWithinPoly((i, j), part.migaration_part[1]):
                return -Caculate.migration_rates*Caculate.migration_num
            if Check.isPoiWithinPoly((i, j), part.migaration_part[2]):
                return Caculate.migration_rates*Caculate.migration_num*1.5
        if int((Caculate.t*12) % 12) == 2:
            if Check.isPoiWithinPoly((i, j), part.migaration_part[2]):
                return -Caculate.migration_rates*Caculate.migration_num
        return 0

    def caculateGrassMigration(part):
        if int((Caculate.t*12) % 12) >= 7 and int((Caculate.t*12) % 12) <= 9:
            return -Caculate.migration_grass_rates
        else:
            return 0

    def caculateHumanCost(grass_cells, herbivores_cells, carnivores_cells, human_effect_pos, human_cost):
        grass_cost = np.sum(grass_cells[human_effect_pos])
        herbivores_cost = np.sum(herbivores_cells[human_effect_pos])
        carnivores_cost = np.sum(carnivores_cells[human_effect_pos])
        return human_cost + Caculate.grass_cost_rate*grass_cost + Caculate.herbivores_cost_rate*herbivores_cost + Caculate.carnivores_cost_rate*carnivores_cost

    def getNeighborNum(cells):
        neighbor = np.zeros(cells.shape)
        for i in range(1, cells.shape[0]-1):
            for j in range(1, cells.shape[1]-1):
                neighbor[i][j] = cells[i-1][j-1] + cells[i-1][j] + cells[i-1][j+1] + \
                    cells[i][j-1] + cells[i][j] + cells[i][j+1] + \
                    cells[i+1][j] + cells[i+1][j+1]
        return neighbor

    def getProtectGain(i, j, part, type):
        if type == "Grass":
            if Check.isPoiWithinPoly((i, j), part.national_part):
                return Caculate.grass_protect_rate * Caculate.national_protect
            if Check.isPoiWithinPoly((i, j), part.animal_part):
                return Caculate.grass_protect_rate * Caculate.animal_protect
            if Check.isPoiWithinPoly((i, j), part.farm_part):
                return Caculate.grass_protect_rate * Caculate.farm_protect
        if type == "Herbivores":
            if Check.isPoiWithinPoly((i, j), part.national_part):
                return Caculate.herbivores_protect_rate * Caculate.national_protect
            if Check.isPoiWithinPoly((i, j), part.animal_part):
                return Caculate.herbivores_protect_rate * Caculate.animal_protect
            if Check.isPoiWithinPoly((i, j), part.farm_part):
                return Caculate.herbivores_protect_rate * Caculate.farm_protect
        if type == "Carnivores":
            if Check.isPoiWithinPoly((i, j), part.national_part):
                return Caculate.carnivores_protect_rate * Caculate.national_protect
            if Check.isPoiWithinPoly((i, j), part.animal_part):
                return Caculate.carnivores_protect_rate * Caculate.animal_protect
            if Check.isPoiWithinPoly((i, j), part.farm_part):
                return Caculate.carnivores_protect_rate * Caculate.farm_protect
        return 0


if __name__ == '__main__':
    game = Cellular()
    print(np.sum(game.grass_cells))
    print(np.sum(game.herbivores_cells))
    print(np.sum(game.carnivores_cells))
    game.update_and_plot(60)
    print(np.sum(game.grass_cells))
    print(np.sum(game.herbivores_cells))
    print(np.sum(game.carnivores_cells))
    print(game.human_cost)
