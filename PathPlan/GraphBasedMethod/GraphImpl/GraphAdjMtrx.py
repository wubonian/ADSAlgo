class GraphAdjMtrx:
    def __init__(self, graph_size):
        self.graph_size = graph_size
        self.graph_matrix = [[-1]*graph_size for x in range(self.graph_size)]
        self.vertex = [0]*graph_size

    def add_edge(self, src, dest, cost, direction=0):
        self.graph_matrix[src][dest] = cost
        if direction == 0:
            self.graph_matrix[dest][src] = cost

    def print_graph(self):
        for i in range(self.graph_size):
            print("For node {}, connected vertex are:\n".format(i), end="")
            for j in range(self.graph_size):
                if self.graph_matrix[i][j] != -1:
                    print("Node {}".format(j), " cost {}; ".format(self.graph_matrix[i][j]), end="")
            print("\n", end="")

        


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
    G.print_graph()


if __name__ == "__main__":
    main()