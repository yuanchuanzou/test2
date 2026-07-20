"""
Self (co-spatial) gamma-gamma absorption of the 16 GeV photon by the OUTER
(GeV/PL) zone's OWN photons, evaluated at the two-zone crossing solution
(Gamma_G = 434, R_G = 3.4e12 cm; see twozone_crossing_gaozou.py).

This is DISTINCT from the crossing opacity against the inner (mBB) zone:
here the 16 GeV photon pair-produces on the PL/IC photons that are produced
in the SAME (outer) zone and are isotropic in the comoving frame -- the
original one-zone compactness, which the two-zone geometry does NOT relieve.

The target is the PL/IC component with photon index beta_PL = 1.8; its
threshold energy for the 16 GeV photon (Gamma = 434) is ~1 MeV (observed).

Result: with the full observed keV-GeV luminosity (L_PL = 1e54 erg/s), the
16 GeV photon self-absorbs (tau_self = 2.2e3) unless Gamma >~ 1700. For it
to escape at Gamma ~ 434, the OUTER zone's own photon field near ~1 MeV
must be >~ 1e3-1e4 times fainter than the keV-GeV power-law extrapolation
-- i.e. the bright ~MeV emission must belong to the inner (mBB) zone, and
the outer IC/PL component must turn over (be faint) below ~a few MeV.

The recovery photons that actually define the gap (1.21-4.39 GeV) have
higher thresholds (2-7 MeV), where the field is far fainter, so they are
not similarly constrained; the 16 GeV photon is the sole outlier.
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

sigT = 6.652e-25
mec2 = 0.511e-3        # GeV
c = 3.0e10
z = 2.34
GeV = 1.602e-3
E1 = 16.09             # GeV, highest-energy photon


def sig(s):
    s = np.atleast_1d(s).astype(float)
    o = np.zeros_like(s)
    m = s > 1.0001
    b = np.sqrt(1 - 1 / s[m])
    o[m] = (3 / 16) * sigT * (1 - b ** 2) * (
        (3 - b ** 4) * np.log((1 + b) / (1 - b)) - 2 * b * (2 - b ** 2))
    return o


def tau_self(Gamma, R, L_PL, bPL=1.8, Elo=1e-6, Ehi=16.09):
    """One-zone (co-spatial, isotropic comoving) gamma-gamma optical depth of
    the 16 GeV photon against a PL target of luminosity L_PL, index bPL."""
    Up = L_PL / (4 * np.pi * R ** 2 * c * Gamma ** 2) / GeV        # GeV/cm^3
    elo, ehi = [E * (1 + z) / (2 * Gamma) for E in (Elo, Ehi)]
    n0 = Up * (2 - bPL) / (ehi ** (2 - bPL) - elo ** (2 - bPL))
    e1 = E1 * (1 + z) / (2 * Gamma)

    def integ(lne2):
        e2 = np.exp(lne2)
        mus = np.linspace(-0.999, 1, 40)
        s = e1 * e2 * (1 - mus) / 2 / mec2 ** 2
        ang = np.trapezoid((1 - mus) / 2 * sig(s), mus) / 2
        return n0 * e2 ** -bPL * ang * e2
    val, _ = quad(integ, np.log(elo), np.log(ehi), limit=120)
    return val * (R / Gamma)


if __name__ == '__main__':
    print("Self-absorption of the 16 GeV photon by the outer-zone PL")
    print("(R_G = 2 Gamma^2 c t_G/(1+z), t_G = 1 ms):\n")
    for L_PL, lab in [(1e54, 'L_PL = 1e54 (full observed keV-GeV component)'),
                      (1e53, 'L_PL = 1e53 (outer PL 10x fainter at MeV)'),
                      (1e52, 'L_PL = 1e52 (100x fainter)')]:
        print("  " + lab)
        for G in (300., 434.):
            R = 2 * G ** 2 * c * 1e-3 / (1 + z)
            print("     Gamma=%3.0f, R=%.2e: tau_self = %.2e"
                  % (G, R, tau_self(G, R, L_PL)))
        gs = brentq(lambda G: np.log(tau_self(G, 2 * G ** 2 * c * 1e-3 / (1 + z),
                                              L_PL)), 150, 6000)
        print("     -> tau_self = 1 at Gamma = %.0f\n" % gs)
