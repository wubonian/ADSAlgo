import numpy as np
from math import cos, sin, pi, radians, sqrt, atan
from scipy.special import fresnel
import matplotlib.pyplot as plt

def clothoid_eval(s, distance, x0, y0, h0, c_start, c_end):
    r_c = 1/(c_end - c_start)
    alpha = 1 / sqrt(abs(2*r_c*distance))
    s_dot = s * alpha * sqrt(2/pi)
    dy_c0, dx_c0 = fresnel(s_dot)
    dx_c = dx_c0 / alpha
    dy_c = dy_c0 / alpha
    dx = dx_c * cos(h0) - dy_c * sin(h0)
    dy = dx_c * sin(h0) + dy_c * cos(h0)
    x = x0 + dx
    y = y0 + dy
    return x, y

def clothoid_length(c_delta, h_delta):
    R = 1 / c_delta
    dist = 2 * R * h_delta
    return dist

def main():
    h_e = atan(0.1)
    h_s = 0
    x0 = 5
    y0 = 6
    c_s = 0
    c_e = 1
    c_delta = c_e - c_s
    h_delta = h_e - h_s
    dist = clothoid_length(c_delta, h_delta)
    print(dist)
    s_array = np.linspace(0, dist, 100)
    x_array = []
    y_array = []
    for s in s_array:
        x, y = clothoid_eval(s, dist, x0, y0, h_s, c_s, c_e)
        x_array.append(x)
        y_array.append(y)
    print(x_array, y_array)
    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(1, 1, 1)
    circ = plt.Circle((5, 5), radius=1, color='g', fill=False)
    ax.add_patch(circ)
    x = np.linspace(-10, 10, 200)
    y = 9.5 + 0.1 * x
    ax.plot(x, y)
    ax.plot(x_array, y_array)
    # ax.plot(xs, ys)
    plt.xlim((-10, 10))
    plt.ylim((-10, 10))
    plt.show()

if __name__ == "__main__":
    main()