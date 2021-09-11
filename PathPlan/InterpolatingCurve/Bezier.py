import numpy as np
import matplotlib.pyplot as plt
from math import pi, factorial

def bezier_evaluation(N, ctrl_pts, u):
    rtn = [0, 0]
    for i in range(N+1):
        rtn_x = (factorial(N) / factorial(i) / factorial(N - i)) * pow(u, i) * pow(1 - u, N - i) * ctrl_pts[i][0]
        rtn_y = (factorial(N) / factorial(i) / factorial(N - i)) * pow(u, i) * pow(1 - u, N - i) * ctrl_pts[i][1]
        print(rtn_x)
        rtn[0] = rtn[0] + rtn_x
        rtn[1] = rtn[1] + rtn_y
    return rtn

def main():
    ctrl_pts = [[0, 0], [1, 1], [3, 1], [4, 0]]
    N = 3
    p = np.linspace(0, 1, 100)
    x = []
    y = []
    for u in p:
        point = bezier_evaluation(N, ctrl_pts, u)
        print(point)
        x.append(point[0])
        y.append(point[1])
    plt.figure(figsize=(5, 5))
    ax = plt.gca()
    ax.set_xlim([-20, 20])
    ax.set_ylim([-20, 20])
    plt.plot(x, y, '-g')
    plt.show()

if __name__ == "__main__":
    main()