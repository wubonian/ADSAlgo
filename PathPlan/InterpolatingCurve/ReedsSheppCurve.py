import numpy as np
from math import sin, cos, atan, pi

def reeds_shepp_curve(x, y, phi):
    # only LpSpRp pattern is implemented here
    # 1st, calculate circular center of start and stop
    center_start = [0, 1]
    center_end = [x+sin(phi)*1, y-cos(phi)*1]
    # 2nd, calculate heading angle of line between two circular center
    v = [center_end[0]-center_start[0], center_end[1]-center_start[1]]
    theta = atan(v[1]/v[0])
    # 3nd, calculate intersection angle between tangent line and center line
    dis = np.sqrt(v[0]**2 + v[1]**2)
    alpha = atan(2/dis)
    # 4th, calculate angle between start point and tangent point
    t1 = alpha + theta
    t2 = alpha - phi
    return t1, t2

