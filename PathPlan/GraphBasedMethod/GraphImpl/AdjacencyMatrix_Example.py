class Graph:
    def __init__(self, numvertex):
        self.adjMatrix = [[-1]*numvertex for x in range(numvertex)]
        self.numvertex = numvertex
        # vertices stores logic representation of vertex in a graph
        self.vertices = {}
        # verticesList stores index for vertex in a graph
        self.verticesList = [0]*numvertex

    def set_vertex(self, vtx, id):
        # vtx is the index, and id is logic representation
        if 0 <= vtx <= self.numvertex:
            self.vertices[id] = vtx
            self.verticesList[vtx] = id

    def set_edge(self, frm, to, cost=0):
        frm = self.vertices[frm]
        to = self.vertices[to]
        self.adjMatrix[frm][to] = cost
        self.adjMatrix[to][frm] = cost

    def get_vertex(self):
        return self.verticesList

    def get_edges(self):
        edges = []
        for i in range(self.numvertex):
            for j in range(self.numvertex):
                if (self.adjMatrix[i][j] != -1):
                    edges.append((self.verticesList[i], self.verticesList[j], self.adjMatrix[i][j]))
        return edges

    def get_matrix(self):
        return self.adjMatrix

if __name__ == "__main__":
    G = Graph(6)
    G.set_vertex(0, 'a')
    G.set_vertex(1, 'b')
    G.set_vertex(2, 'c')
    G.set_vertex(3, 'd')
    G.set_vertex(4, 'e')
    G.set_vertex(5, 'f')
    G.set_edge('a', 'e', 10)
    G.set_edge('a', 'c', 20)
    G.set_edge('c', 'b', 30)
    G.set_edge('b', 'e', 40)
    G.set_edge('e', 'd', 50)
    G.set_edge('f', 'e', 60)
    print("Vertices of Graph")
    print(G.get_vertex())
    print("Edges of Graph")
    print(G.get_edges())
    print("Adjacency Matrix of Graph")
    print(G.get_matrix())