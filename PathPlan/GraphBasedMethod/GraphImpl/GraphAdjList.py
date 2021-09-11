class Node:
    def __init__(self, vertex, cost=0):
        self.vertex = vertex
        self.next = None
        self.cost = cost


class GraphAdjList:
    def __init__(self, graph_size):
        self.graph_size = graph_size
        self.graph = [None] * graph_size

    def add_edge(self, src, dest, cost, direction=0):
        node = Node(dest, cost)
        node.next = self.graph[src]
        self.graph[src] = node
        # direction: 0->bi-direction, 1->direction
        if direction == 0:
            node = Node(src, cost)
            node.next = self.graph[dest]
            self.graph[dest] = node

    def print_graph(self):
        for i in range(self.graph_size):
            print("for node {}, following vertex are connected".format(i))
            temp = self.graph[i]
            while temp:
                print("Vertex is {} ".format(temp.vertex), " Cost is {}".format(temp.cost))
                temp = temp.next


def main():
    G = GraphAdjList(6)
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