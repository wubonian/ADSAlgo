from PathPlan.GraphBasedMethod.GraphImpl.GraphAdjMtrx import GraphAdjMtrx

class Path:
    def __init__(self, start_point, cost=float('inf')):
        self.cost = cost
        self.path = [start_point]


def extract_min(Q, D):
    if len(Q) != 0:
        cost_min = float('inf')
        for i in range(len(Q)):
            index = Q[i]
            cost = D[index].cost
            if cost < cost_min:
                cost_min = cost
                index_out = index
        return index_out
    else:
        return float('inf')


def Dijkstra(G, start_point, end_point):
    Q = [i for i in range(G.graph_size)]
    D = [Path(start_point) for i in range(G.graph_size)]
    D[start_point].cost = 0
    S = []
    l = G.graph_size
    u = start_point
    while l != 0 and u != end_point:
        u = extract_min(Q, D)
        S.append(u)
        Q.remove(u)
        if u != end_point:
            for i in range(G.graph_size):
                if G.graph_matrix[u][i] != -1 and i not in S:
                    tmp_distance = D[u].cost + G.graph_matrix[u][i]
                    if tmp_distance < D[i].cost:
                        D[i].cost = tmp_distance
                        D[i].path = D[u].path[:]
                        D[i].path.append(i)
                        print("start point is {}, ".format(u), end="")
                        print("end point is {}, ".format(i), end="")
                        print("path is {}, ".format(D[i].path))
        l = len(Q)
    print("start point is {}, ".format(start_point), end="")
    print("end point is {}".format(end_point))
    print("path is {}, ".format(D[u].path), end="")
    print("cost is {}".format(D[u].cost))


def main():
    G = GraphAdjMtrx(6)
    G.add_edge(0, 1, 5)
    G.add_edge(0, 2, 10)
    G.add_edge(1, 2, 3)
    G.add_edge(1, 3, 15)
    G.add_edge(1, 4, 4)
    G.add_edge(2, 3, 20)
    G.add_edge(2, 4, 7)
    G.add_edge(3, 4, 10)
    G.add_edge(3, 5, 15)
    G.add_edge(4, 5, 20)
    Dijkstra(G, 0, 5)

if __name__ == "__main__":
    main()