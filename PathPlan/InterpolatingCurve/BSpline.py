import numpy as np
import matplotlib.pyplot as plt

def b_spline_basis(i, k, n, um, u, uf):
    m = len(um)
    y = float('inf')
    if k == 0:
        if um[i] <= u <= um[i+1]:
            y = 1
        else:
            y = 0
    else:
        if um[i+k] - um[i] == 0 or um[i+k+1] - um[i+1] == 0:
            y = 1
        elif um[k] <= u <= um[n+1]:
            y1 = b_spline_basis(i, k-1, n, um, u, uf)
            y2 = b_spline_basis(i+1, k-1, n, um, u, uf)
            # print("y1 ", i, k-1, n, um, u)
            # print("y2 ", i+1, k-1, n, um, u)
            y = (u - um[i]) / (um[i+k] - um[i]) * y1 + (um[i+k+1] - u)/(um[i+k+1] - um[i+1]) * y2
        else:
            y = 0
    return y

def b_spline(ctrl_pts, k, um, u, uf):
    n = len(ctrl_pts) - 1
    y = 0
    for i in range(n+1):
        y = y + b_spline_basis(i, k, n, um, u, uf) * ctrl_pts[i]
    return y

def b_spline_uniform(ctrl_pts, k):
    n = len(ctrl_pts) - 1
    m = len(ctrl_pts) + k + 1
    um = np.linspace(0, 1, m)
    us = np.linspace(0, 1, 3000)
    y = []
    for u in us:
        if um[k] <= u <= um[n+1]:
            y_tmp = b_spline(ctrl_pts, k, um, u, True)
            y.append(y_tmp)
    return y

def b_spline_clamped(ctrl_pts, k):
    # there is error to be fixed
    n = len(ctrl_pts) - 1
    m = len(ctrl_pts) + k + 1
    # um = np.linspace(0, 1, n-k+2)
    um = [0, 0.0001, 0.0002, 0.0003, 1/7, 2/7, 3/7, 4/7, 5/7, 6/7, 0.9997, 0.9998, 0.9999, 1]
    # for i in range(k):
    #     um = np.insert(um, 0, 0)
    #     um = np.append(um, 1)
    us = np.linspace(0, 1, 3000)
    y = []
    for u in us:
        if um[k] <= u <= um[n + 1]:
            y_tmp = b_spline(ctrl_pts, k, um, u, False)
            y.append(y_tmp)
    return y

def main():
    ctrl_pts_x = [1, 2, 4, 6, 8, 10, 14, 16, 17, 19]
    ctrl_pts_y = [0, 10, 5, 7, 3, 4, 5, 7, 10, 9]
    k = 3
    x = b_spline_clamped(ctrl_pts_x, k)
    y = b_spline_clamped(ctrl_pts_y, k)


    plt.figure(figsize=(5, 5))
    ax = plt.gca()
    ax.set_xlim([-20, 20])
    ax.set_ylim([-20, 20])
    plt.plot(ctrl_pts_x, ctrl_pts_y, '-g')
    plt.plot(x, y, '-y')
    plt.show()

if __name__ == "__main__":
    main()