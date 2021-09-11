import numpy as np
from math import sin, cos, pi
import matplotlib.pyplot as plt

class EKF_Localization():
    def __init__(self, x, y, phi, v, Pinit):
        self.s_vec = np.array([x, y, phi, v]).T    # state vector is [x, y, phi, v]
        self.dt = 0.001
        self.P = Pinit


    def predict(self, u, Q):
        v = self.s_vec[3]
        phi = self.s_vec[2]
        dt = self.dt
        Jf = np.array([[1, 0, -v*sin(phi)*dt, cos(phi)*dt],
                       [0, 1, v*cos(phi)*dt, sin(phi)*dt],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]])
        F = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0],
                      [0, 0, 1, 0],
                      [0, 0, 0, 0]])
        B = np.array([[cos(phi)*dt, 0],
                      [sin(phi)*dt, 0],
                      [0, dt],
                      [1, 0]])
        s_vec_pred = np.dot(F, self.s_vec) + np.dot(B, u)
        P_pred = np.dot(np.dot(Jf, self.P), Jf.T) + Q
        return s_vec_pred, P_pred

    def update(self, z, s_vec_pred, P_pred, R):
        H = np.array([[1, 0, 0, 0],
                      [0, 1, 0, 0]])
        z_pred = np.dot(H, s_vec_pred)
        Jh = H
        y = z - z_pred
        S = np.dot(np.dot(Jh, P_pred), Jh.T) + R
        K = np.dot(np.dot(P_pred, Jh.T), np.linalg.inv(S))
        self.s_vec = s_vec_pred + np.dot(K, y)
        self.P = np.dot((np.eye(4) - np.dot(K, Jh)), P_pred)

def main():
    Q = np.diag([0.1, 0.1, np.deg2rad(1.0), 1])**2
    Rm = np.diag([1.5, 1.5])**2
    Pinit = np.eye(4)

    ekf = EKF_Localization(0, 0, 0, 5, Pinit)
    timer = 0.0
    v = 10
    w = 0.1
    R = v/w
    x_true = []
    y_true = []
    x_est = []
    y_est = []
    while timer < 10:
        u = np.array([w+np.random.randn()*np.deg2rad(1.0), v+np.random.randn()*1]).T
        theta = w*timer

        x1 = R*sin(theta)
        y1 = R - R*cos(theta)
        z = np.array([x1+np.random.randn()*1.5, y1+np.random.randn()*1.5]).T
        x_true.append(x1)
        y_true.append(y1)
        s_vec_pred, P_pred = ekf.predict(u, Q)
        ekf.update(z, s_vec_pred, P_pred, Rm)
        x2 = ekf.s_vec[0]
        y2 = ekf.s_vec[1]
        x_est.append(x2)
        y_est.append(y2)
        timer = timer + 0.001
    plt.figure()
    plt.plot(x_true, y_true, 'r')
    plt.plot(x_est, y_est, 'b')
    plt.show()

if __name__ == "__main__":
    main()
