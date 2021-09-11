from random import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections as mc
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GraphList:
    def __init__(self, left_corner, right_corner):
        self.left_corner = left_corner
        self.right_corner = right_corner
        self.vertices = []
        self.edge = []
        self.vex2idx = {}
        self.neighbour = {}
        self.distance = {}

    def gen_rand_point(self):
        fac_x = random()
        fac_y = random()
        p_x = self.left_corner.x + (self.right_corner.x - self.left_corner.x) * fac_x
        p_y = self.left_corner.y + (self.right_corner.y - self.left_corner.y) * fac_y
        p = Point(p_x, p_y)
        return p

    def check_point_collide(self, p):
        return False

    def check_line_collide(self, s, e):
        return False

    def add_vertex(self, p):
        try:
            idx = self.vex2idx[p]
        except:
            idx = len(self.vertices)
            self.vertices.append(p)
            self.vex2idx[p] = idx
            self.neighbour[idx] = []
        return idx

    def add_connection(self, s_idx, e_idx, d):
        self.edge.append((s_idx, e_idx))
        self.neighbour[s_idx].append((e_idx, d))
        self.neighbour[e_idx].append((s_idx, d))

    def calculate_distance(self, s, e):
        x_len = abs(e.x - s.x)
        y_len = abs(e.y - s.y)
        dis = np.sqrt(x_len * x_len + y_len * y_len)
        return dis

    def check_nearby_pointlist(self, p, r):
        p_list = []
        for v in self.vertices:
            dis = self.calculate_distance(v, p)
            if ~self.check_line_collide(v, p) and 0 < dis < r:
                p_list.append(v)
        return p_list


class PRM:
    def __init__(self, G, num, r0):
        self.G = G
        self.num = num
        self.r0 = r0

    def process(self):
        itr = 1
        while itr <= self.num:
            # generate new random point
            p_rand = self.G.gen_rand_point()
            # if new random point collide with obstacle, discard the point
            if self.G.check_point_collide(p_rand):
                continue
            rand_idx = self.G.add_vertex(p_rand)
            # calculate dynamic bounding radius
            r = self.r0 #* pow(np.log(itr)/itr, 1/2)
            # update connection with nearby point within certain range
            if len(self.G.vertices) > 1:
                nrby_list = self.G.check_nearby_pointlist(p_rand, r)
                if nrby_list is not []:
                    for nrby_p in nrby_list:
                        nrby_idx = self.G.vex2idx[nrby_p]
                        dis = self.G.calculate_distance(nrby_p, p_rand)
                        self.G.add_connection(nrby_idx, rand_idx, dis)
            itr = itr + 1

def main():
    left_corner = Point(0, 0)
    right_corner = Point(10, 10)
    G = GraphList(left_corner, right_corner)
    prm = PRM(G, 900, 1)
    prm.process()

    fig, ax = plt.subplots()
    for v in G.vertices:
        ax.scatter(v.x, v.y, c='cyan')
    lines = []
    for edge in G.edge:
        idx1 = edge[0]
        idx2 = edge[1]
        p1 = (G.vertices[idx1].x, G.vertices[idx1].y)
        p2 = (G.vertices[idx2].x, G.vertices[idx2].y)
        line_tmp = (p1, p2)
        lines.append(line_tmp)
    lc = mc.LineCollection(lines, colors='green', linewidths=2)
    ax.add_collection(lc)
    plt.show()

if __name__ == "__main__":
    main()





