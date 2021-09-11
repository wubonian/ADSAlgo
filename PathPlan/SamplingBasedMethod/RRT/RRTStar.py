from random import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import collections as mc
from collections import deque

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GraphList:
    def __init__(self, corner_p_1, corner_p_2):
        self.left_corner = corner_p_1
        self.right_corner = corner_p_2

        self.vertices = []
        self.edges = []

        self.vex2idx = {}
        self.neighbour = {0:[]}
        self.distance = {0:0.}

        self.len = abs(corner_p_2.x - corner_p_1.x)
        self.wid = abs(corner_p_2.y - corner_p_1.y)

    def gen_random_point(self):
        rx = random()
        ry = random()

        pos_x = self.left_corner.x + rx * self.len
        pos_y = self.left_corner.y + ry * self.wid

        p = Point(pos_x, pos_y)

        return p

    def add_vertex(self, p):
        try:
            idx = self.vex2idx[p]
        except:
            idx = len(self.vertices)
            self.vertices.append(p)
            self.vex2idx[p] = idx
            self.neighbour[idx] = []
        return idx

    def add_edge(self, idx_strt, idx_end, distance):
        self.edges.append((idx_strt, idx_end))
        self.neighbour[idx_strt].append((idx_end, distance))
        self.neighbour[idx_end].append((idx_strt, distance))

    def is_in_graph(self, p):
        in_range = False
        if self.left_corner.x <= p.x <= self.right_corner.x and self.left_corner.y <= p.y <= self.right_corner.y:
            in_range = True
        return in_range

    def is_within_obstacle(self, p):
        return False

    def is_through_obstacle(self, s, e):
        return False

    def find_nearest_point(self, p):
        n_vex = None
        n_idx = None
        min_dis = float('inf')
        for idx, v in enumerate(self.vertices):
            dis = self.calculate_distance(p, v)
            if dis < min_dis:
                n_vex = v
                n_idx = idx
                min_dis = dis
        return n_idx, n_vex, min_dis

    def calculate_distance(self, s, e):
        x_len = abs(e.x - s.x)
        y_len = abs(e.y - s.y)
        dis = np.sqrt(x_len * x_len + y_len * y_len)
        return dis

    def create_point_setDis(self, s, e, step):
        len = self.calculate_distance(s, e)
        factor = step/len
        vec_x = s.x + (e.x - s.x) * factor
        vec_y = s.y + (e.y - s.y) * factor
        vec = Point(vec_x, vec_y)
        return vec


class RRT:
    def __init__(self, init_pos, end_pos, vertex_num, delta_q, G, star):
        self.init_pos = init_pos
        self.end_pos = end_pos
        self.num = vertex_num
        self.delta_q = delta_q
        self.G = G
        self.star = star

    def process(self):
        # initialize the graph
        self.G.add_vertex(self.init_pos)
        # self.G.add_vertex(self.end_pos)
        itr = 0
        while itr <= self.num:
            # generate random position
            new_pos = self.G.gen_random_point()
            # check if new point is in obstacle, otherwise gen a new random point
            if self.G.is_within_obstacle(new_pos):
                continue
            # find nearest point, and create new vertex; if nearest point is not found, continue to generate new random point
            near_idx, v_near, dis = self.G.find_nearest_point(new_pos)
            if v_near is None:
                continue
            # create the point to be added into vertices list
            if dis < self.delta_q:
                v_add = new_pos
                dis_add = dis
            else:
                v_add = self.G.create_point_setDis(v_near, new_pos, self.delta_q)
                dis_add = self.delta_q
            # add the new point into vertices list, if use RRT*, update distance
            add_idx = self.G.add_vertex(v_add)
            self.G.add_edge(near_idx, add_idx, dis_add)
            if self.star == 1:
                self.G.distance[add_idx] = self.G.distance[near_idx] + dis_add
            # update nearby vertices distance
            if self.star == 1:
                for vec in self.G.vertices:
                    # continue if they are same vertex
                    if vec == v_add:
                        continue
                    dist_nrby = self.G.calculate_distance(vec, v_add)
                    # continue if distance is too far away
                    if dist_nrby > 1.5 * self.delta_q:
                        continue
                    # check if it is ok to update the distance and add new edge between two point
                    nrby_idx = self.G.vex2idx[vec]
                    if self.G.distance[nrby_idx] > self.G.distance[add_idx] + dist_nrby:
                        self.G.add_edge(nrby_idx, add_idx, dist_nrby)
                        self.G.distance[nrby_idx] = self.G.distance[add_idx] + dist_nrby
            # check if new point can be connected to end point
            if self.G.is_through_obstacle(v_add, self.end_pos):
                continue
            dis_end = self.G.calculate_distance(v_add, self.end_pos)
            if dis_end < 2 * self.delta_q:
                end_idx = self.G.add_vertex(self.end_pos)
                self.G.add_edge(add_idx, end_idx, dis_end)
                if self.star == 1:
                    try:
                        self.G.distance[end_idx] = min(self.G.distance[end_idx], self.G.distance[add_idx] + dis_end)
                    except:
                        self.G.distance[end_idx] = self.G.distance[add_idx] + dis_end
            itr = itr + 1

def main():
    left_corner = Point(0, 0)
    right_corner = Point(100, 100)
    G = GraphList(left_corner, right_corner)
    start_point = Point(10,3)
    end_point = Point(50.7, 90.4)
    rrt = RRT(start_point, end_point, 300, 10, G, 1)
    rrt.process()
    fig, ax = plt.subplots()
    for v in G.vertices:
        ax.scatter(v.x, v.y, c='cyan')
    ax.scatter(start_point.x, start_point.y, c='black')
    ax.scatter(end_point.x, end_point.y, c='black')
    lines = []
    for edge in G.edges:
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

