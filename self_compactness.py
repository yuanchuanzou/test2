"""
Self (one-zone) gamma-gamma compactness for the high-energy photons of
GRB 210704A, and its tension with the deuterium optical depth.

This addresses the concern that the two-zone (crossing) geometry does NOT
relieve: a >GeV photon pair-producing on the *co-spatial* photons of its
own zone (isotropic in the comoving frame) -- the original compactness
problem (Ruderman 1975; Lithwick & Sari 2001).

One-zone optical depth (manuscript Appendix C, Eqs. C6-C8):
    tau_gg(E1) = sigma_gg * d_L^2 * Phi(>E_pm) / [2 R c (1+z) Gamma^2],
    E_pm,obs   = (2 Gamma m_e c^2/(1+z))^2 / E1,
with Phi(>E) the OBSERVED photon-number flux of the co-spatial (target)
component above E.

Two target choices are provided:
  (i)  'PL'  : the broad keV-GeV PL/IC component extrapolated as a single
              power law down to keV (worst case);
  (ii) 'obs' : only the actually observed high-energy photons (a spectral
              valley is assumed between the mBB cutoff and ~E_valley),
              i.e. Phi(>E_pm) is capped at Phi(>E_valley).

Deuterium optical depth (v3 main text, luminosity form):
    tau_gD = 1.4 * Y_D * L_K,55 * (R/1e12)^-1 * (Gamma/10^2.5)^-3.

Run:  python3 self_compactness.py
"""

import numpy as np
from scipy.optimize import brentq

# --------------------------------------------------------------- constants
mec2 = 0.511e-3          # GeV
sigT = 6.652e-25         # cm^2
sig_gg = 0.2 * sigT      # angle/threshold-averaged pair cross section
c = 3.0e10               # cm/s
z = 2.34
dL = 5.95e28             # cm at z=2.34
GeV = 1.602e-3           # erg

# ------------------------------------------------- observed target field(s)
p_idx = 1.80             # photon index of the broad PL/IC component
L_PL = 1.0e54            # erg/s isotropic luminosity of the keV-GeV component
S_E = L_PL / (4 * np.pi * dL ** 2)      # bolometric energy flux [erg/cm^2/s]
E_lo, E_hi = 1e-6, 10.0                  # GeV (PL band for normalization)
# photon-flux normalization K [ph/cm^2/s/GeV] from the energy flux
I_E = (E_hi ** (2 - p_idx) - E_lo ** (2 - p_idx)) / (2 - p_idx)   # GeV^(2-p)
K = S_E / (I_E * GeV)

# observed integral photon flux above E [GeV] of the PL component
def Phi_PL(Emin):
    return K * (Emin ** (1 - p_idx) - E_hi ** (1 - p_idx)) / (p_idx - 1)

# 'obs' target: cap the threshold at a valley energy (few observed photons
# between the mBB Wien cutoff and E_valley); above E_valley use the PL.
def Phi_obs(Emin, E_valley=0.1):
    return Phi_PL(max(Emin, E_valley))

def E_pm(E1, G):
    return (2 * G * mec2 / (1 + z)) ** 2 / E1          # GeV

def tau_self(E1, G, R, target='PL', E_valley=0.1):
    Phi = Phi_PL(E_pm(E1, G)) if target == 'PL' \
        else Phi_obs(E_pm(E1, G), E_valley)
    return sig_gg * dL ** 2 * Phi / (2 * R * c * (1 + z) * G ** 2)

def tau_gD(R, G, Y_D=0.3, L_K55=1.0):
    return 1.4 * Y_D * L_K55 * (R / 1e12) ** -1 * (G / 10 ** 2.5) ** -3

def R_of(G, dt):                      # internal-shock radius
    return 2 * G ** 2 * c * dt / (1 + z)

# --------------------------------------------------------------- reporting
if __name__ == '__main__':
    dt = 1e-3
    print("GRB 210704A self-compactness  (z=%.2f, PL: L=%.0e erg/s, index %.2f)"
          % (z, L_PL, p_idx))
    print("Phi_PL(>0.5 MeV) = %.2f ph/cm^2/s, Phi(>0.1 GeV) = %.3f ph/cm^2/s\n"
          % (Phi_PL(0.5e-3), Phi_PL(0.1)))

    print("(1) tau_self(16.09 GeV) vs Gamma, R = 2 Gamma^2 c dt/(1+z), dt=1 ms")
    print("      Gamma     R[cm]    E_pm[MeV]  tau(PL)   tau(obs,valley<0.1GeV)")
    for G in (300, 500, 800, 1200, 1700):
        R = R_of(G, dt)
        print("    %6d  %8.2e  %7.2f   %8.2e   %8.2e"
              % (G, R, E_pm(16.09, G) * 1e3,
                 tau_self(16.09, G, R, 'PL'),
                 tau_self(16.09, G, R, 'obs')))

    print("\n(2) tau_self at Gamma=300, R=1.6e12 cm, for different test photons")
    print("      E1[GeV]  E_pm[MeV]  tau(PL)   tau(obs)")
    R0 = R_of(300, dt)
    for E1 in (0.30, 0.62, 1.21, 4.39, 8.54, 16.09):
        print("    %7.2f  %7.2f   %8.2e  %8.2e"
              % (E1, E_pm(E1, 300) * 1e3,
                 tau_self(E1, 300, R0, 'PL'),
                 tau_self(E1, 300, R0, 'obs')))

    print("\n(3) Gamma required for tau_self(16 GeV)=1 (dt=1 ms shell):")
    for tgt in ('PL', 'obs'):
        f = lambda G: np.log(tau_self(16.09, G, R_of(G, dt), tgt))
        print("      target=%-4s  Gamma_min = %.0f" % (tgt, brentq(f, 100, 6000)))

    print("\n(4) Is there ANY (R,Gamma) with tau_gD>1 AND tau_self(16 GeV)<1?")
    print("      Gamma   R(tau_gD=1)[cm]   tau_self(16GeV) there (obs target)")
    for G in (300, 500, 800, 1200, 1700, 3000):
        # radius at which tau_gD=1 (upper radius allowed for absorption)
        RD = brentq(lambda R: tau_gD(R, G) - 1, 1e8, 1e20)
        print("    %6d  %12.2e     %10.2e"
              % (G, RD, tau_self(16.09, G, RD, 'obs')))
    print("    (tau_self > 1 in every row => no single-zone window; the GeV")
    print("     photons that escape and the deuterium that absorbs them")
    print("     cannot share the same R and Gamma.)")
