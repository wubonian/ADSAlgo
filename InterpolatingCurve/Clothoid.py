import numpy as np
from math import cos, sin, pi, sqrt, tan
import matplotlib.pyplot as plt

def clothoid_eval_num(A, x_init, y_init, phi_0, phi_dir, s_e, int_dir, N):
    if int_dir == 1:
        s = np.linspace(0, s_e, N)
    else:
        s = np.linspace(s_e, 0, N)
    dstep = s_e / N
    x_series = [x_init]
    y_series = [y_init]
    phi_series = []
    for i in range(len(s)):
        phi_tmp = phi_0 + phi_dir * (s[i] * s[i]) / (2 * A * A)
        phi_series.append(phi_tmp)
        x_dot = cos(phi_tmp)
        y_dot = sin(phi_tmp)
        if int_dir == 1:
            x_tmp = x_series[i] + dstep * x_dot
            y_tmp = y_series[i] + dstep * y_dot
        else:
            x_tmp = x_series[i] - dstep * x_dot
            y_tmp = y_series[i] - dstep * y_dot
        x_series.append(x_tmp)
        y_series.append(y_tmp)
    return x_series, y_series, phi_series

def main():
    # first example: find clothoid between a point on circle and a straight line
    example = 2
    if example == 1:
        phi_0 = pi/32
        phi_e = pi/2
        c = 1/5
        R = 5
        x_c = 7
        y_c = 10
        N = 10000
        sl = (phi_e - phi_0)*2*R
        print(sl)
        A = sqrt(R * sl)
        xs, ys, phis = clothoid_eval_num(A, x_c+R, y_c, phi_0, 1, sl, 0, N)
        print(xs)
        print(ys)
        print(phis)
        plt.figure(figsize=(5, 5))
        ax = plt.gca()
        ax.set_xlim([-20, 20])
        ax.set_ylim([-20, 20])
        plt.plot(xs, ys, "-b")
        # plot circle
        circle = plt.Circle((x_c, y_c), R, color='r', fill=False)
        ax.add_patch(circle)
        # plot line
        k = tan(phi_0)
        x_l = np.linspace(0, 10, 1000)
        x_l0 = xs[N]
        y_l0 = ys[N]
        y_l = k*(x_l - x_l0) + y_l0
        plt.plot(x_l, y_l, '-g')
        plt.show()
    elif example == 2:
        R = 10
        w = pi/16
        phi_1 = pi/16
        phi_2 = pi/2 - pi/16
        belta = pi - phi_2 + phi_1
        x_v = 6
        y_v = 3
        N = 10000
        # calculate first clothoid
        h0_1 = phi_1
        he_1 = phi_1 + pi/2 - (belta/2 + w/2)
        s1 = 2*R*(he_1 - h0_1)
        A1 = sqrt(R*s1)
        xs1, ys1, phis1 = clothoid_eval_num(A1, 0, 0, 0, 1, s1, 1, N)
        x1_end = xs1[N]
        y1_end = ys1[N]
        l11 = x1_end
        l12 = y1_end/tan(belta/2+w/2)
        l13 = (R+y1_end/sin(belta/2+w/2))/sin(belta/2)*sin(w/2)
        l1 = l11+l12+l13
        x1 = x_v - cos(phi_1)*l1
        y1 = y_v - sin(phi_1)*l1
        xs1_o, ys1_o, phis1_o = clothoid_eval_num(A1, x1, y1, phi_1, 1, s1, 1, N)
        # calculate second clothoid
        x2 = x_v + cos(phi_2)*l1
        y2 = y_v + sin(phi_2)*l1
        xs2_o, ys2_o, phis2_o = clothoid_eval_num(A1, x2, y2, phi_2 + pi, -1, s1, 1, N)
        # calculate line
        ls = np.linspace(-20, 20, 2000)
        xl1 = x_v + ls * cos(phi_1)
        yl1 = y_v + ls * sin(phi_1)
        xl2 = x_v + ls * cos(phi_2)
        yl2 = y_v + ls * sin(phi_2)
        # calculate circle
        phi_c = phi_2 + belta/2
        lc = (R+y1_end/sin(belta/2+w/2))/sin(belta/2)*sin(pi-w/2-belta/2)
        x_c2 = x_v + cos(phi_c) * lc
        y_c2 = y_v + sin(phi_c) * lc
        # plot figure
        plt.figure(figsize=(5, 5))
        ax = plt.gca()
        ax.set_xlim([-20, 20])
        ax.set_ylim([-20, 20])
        plt.plot(xs1_o, ys1_o, '-g')
        plt.plot(xs2_o, ys2_o, '-g')
        plt.plot(xl1, yl1, '-b')
        plt.plot(xl2, yl2, '-b')
        circle = plt.Circle((x_c2, y_c2), R, color='r', fill=False)
        ax.add_patch(circle)
        plt.show()
    elif exmaple == 3:
        



if __name__ == "__main__":
    main()






