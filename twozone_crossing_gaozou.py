"""
Two-zone crossing-geometry gamma-gamma constraint on the GeV-zone Lorentz
factor of GRB 210704A, computed with the ORIGINAL code of Gao & Zou (2023),
ApJL 956, L38 (https://github.com/qilunuo9/two-zone_model), adapted here.

The physics functions (theta, R_max, n_Mev, E_Mmin, beta-hat, sigma, the
optical-depth integrals iyx0/iyx3, the Doppler-weighted angle average yy,
and the bisection gamma_min) are transcribed verbatim from that repository;
only the input block is changed for GRB 210704A. The transcription is
validated below against Table 1 of Gao & Zou (2023) for GRB 221009A
(reproduces 297.7/161.7/139.4/113.0 vs the published 297.92/162.93/139.31/
113.06 at t_T = 5/10/15/20 s).

Model for GRB 210704A: the GeV photons come from an OUTER internal shock
(not the external shock of Gao & Zou 2023), so the GeV emission time is the
millisecond variability time (t_G ~ 1 ms) and R_G = 2 Gamma_G^2 c t_G/(1+z)
stays at ~1e12 cm -- co-spatial with the deuterium. The MeV photons come
from an inner internal shock and are described by a Band function; the
16 GeV photon's pair-production threshold sits above E_P, so beta_M = 2.80
is the relevant index.

RESULT (t_G = 1 ms): Gamma_G,min = 234 / 318 / 434 for the 1.21 / 4.39 /
16 GeV photons (R_G = 1.0 / 1.8 / 3.4 e12 cm). Gamma_G ~ 300-430 maps the
gap centre (0.9 GeV) to a comoving 3.5-5.0 MeV -- the deuterium
photodissociation resonance -- so the two-zone escape of the GeV photons
and the resonant deuterium absorption are mutually consistent.
"""

import numpy as np
from scipy import integrate

m_e = 9.1093837e-28
c = 29979245800.0
sigma_T = 6.652448e-25
ev_to_erg = 1.60217662e-12


# ---- verbatim from Gao & Zou (2023), github.com/qilunuo9/two-zone_model ----
def theta(R, theta_M, theta_G, phi):
    dx_M = R_M * np.sin(theta_M)
    dx_G = R_G * np.sin(theta_G)
    dx = np.sqrt(dx_M ** 2 + dx_G ** 2 - 2. * dx_M * dx_G * np.cos(phi))
    dy = R_G * np.cos(theta_G) - R_M * np.cos(theta_M) + R - R_G
    thetam = np.arctan(dx / dy)
    return 0.01 if thetam > 0.01 else thetam


def R_max(theta_G):
    if (1 - 2 * c * T_90 / ((1 + z) * theta_G ** 2 * R_G)) > 0:
        return R_G / (1 - 2 * c * T_90 / ((1 + z) * theta_G ** 2 * R_G))
    return R_G * 1e3


def L_M(theta_G, R):
    t_R = T_REF + (1 + z) * T_G - (1 + z) * theta_G ** 2 * R_G / 2 / c * (R_G / R)
    if t_R < t[0] or t_R > t[-1]:
        return 0, 1, 3, 1
    for index in range(len(t)):
        if t_R < t[index]:
            break
    return L[index], alphaM[index], betaM[index], EP[index]


def n_Mev(theta_G, R, E_Ma):
    L_MR, alpha_M, beta_M, E_P = L_M(theta_G, R)
    n0 = L_MR / ((1 + z) * E_P ** 2
                 * (1 / (2 - alpha_M) + 1 / (beta_M - 2)
                    * (1 - E_P ** (beta_M - 2) * E_maxo ** (2 - beta_M)))
                 * 4. * np.pi * R ** 2 * c)
    result = np.array([])
    for E_M in E_Ma:
        if E_M < E_P:
            result = np.append(result, n0 * (E_M / E_P) ** (-alpha_M))
        elif E_M < E_max:
            result = np.append(result, n0 * (E_M / E_P) ** (-beta_M))
        else:
            result = np.append(result, 0)
    return result


def E_Mmin(th):
    return 2 * (m_e * c ** 2) ** 2 / (1 + z) ** 2 / (1 - np.cos(th)) / E_G


def beta(E_M, th):
    return np.sqrt(np.abs(1 - 2.0 * (m_e * c ** 2 / (1 + z)) ** 2
                          / E_M / E_G / (1 - np.cos(th))))


def sigma(b):
    return 3. / 16. * sigma_T * (1. - b ** 2) * (
        (3. - b ** 4) * np.log((1. + b) / (1. - b)) - 2. * b * (2. - b ** 2))


def y0(theta_G, E_M, phi, theta_M, R):
    th0 = theta(R, theta_M, theta_G, phi)
    return n_Mev(theta_G, R, E_M) * sigma(beta(E_M, th0)) * (1 - np.cos(th0))


def iyx0(theta_G, x1, x2, x3):
    th0 = theta(x3, x2, theta_G, 0)
    Em0 = E_Mmin(th0)
    if Em0 > E_max:
        return 0
    x0 = np.logspace(np.log10(Em0), np.log10(E_max), 101)
    return integrate.simpson(y0(theta_G, x0, x1, x2, x3), x=x0)


def iyx3(theta_G, x3min, x3max):
    x3 = np.logspace(np.log10(x3min), np.log10(x3max), 51)
    arr = np.array([iyx0(theta_G, 0, 0.01, x) for x in x3])
    return integrate.simpson(arr, x=x3)


def yy(theta_Gmax):
    tGa = np.logspace(-4, np.log10(theta_Gmax), 30)
    num = np.array([])
    den = np.array([])
    for tGx in tGa:
        D = 1 / (Gamma_G * (1 - beta_Gb * np.cos(tGx)))
        tua = iyx3(tGx, R_G, R_max(tGx))
        num = np.append(num, D ** (3 + beta_G) * np.exp(-tua) * tGx)
        den = np.append(den, D ** (3 + beta_G) * tGx)
    return integrate.simpson(num, x=tGa) / integrate.simpson(den, x=tGa)


def gamma_min(t_G):
    global Gamma_G, R_G, beta_Gb, T_G
    T_G = t_G / (1 + z)
    lo, hi = 0.1, 2000.
    for _ in range(40):
        Gamma_G = (lo + hi) / 2.
        R_G = 2 * Gamma_G * Gamma_G * c * T_G * eta
        beta_Gb = np.sqrt(1 - 1 / Gamma_G ** 2)
        tua_e = -np.log(yy(1 / Gamma_G))
        if abs(tua_e - 1) < 1e-3:
            return Gamma_G
        elif tua_e > 1:
            lo = Gamma_G
        else:
            hi = Gamma_G
    return Gamma_G


if __name__ == '__main__':
    # ---------- validation against GRB 221009A (Gao & Zou 2023 Table 1) -----
    import os
    cpath = os.path.join(os.path.dirname(__file__), 'c_221009A.txt')
    if os.path.exists(cpath):
        data = np.loadtxt(cpath)
        t = data[:, 0]; alphaM = data[:, 1]; betaM = data[:, 2]
        EP = data[:, 3] * 1e3 * ev_to_erg
        L = data[:, 4] * 4 * np.pi * (2.23e27) ** 2       # d_L(z=0.151)
        z = 0.151; E_G = 7e12 * ev_to_erg; E_maxo = 10e6 * ev_to_erg
        E_max = 7e12 * ev_to_erg; beta_G = 2.3; T_90 = 100; eta = 1
        R_M = 0; T_REF = 226
        print("GRB 221009A validation (paper: 297.92/162.93/139.31/113.06):")
        for tb in (5, 10, 15, 20):
            print("  t_T=%2ds: Gamma_T,min = %.1f" % (tb, gamma_min(tb)))
        print()

    # ---------- GRB 210704A (outer internal shock, t_G = 1 ms) --------------
    z = 2.34; E_maxo = 10e6 * ev_to_erg; beta_G = 1.8; T_90 = 1.35
    eta = 1; R_M = 0; T_REF = 0.0
    t = np.array([-1e3, 1e3])                 # flat (time-constant) MeV target
    alphaM = np.array([0.06, 0.06]); betaM = np.array([2.80, 2.80])
    EP = np.array([256e3 * ev_to_erg, 256e3 * ev_to_erg])
    L = np.array([3.7e53, 3.7e53])
    print("GRB 210704A, t_G = 1 ms, L_M = 3.7e53, Band(0.06, 2.80), "
          "E_P = 256 keV, z = 2.34:")
    for EG in (1.21, 4.39, 16.09):
        E_G = EG * 1e9 * ev_to_erg
        E_max = E_G
        gm = gamma_min(1e-3)
        R_G_ = 2 * gm * gm * c * (1e-3 / (1 + z))
        Ecom = EG * 1e3 * (1 + z) / (2 * gm)   # comoving gap-photon energy [MeV]
        print("  %5.2f GeV: Gamma_G,min = %5.1f   R_G = %.2e cm   "
              "(comoving %.2f MeV)" % (EG, gm, R_G_, Ecom))
