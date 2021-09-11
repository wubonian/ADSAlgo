import numpy as np

def dubins_curve(sp, sv, ep, ev, sr, er):
    # calculate norm vector for start and stop speed vector
    sv_norm = sv/np.sqrt(sv[0]**2+sv[1]**2)
    ev_norm = ev/np.sqrt(ev[0]**2+ev[1]**2)
    # calculate circle center for start and stop point
    sc = [sv_norm[1]*sr, sv_norm[0]*sr]
    ec = [ev_norm[1]*er, ev_norm[0]*er]
    srp = [sp[0]+sc[0], sp[1]+sc[1]]
    erp = [ep[0]+ec[0], ep[1]+ec[1]]
    # calculate contact point on circle
    v1 = [erp[0]-srp[0], erp[1]-srp[1]]
    D = np.sqrt(v1[0]**2 + v1[1]**2)
    c = (sr - er)/D
    v1_norm = v1/D
    nx = v1_norm[0]*c - v1_norm[1]*np.sqrt(1-c**2)
    ny = v1_norm[1]*c + v1_norm[0]*np.sqrt(1-c**2)
    n = [nx, ny]
    s_contact = [srp[0]+n[0]*sr, srp[1]+n[1]*sr]
    e_contact = [erp[0]+n[0]*er, erp[1]+n[1]*er]
    # return contact point and circular point
    return s_contact, e_contact, srp, erp

def main():
    sp = [0, 0]
    ep = [10, 0]
    sv = [0, 1]
    ev = [0, -1]
    sr = 3
    er = 3
    s_contact, e_contact, srp, erp = dubins_curve(sp, sv, ep, ev, sr, er)
    print(s_contact, e_contact, srp, erp)

if __name__ == "__main__":
    main()

