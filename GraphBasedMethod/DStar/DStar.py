import math

class Point:
    def __init__(self, x, y, cost):
        self.x = x
        self.y = y
        self.h = float('inf')
        self.k = float('inf')
        self.cost = cost
        self.parent = None
        self.t = "new"
        self.state = "."

class Map:
    def __init__(self, row, col, cost):
        self.row = row
        self.col = col
        self.map = self.init_map(cost)

    def init_map(self, cost):
        tmp_map = []
        for i in range(self.row):
            tmp_row = []
            for j in range(self.col):
                tmp_row.append(Point(i, j, cost))
            tmp_map.append(tmp_row)
        return tmp_map

    def get_neighbour(self, p):
        neighbour_list = []
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                # print(p.x, p.y)
                i_index = p.x + i
                j_index = p.y + j
                # print(p.x + i, p.y + j)
                if 0 <= i_index < self.row and 0 <= j_index < self.col:
                    neighbour_list.append(self.map[i_index][j_index])
                    # print("neighbour point:")
                    # print("x is {};".format(self.map[i_index][j_index].x), "y is {}".format(self.map[i_index][j_index].y), end="")
                    # print("")
        return neighbour_list

    def calculate_cost(self, s, e):
        x_dlt = e.x - s.x
        y_dlt = e.y - s.y
        c = math.sqrt(x_dlt * x_dlt + y_dlt * y_dlt) * e.cost
        return c

    def place_obstacle(self, point_list, cost_list):
        for i in range(len(point_list)):
            (x, y) = point_list[i]
            if 0 <= x < self.row and 0 <= y < self.col:
                self.map[x][y].cost = cost_list[i]
                self.map[x][y].h = cost_list[i]
                self.map[x][y].state = "#"

    def print_map(self):
        for i in range(self.row):
            for j in range(self.col):
                print("{} ".format(self.map[i][j].state), end="")
            print("")

    def print_map_state(self):
        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j].t == "new":
                    print("x ", end="")
                elif self.map[i][j].t == "open":
                    print("* ", end="")
                elif self.map[i][j].t == "close":
                    print("+ ", end="")
            print("")



class DStar:
    def __init__(self, map):
        self.map = map
        self.open_list = []

    def process_state(self):
        x = self.min_state()
        # print("main point")
        # print("x is {};".format(x.x), "y is {}".format(x.y), end="")
        # print("")
        if x is None:
            return -1
        k_old = self.get_min()
        self.delete(x)
        if k_old < x.h:
            neighbours = self.map.get_neighbour(x)
            for n in neighbours:
                h_tmp = n.h + self.map.calculate_cost(n, x)
                if n.h <= k_old and h_tmp < x.h:
                    x.parent = n
                    x.h = h_tmp
        if k_old == x.h:
            neighbours = self.map.get_neighbour(x)
            for n in neighbours:
                h_tmp = x.h + self.map.calculate_cost(x, n)
                if n.t == "new" or (n.parent == x and n.h != h_tmp) or (n.parent != x and n.h > h_tmp):
                    n.parent = x
                    self.insert(n, h_tmp)
        else:
            neighbours = self.map.get_neighbour(x)
            for n in neighbours:
                h_tmp = x.h + self.map.calculate_cost(x, n)
                if n.t == "new" or (n.parent == x and n.h != h_tmp):
                    n.parent = x
                    self.insert(n, h_tmp)
                else:
                    if n.parent != x and n.h > h_tmp:
                        self.insert(x, x.h)
                    else:
                        h_tmp2 = n.h + self.map.calculate_cost(n, x)
                        if n.parent != x and x.h > h_tmp2 and n.t == "close" and n.h > k_old:
                            self.insert(n, h_tmp2)
        return self.get_min()

    def modify_cost(self, p, h_new):
        if p.t == "close":
            self.insert(p, h_new)

    def min_state(self):
        state = min(self.open_list, key=lambda x: x.k)
        return state

    def get_min(self):
        k_val = min([x.k for x in self.open_list])
        return k_val

    def delete(self, p):
        p.t = "close"
        self.open_list.remove(p)

    def insert(self, p, h):
        if p.t == "new":
            p.k = h
        elif p.t == "open":
            p.k = min(p.k, h)
        elif p.t == "close":
            p.k = min(p.h, h)
        p.h = h
        p.t = "open"
        if p not in self.open_list:
            self.open_list.append(p)

    def init_algo(self, start, end):
        self.insert(end, 0)
        while True:
            self.process_state()
            if start.t == "close":
                break
        self.plot_path(start, end)

    def plot_path(self, start, end):
        s = start
        s.state = "+"
        while s != end:
            s = s.parent
            s.state = "+"

    def reset_state(self):
        for i in range(self.map.row):
            for j in range(self.map.col):
                if self.map.map[i][j].state is not "#":
                    self.map.map[i][j].state = "."

    def update_algo(self, current_location, start, end):
        tmp_s = current_location
        while tmp_s != end:
            if tmp_s.parent.state == "#":
                print(tmp_s.parent.h + self.map.calculate_cost(tmp_s, tmp_s.parent))
                self.modify_cost(tmp_s, tmp_s.parent.h + self.map.calculate_cost(tmp_s, tmp_s.parent))
                print(tmp_s.t)
                print(tmp_s.x, tmp_s.y)
                while True:
                    k_min = self.process_state()
                    if tmp_s.h <= k_min:
                        break
            tmp_s = tmp_s.parent
            print(tmp_s.x, tmp_s.y)
        self.plot_path(current_location, end)

def main():
    m = Map(20, 20, 1)
    d_star = DStar(m)
    start_point = m.map[3][3]
    end_point = m.map[18][15]

    d_star.init_algo(start_point, end_point)

    m.print_map()

    obs_list = [(i, 12) for i in range(2, 17)]
    cost_list = [float('inf')] * 15
    m.place_obstacle(obs_list, cost_list)
    d_star.reset_state()

    current_location = m.map[7][7]
    d_star.update_algo(current_location, start_point, end_point)
    m.print_map()

if __name__ == "__main__":
    main()