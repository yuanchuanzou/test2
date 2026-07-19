"""
Two-zone compactness constraints on the Lorentz factors for GRB 210704A.

Model (following Zou, Fan & Piran 2011, ApJ 726, L2 and the corrected
formulas of Gao & Zou 2023, ApJL 956, L38): the GeV photons come from an
outer internal shock (zone G, radius R_G, Lorentz factor Gamma_G), while
the MeV photons come from an inner internal shock (zone M, radius R_M,
Lorentz factor Gamma_M).  A GeV photon emitted at angle theta_T ~ 1/Gamma_G
crosses the MeV photon shell; at radius R the collision angle theta obeys
R sin(theta) = R_T sin(theta_T), so the field becomes more and more radial
and the opacity is strongly reduced compared with the one-zone case.

Instead of using the simplified analytic formulas (Eq. (17) of Gao & Zou
2023; Eqs. (14)-(15) of Zou et al. 2011), the optical depth is integrated
numerically with
  - the exact pair-production cross section (Jauch & Rohrlich 1980),
  - the exact threshold E_min = 2(m_e c^2)^2 / [(1+z)^2 E_T (1-cos theta)],
  - the observed MeV spectrum of GRB 210704A,
which avoids the small-angle / single-power-law approximations (and the
typos of the published simplified formulas).  The analytic Eq. (17) is also
implemented for cross-checking.

Data of GRB 210704A (from the manuscript):
  z = 2.34;  highest-energy LAT photon E_T = 16.09 GeV at t_T ~ 0.96 s;
  MeV (peaking) component from the BAND+PL fit in T0+[0.7, 2.05] s:
      E_p = 256.1 keV, alpha_Band = -0.06, beta_Band = -2.80,
      L_M = L_gamma,peak = 3.7e53 erg/s;
  PL component: photon index 1.80, L_gamma,keV-GeV = 1.0e54 erg/s;
  MeV-pulse duration T90 ~ 1.35 s (T0+[0.7, 2.05] s);
  variability delta_t ~ 1 ms  (wavelet decomposition).

Author: prepared for the GRB 210704A deuterium-absorption paper.
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq

# ---------------------------------------------------------------- constants
mec2_erg = 8.187e-7           # electron rest energy [erg]
sigma_T  = 6.652e-25          # Thomson cross section [cm^2]
c        = 2.998e10           # speed of light [cm/s]
keV      = 1.602e-9           # [erg]
MeV      = 1.602e-6
GeV      = 1.602e-3

# ------------------------------------------------------- GRB 210704A inputs
z        = 2.34
E_T      = 16.09 * GeV        # highest-energy LAT photon
t_T      = 0.96               # observed arrival time of that photon [s]
T90_MeV  = 1.35               # duration of the main MeV pulse [s]
E_maxo   = 10.0 * MeV         # maximal energy of the observed MeV component

# MeV (peaking) component, BAND+PL fit
E_p      = 256.1 * keV
a_M      = 0.06               # = -alpha_Band  (photon index below E_p)
b_M      = 2.80               # = -beta_Band   (photon index above E_p)
L_peak   = 3.7e53             # erg/s

# PL component (in case it is attributed to the inner zone as well)
p_PL     = 1.80               # photon index of the PL component
L_PL_tot = 1.0e54             # erg/s over the keV-GeV band
E_PL_lo, E_PL_hi = 1.0 * keV, 10.0 * GeV


# ----------------------------------------------------------- target spectra
def shape_band(E):
    """Unnormalized photon-number spectrum of the peaking (MeV) component."""
    return np.where(E <= E_p, (E / E_p) ** (-a_M), (E / E_p) ** (-b_M))


def shape_pl(E):
    return (E / E_p) ** (-p_PL)


class TargetField:
    """Photon field of the inner (MeV) zone, n_E(E, R) in [ph/cm^3/erg]."""

    def __init__(self, include_pl=False):
        self.include_pl = include_pl
        # energy normalization U_i = int E s_i(E) dE over the emitted band
        self.U_band = quad(lambda E: E * shape_band(E), 1e-3 * keV, E_maxo,
                           limit=200)[0]
        if include_pl:
            # the PL luminosity within the target band (<= E_maxo)
            U_full = quad(lambda E: E * shape_pl(E), E_PL_lo, E_PL_hi,
                          limit=200)[0]
            U_band_pl = quad(lambda E: E * shape_pl(E), E_PL_lo, E_maxo,
                             limit=200)[0]
            self.L_pl_band = L_PL_tot * U_band_pl / U_full
            self.U_pl = U_band_pl

    def n_E(self, E, R):
        """Comoving-frame... (lab-frame) number density per unit energy at R."""
        pref = 1.0 / ((1 + z) ** 2 * 4 * np.pi * R ** 2 * c)
        n = pref * L_peak * shape_band(E) / self.U_band
        if self.include_pl:
            n += pref * self.L_pl_band * shape_pl(E) / self.U_pl
        return n


# ------------------------------------------------- exact gamma-gamma sigma
def sigma_gg(E_M, E_Tph, one_minus_cos):
    """Exact pair-production cross section (Jauch & Rohrlich 1980).

    Vectorized in E_M; energies are observed ones, boosted by (1+z) each.
    """
    E_M = np.asarray(E_M, dtype=float)
    x = 2 * mec2_erg ** 2 / ((1 + z) ** 2 * E_M * E_Tph * one_minus_cos)
    below = x < 1.0
    beta = np.sqrt(np.clip(1.0 - x, 0.0, None))
    beta = np.clip(beta, 1e-12, 1 - 1e-12)
    sig = (3.0 / 16.0) * sigma_T * (1 - beta ** 2) * (
        (3 - beta ** 4) * np.log((1 + beta) / (1 - beta))
        - 2 * beta * (2 - beta ** 2))
    return np.where(below, sig, 0.0)


def _dtau_dR(R, omc, field, E_Tph, n_E_grid=160):
    """d tau / dR at radius R for collision angle with 1-cos(theta)=omc."""
    E_min = 2 * mec2_erg ** 2 / ((1 + z) ** 2 * E_Tph * omc)
    if E_min >= E_maxo:
        return 0.0
    lnE = np.linspace(np.log(E_min * (1 + 1e-9)), np.log(E_maxo), n_E_grid)
    E = np.exp(lnE)
    integ = field.n_E(E, R) * sigma_gg(E, E_Tph, omc) * omc * E
    return np.trapezoid(integ, lnE)


# --------------------------------------------- optical depth, zone-G photon
def tau_G(Gamma, eta=1.0, field=None, E_Tph=E_T, n_R=140):
    """
    Optical depth of a high-energy photon from the outer zone crossing the
    MeV shell.  Emitted at theta_T = 1/Gamma, R_T = 2 Gamma^2 c eta t_T/(1+z);
    at radius R the collision angle follows R sin(theta) = R_T sin(theta_T).
    """
    if field is None:
        field = TargetField()
    theta_T = 1.0 / Gamma
    R_T = 2 * Gamma ** 2 * c * (eta * t_T) / (1 + z)
    # maximal radius: photon leaves the MeV shell (Zou et al. 2011, Eq. 2)
    x_crit = 2 * c * T90_MeV / ((1 + z) * theta_T ** 2 * R_T)
    R_max = R_T / (1 - x_crit) if x_crit < 1 else 3e3 * R_T
    R_max = min(R_max, 3e3 * R_T)          # integrand converges as R^-4
    p_imp = R_T * np.sin(theta_T)

    lnR = np.linspace(np.log(R_T), np.log(R_max), n_R)
    Rg = np.exp(lnR)
    integ = np.zeros_like(Rg)
    for i, R in enumerate(Rg):
        sth = p_imp / R
        theta = np.arcsin(min(sth, 1.0))
        omc = 1 - np.cos(theta)
        if omc <= 0:
            continue
        integ[i] = _dtau_dR(R, omc, field, E_Tph) * R   # d(lnR) measure
    return np.trapezoid(integ, lnR)


def gamma_G_min(eta=1.0, field=None, E_Tph=E_T):
    f = lambda g: tau_G(g, eta=eta, field=field, E_Tph=E_Tph) - 1.0
    lo, hi = 5.0, 8000.0
    if f(lo) < 0:
        return lo          # already transparent
    if f(hi) > 0:
        return np.inf
    return brentq(f, lo, hi, rtol=1e-3)


# --------------------------------------------- optical depth, zone-M limit
def tau_M(Gamma_M, R_M, R_G, field=None, E_Tph=E_T, n_R=140):
    """
    Optical depth of an on-axis GeV photon in the regime theta_G <
    R_M/(R Gamma_M): the collision angle is set by the angular width of the
    MeV photon beam, theta(R) ~ R_M/(R Gamma_M)  (Zou et al. 2011, Sec. 2).
    Depends on Gamma_M and not on Gamma_G.
    """
    if field is None:
        field = TargetField()
    R_end = 3e4 * R_G
    lnR = np.linspace(np.log(R_G), np.log(R_end), n_R)
    Rg = np.exp(lnR)
    integ = np.zeros_like(Rg)
    for i, R in enumerate(Rg):
        theta = R_M / (R * Gamma_M)
        omc = 1 - np.cos(theta)
        if omc <= 0:
            continue
        integ[i] = _dtau_dR(R, omc, field, E_Tph) * R
    return np.trapezoid(integ, lnR)


def gamma_M_min(R_M, R_G, field=None):
    f = lambda g: tau_M(g, R_M, R_G, field=field) - 1.0
    lo, hi = 1.001, 3000.0
    if f(lo) < 0:
        return lo
    if f(hi) > 0:
        return np.inf
    return brentq(f, lo, hi, rtol=1e-3)


# ------------------------------------------ analytic Eq. (17) (cross-check)
def gamma_T_min_eq17(alpha, eta=1.0, L_M=L_peak, EP=E_p, EPstar=None):
    """Simplified formula, Eq. (17) of Gao & Zou (2023), with eta t_T."""
    if EPstar is None:
        # E_P*^2 = int E s(E) dE / E_P^... (effective peak energy squared)
        U = quad(lambda E: E * shape_band(E), 1e-3 * keV, E_maxo,
                 limit=200)[0]
        EPstar = np.sqrt(U)
    eps_T = E_T / mec2_erg
    eps_P = EP / mec2_erg
    eps_Ps = EPstar / mec2_erg
    num = (1 + z) ** (2 * alpha - 3) * L_M * eps_T ** (alpha - 1) \
        * eps_P ** alpha * sigma_T
    den = 12 * 4 ** alpha * np.pi * (mec2_erg * c ** 2) \
        * (eta * t_T) * eps_Ps ** 2 * alpha
    return (num / den) ** (1.0 / (2 * alpha + 2))


# ------------------------------------------------------------------ report
if __name__ == '__main__':
    band_only = TargetField(include_pl=False)
    band_pl = TargetField(include_pl=True)

    print('=' * 72)
    print('Two-zone compactness limits for GRB 210704A '
          '(E_T = 16.09 GeV, t_T = 0.96 s, z = 2.34)')
    print('=' * 72)

    for label, field in (('MeV target = peaking (BAND) component only, '
                          'L_M = 3.7e53 erg/s', band_only),
                         ('MeV target = BAND + PL(<10 MeV) components',
                          band_pl)):
        print('\n--- ' + label)
        for eta in (1.0, 1e-2, 1e-3):
            g = gamma_G_min(eta=eta, field=field)
            R_T = 2 * g ** 2 * c * (eta * t_T) / (1 + z) if np.isfinite(g) \
                else float('nan')
            print(f'  eta = {eta:7.0e}:  Gamma_G,min = {g:7.1f}'
                  f'   (R_G = {R_T:9.3e} cm)')

    # radius required for Gamma_G = 300 to be optically thin
    print('\n--- R_G required for tau_gg(Gamma_G = 300) = 1:')
    for field, name in ((band_only, 'BAND-only'), (band_pl, 'BAND+PL')):
        g = lambda eta: tau_G(300., eta=eta, field=field) - 1.0
        eta1 = brentq(g, 0.3, 100., rtol=1e-3)
        R_G = 2 * 300 ** 2 * c * (eta1 * t_T) / (1 + z)
        print(f'  {name}: eta = {eta1:5.2f}  ->  R_G = {R_G:.2e} cm')

    # the 1.21-4.39 GeV photons that constitute the upper boundary of the gap
    print('\n--- limits for the recovery photons (outer zone, eta = 1):')
    for ET, tt in ((1.21, 1.04), (4.39, 1.94)):
        g = gamma_G_min(eta=tt / t_T, field=band_only, E_Tph=ET * GeV)
        print(f'  E = {ET:5.2f} GeV (t = {tt} s): Gamma_G,min = {g:6.1f}')

    print('\n--- Lorentz-factor limit of the MeV zone '
          '(on-axis geometry, Zou et al. 2011), R_G = 2e15 cm:')
    for R_M in (1e11, 1.5e12, 1e13):
        gM = gamma_M_min(R_M, 2e15, field=band_only)
        print(f'  R_M = {R_M:.1e} cm: Gamma_M,min = {gM:6.1f}')

    # sanity: tau at Gamma = 300 for the adopted configuration
    for field, name in ((band_only, 'BAND-only'), (band_pl, 'BAND+PL')):
        print(f'\n--- tau_gg(16.09 GeV) at Gamma_G = 300 ({name} target):')
        for eta in (1.0, 1e-2, 1e-3):
            print(f'  eta = {eta:7.0e}:  '
                  f'tau = {tau_G(300., eta=eta, field=field):.3e}')
