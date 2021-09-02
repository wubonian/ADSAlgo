import numpy as np
import matplotlib.pyplot as plt

class cubic_spline:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.n = len(x)
        self.a = []
        self.b = []
        self.c = []
        self.d = []
        self.d_mtx = []

    def calc_d_mtx(self):
        A = np.zeros((self.n, self.n))
        for i in range(self.n):
            if i == 0:
                A[i][i] = 2
                A[i][i+1] = 1
            elif i == self.n - 1:
                A[i][i] = 2
                A[i-1][i] = 1
            else:
                A[i-1][i] = 1
                A[i][i] = 2
                A[i][i+1] = 1
        Y = np.zeros((self.n, 1))
        for i in range(self.n):
            if i == 0:
                Y[i] = 3*(self.y[i+1] - self.y[0])
            elif i == self.n-1:
                Y[i] = 3*(self.y[i] - self.y[i-1])
            else:
                Y[i] = 3*(self.y[i+1] - self.y[i-1])
        IA = np.linalg.inv(A)
        self.d_mtx = np.dot(IA, Y)

    def calc_coef(self):
        for i in range(self.n-1):
            self.a.append(self.y[i])
            self.b.append(self.d_mtx[i])
            c_tmp = 3*(self.y[i+1] - self.y[i]) - 2*self.d_mtx[i] - self.d_mtx[i+1]
            self.c.append(c_tmp)
            d_tmp = 2*(self.y[i] - self.y[i+1]) + self.d_mtx[i] + self.d_mtx[i+1]
            self.d.append(d_tmp)

    def find_index(self, u):
        i = 0
        while self.x[i] < u:
            i = i+1
        if u > self.x[0]:
            return i - 1
        else:
            return 0

    def calc_prop(self, i, u):
        return (u - self.x[i]) / (self.x[i+1] - self.x[i])

    def eval_val(self, u):
        i = self.find_index(u)
        p = self.calc_prop(i, u)
        y = self.a[i] + self.b[i]*p + self.c[i]*p*p + self.d[i]*p*p*p
        return y


def main():
    x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    y = [2, 3, 5, 4, 8, 9, 4, 2, 3, 5, 7]
    cubic = cubic_spline(x, y)
    cubic.calc_d_mtx()
    cubic.calc_coef()

    xs = np.linspace(0, 10, 1000)
    ys = []
    for x_tmp in xs:
        y_tmp = cubic.eval_val(x_tmp)
        ys.append(y_tmp)

    plt.figure(figsize=(5, 5))
    ax = plt.gca()
    ax.set_xlim([-5, 20])
    ax.set_ylim([-5, 20])
    plt.plot(x, y, '-g')
    plt.plot(xs, ys, '-y')
    plt.show()

if __name__ == "__main__":
    main()