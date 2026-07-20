"""
Two-zone (crossing-geometry) gamma-gamma constraint on the GeV-zone Lorentz
factor for GRB 210704A.

Physical picture (the "outer internal shock" variant of Zou, Fan & Piran
2011, ApJ 726, L2 / Gao & Zou 2023, ApJL 956, L38): the MeV photons come
from an inner internal shock; the GeV photons come from a *more external
internal shock* (NOT the external shock of Gao & Zou 2023), so the GeV
emission time is the millisecond variability time t_G ~ 1 ms and the GeV
radius stays at R_G = 2 Gamma_G^2 c t_G/(1+z) ~ 1e12 cm (compatible with
the deuterium radius). A GeV photon emitted at theta_G = 1/Gamma_G
overtakes the radial MeV photon shell; along the trajectory the collision
angle obeys R sin(theta) = R_G sin(theta_G).

The MeV target is a BAND function (alpha_M, beta_M); the 16 GeV photon's
pair-production threshold sits ABOVE E_P, so the relevant single index is
beta_M -- this is the "alpha" of Gao & Zou (2023) Eq. (17).

Two methods, same physics:
  * Method A (this file, `tau_cross` / `GammaG_min_A`): numerical
    integration of the optical depth with the exact pair-production cross
    section and the Band target [= Gao & Zou 2023 Eqs. (12)-(13)].
  * Method B (`eq17`): the analytic minimum Lorentz factor, Gao & Zou 2023
    Eq. (17), first (fundamental) line, with the effective peak E_P* of
    their Eq. (8).

NOTE: A and B currently differ by a constant factor ~4.3 in Gamma_min
(A lower). It is NOT the cross section (tested: exact vs sigma_T/(3*s)
changes A by <3%). The residual is a constant normalization in the
analytic reduction Eq.(16)->(17) (the l_max bracket / the 6*4^alpha
coefficient). To be reconciled against the published 221009A result.
"""

import numpy as np
from scipy.optimize import brentq

# ------------------------------------------------------------- constants
sigT = 6.652e-25
c = 3.0e10
me = 9.109e-28
mec2_erg = me * c * c
mec2 = 0.511e-3           # GeV
z = 2.34

# ------------------------------------------- 210704A inner (MeV) zone: Band
L_M = 3.7e53              # erg/s  isotropic MeV luminosity
E_P = 256e-6             # GeV    Band peak energy
alpha_M, beta_M = 0.06, 2.80    # Band photon-number indices (|alpha|,|beta|)
Emax_M = 10e-3           # GeV    upper end of the MeV component

# Gao & Zou (2023) Eq. (8) effective peak (note: the two terms ADD):
#   E_P*^2 = E_P^2 [ 1/(2-alpha_M) + 1/(beta_M-2) (1 - (Emax/E_P)^(2-beta_M)) ]
EPstar = E_P * np.sqrt(1 / (2 - alpha_M)
                       + 1 / (beta_M - 2) * (1 - (Emax_M / E_P) ** (2 - beta_M)))


def sigma_gg(s):
    """Exact pair-production cross section vs s = (E_cm/m_e c^2)^2 (>1)."""
    s = np.atleast_1d(s).astype(float)
    out = np.zeros_like(s)
    m = s > 1.0001
    b = np.sqrt(1 - 1 / s[m])
    out[m] = (3 / 16) * sigT * (1 - b ** 2) * (
        (3 - b ** 4) * np.log((1 + b) / (1 - b)) - 2 * b * (2 - b ** 2))
    return out


def n0(R):
    """MeV photon normalization (Gao & Zou 2023 Eq. 7), cm^-3 GeV^-1."""
    return L_M / ((1 + z) ** 2 * 4 * np.pi * R ** 2 * c * EPstar ** 2)


def band(E):
    E = np.atleast_1d(E)
    return np.where(E < E_P, (E / E_P) ** (-alpha_M), (E / E_P) ** (-beta_M))


def tau_cross(E_G, Gamma, t_G, n_R=240):
    """Method A: crossing-geometry gamma-gamma optical depth (exact sigma)."""
    R_G = 2 * Gamma ** 2 * c * t_G / (1 + z)
    p = R_G * np.sin(1 / Gamma)                 # impact parameter
    lnR = np.linspace(np.log(R_G), np.log(3e3 * R_G), n_R)
    Rg = np.exp(lnR)
    out = np.zeros_like(Rg)
    for i, R in enumerate(Rg):
        th = np.arcsin(min(p / R, 1.0))
        omc = 1 - np.cos(th)
        if omc <= 0:
            continue
        E_min = 2 * mec2 ** 2 / ((1 + z) ** 2 * E_G * omc)
        if E_min >= Emax_M:
            continue
        lnE = np.linspace(np.log(E_min * 1.001), np.log(Emax_M), 130)
        Em = np.exp(lnE)
        s = E_G * Em * (1 + z) ** 2 * omc / 2 / mec2 ** 2
        out[i] = np.trapezoid(n0(R) * band(Em) * sigma_gg(s) * omc * Em, lnE) * R
    return np.trapezoid(out, lnR)


def GammaG_min_A(E_G, t_G):
    try:
        return brentq(lambda G: np.log(tau_cross(E_G, G, t_G)), 60, 9000,
                      rtol=2e-3)
    except Exception:
        return np.nan


def eq17(E_G, t_G, alpha=beta_M):
    """Method B: Gao & Zou (2023) Eq. (17), fundamental (first) line."""
    epsT, epsP, epsPs = E_G / mec2, E_P / mec2, EPstar / mec2
    num = (1 + z) ** (2 * alpha - 3) * L_M * epsT ** (alpha - 1) \
        * epsP ** alpha * sigT
    den = 12 * 4 ** alpha * np.pi * mec2_erg * c * c * t_G * epsPs ** (2 * alpha)
    return (num / den) ** (1 / (2 * alpha + 2))


if __name__ == '__main__':
    print("GRB 210704A two-zone crossing (outer internal shock, t_G = 1 ms)")
    print("L_M=3.7e53, E_P=256 keV, Band (a,b)=(0.06,2.80), "
          "E_P*=%.2f E_P, z=2.34\n" % (EPstar / E_P))
    print("%8s | %12s | %14s | %6s" % ("E_G[GeV]", "A: numeric",
                                        "B: Eq17(1st)", "R_G[cm]"))
    for E_G in (1.21, 4.39, 16.09):
        gA = GammaG_min_A(E_G, 1e-3)
        gB = eq17(E_G, 1e-3)
        R_G = 2 * gA ** 2 * c * 1e-3 / (1 + z)
        print("%8.2f | %12.0f | %14.0f | %.2e" % (E_G, gA, gB, R_G))
    print("\ntau_cross(16 GeV, t_G=1 ms) vs Gamma  (tau ~ Gamma^-(2b+2)):")
    for G in (200, 300, 500, 1000):
        print("   Gamma=%5d: tau=%.3e" % (G, tau_cross(16.09, G, 1e-3)))
