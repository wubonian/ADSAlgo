import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

class Point:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.cost = cost
        self.g_cost = float('inf')
        self.priority = float('inf')
        self.next_point = []

class PointIndex:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class GraphAdjMtrx:
    def __init__(self, x, y):
        self.graph_size = x * y
        self.row = x
        self.col = y
        self.graph_matrix = []

    def init_graph(self, normal_cost):
        for i in range(self.row):
            tmp_row = []
            for j in range(self.col):
                tmp_row.append(Point(i, j, normal_cost))
            self.graph_matrix.append(tmp_row)

    def place_obstacle(self, start, end, add_cost):
        for i in range(start.x, end.x):
            for j in range(start.y, end.y):
                self.graph_matrix[i][j].cost = add_cost

class AStar:
    def __init__(self, G, normal_cost):
        self.normal_cost = normal_cost
        self.G = G
        self.start_point = Point(0,0,0)
        self.end_point = Point(0,0,0)
        self.open_set = []
        self.close_set = []

    def calculate_vertex_priority(self, search_point, end_point, vertex, normal_cost, k):
        # calculate heuristic cost using Manhattan Distance
        x_dis_h = abs(end_point.x - vertex.x)
        y_dis_h = abs(end_point.y - vertex.y)
        h_cost = (x_dis_h + y_dis_h) * normal_cost* k
        # calculate greedy cost using Manhattan Distance
        g_cost = search_point.g_cost + vertex.cost
        # calculate final cost
        priority = h_cost + g_cost
        return [g_cost, priority]

    def find_low_cost_point(self, point_list):
        cost_min = float('inf')
        cost_index = 0
        for i in range(len(point_list)):
            temp_cost = point_list[i].priority
            if temp_cost < cost_min:
                cost_index = i
                cost_min = temp_cost
        return cost_index

    def point_compare(self, a, b):
        if a.x == b.x and a.y == b.y:
            return True
        else:
            return False

    def find_path(self, start_point, end_point, k):
        self.start_point = self.G.graph_matrix[start_point.x][start_point.y]
        self.start_point.g_cost = 0
        self.start_point.priority = 0
        self.end_point = self.G.graph_matrix[end_point.x][end_point.y]
        self.open_set = []
        self.close_set = []
        self.open_set = [self.start_point]
        while self.open_set is not []:
            u = self.find_low_cost_point(self.open_set)
            search_point = self.open_set[u]
            if self.point_compare(search_point, self.end_point):
                print("target path is: ")
                print(end_point.x, end_point.y)
                path = [PointIndex(end_point.x, end_point.y)]
                tmp = search_point.next_point
                while tmp != []:
                    path.append(PointIndex(tmp.x, tmp.y))
                    print(tmp.x, tmp.y)
                    tmp = tmp.next_point
                return path
                break
            else:
                self.close_set.append(search_point)
                self.open_set.remove(search_point)
                for i in [search_point.x-1, search_point.x, search_point.x+1]:
                    for j in [search_point.y-1, search_point.y, search_point.y+1]:
                        if 0 <= j < self.G.col and 0 <= i < self.G.row and not point_in_list(self.G.graph_matrix[i][j], self.close_set):
                            adj_point = self.G.graph_matrix[i][j]
                            if not point_in_list(adj_point, self.open_set):
                                self.open_set.append(adj_point)
                            [g_cost, priority] = self.calculate_vertex_priority(search_point, self.end_point, adj_point, self.normal_cost, k)
                            if priority < adj_point.priority:
                                adj_point.next_point = search_point
                                adj_point.g_cost = g_cost
                                adj_point.priority = priority

def point_in_list(point, point_list):
    x = False
    for p in point_list:
        if point.x == p.x and point.y == p.y:
            x = True
    return x

def print_solution(G, normal_cost, path):
    plt.figure(figsize = (5, 5))
    ax = plt.gca()
    ax.set_xlim([0, G.row])
    ax.set_ylim([0, G.col])
    for i in range(G.row):
        for j in range(G.col):
            tmp = PointIndex(i, j)
            if point_in_list(tmp, path):
                rec = Rectangle((i, j), width=1, height=1, color='r')
            elif G.graph_matrix[i][j].priority != float('inf'):
                rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='b')
            elif G.graph_matrix[i][j].cost == normal_cost:
                rec = Rectangle((i, j), width=1, height=1, edgecolor='gray', facecolor='w')
            else:
                rec = Rectangle((i, j), width=1, height=1, color='gray')
            ax.add_patch(rec)
    plt.axis('equal')
    plt.axis('off')
    plt.tight_layout()
    plt.show()
    plt.draw()

def main():
    normal_cost = 1
    G = GraphAdjMtrx(100, 50)
    G.init_graph(normal_cost)
    obstacle_start = PointIndex(10, 10)
    obstacle_end = PointIndex(20, 40)
    G.place_obstacle(obstacle_start, obstacle_end, 10000)
    Algo = AStar(G, normal_cost)
    start_point = PointIndex(0, 0)
    end_point = PointIndex(30, 25)
    path = Algo.find_path(start_point, end_point, 1)
    print_solution(G, normal_cost, path)

if __name__ == '__main__':
    main()