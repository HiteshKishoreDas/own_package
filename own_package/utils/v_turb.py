import numpy as np
import matplotlib.pyplot as plt

import os
import sys

cwd = os.path.dirname(__file__)
package_abs_path = cwd[: -len(cwd.split("/")[-1])]

sys.path.insert(0, f"{package_abs_path}utils/")
import units as g

alpha_hyd = 2 ** (1 / 3)  # 1.26 # 1.383
alpha_mhd = (2 * 4.2 / 0.77) ** (1 / 3)


def v_turb_hydro(rho, L_box, dedt, prop_const=alpha_hyd):
    """
    ARGS:
    rho  : Density in amu
    L_box: Box size in kpc
    dedt : dedt in 1E (amu kpc^5 Myr^-3)
    prop_const: Dimensionless constant

    RETURNS:
    v_turb: Turbulent velocity in 1 kpc/Myr
    """

    rho_exp = -1 / 3
    L_exp = -2 / 3
    dedt_exp = 1 / 3

    v_turb = (rho**rho_exp) * (L_box**L_exp) * (dedt**dedt_exp)
    v_turb *= prop_const

    return v_turb


def dedt_calc_hydro(M, rho, T_hot, L, mu=0.5):
    """
    Returns required dedt for a given Mach number, density, temperature
    and  box size
    """

    cs_new = cs_calc(T_hot, mu)
    # print(f'cs_new: {cs_new}')

    dedt_req = rho * (cs_new**3) * (L**2) * (M**3) / (alpha_hyd**3)

    return dedt_req


def v_turb_mhd(rho, L_box, dedt, prop_const=alpha_mhd):
    """
    ARGS:
    rho  : Density in amu
    L_box: Box size in kpc
    dedt : dedt in 1E (amu kpc^5 Myr^-3)
    prop_const: Dimensionless constant

    RETURNS:
    v_turb: Turbulent velocity in 1 kpc/Myr
    """

    rho_exp = -1 / 3
    L_exp = -2 / 3
    dedt_exp = 1 / 3

    dedt_corr_exp = 1.0
    dedt_corr_mul = 1.0  # 1.6

    dedt_corr = (dedt_corr_mul) * (dedt**dedt_corr_exp)

    v_turb = (rho**rho_exp) * (L_box**L_exp) * (dedt_corr**dedt_exp)
    v_turb *= prop_const

    return v_turb


def dedt_calc_mhd(M, rho, T_hot, L, mu=0.5):
    """
    Returns required dedt for a given Mach number, density, temperature
    and  box size
    """

    cs_new = cs_calc(T_hot, mu)
    # print(f'cs_new: {cs_new}')

    dedt_corr_req = rho * (cs_new**3) * (M**3) * (L**2) / (alpha_mhd**3)

    dedt_corr_exp = 0.96
    dedt_corr_mul = 1.0  # 1.6

    dedt_req = dedt_corr_req / (dedt_corr_mul)
    dedt_req = dedt_req ** (1 / dedt_corr_exp)

    return dedt_req


def cs_calc(T_hot, mu=0.5):
    # cs_ini = 0.06725645065307617

    # cs_new = cs_ini*np.sqrt(T_hot/1e7)

    M = 1e-3
    R = 8.31446261815324

    # mu = 0.5

    kB = 1.38 * 1e-23
    mp = 1.66 * 1e-27

    m_to_cm = 100

    # return np.sqrt(g.g*R*T_hot/M) * m_to_cm/g.unit_velocity
    return np.sqrt(g.gamma * kB / (mu * mp) * T_hot) * m_to_cm / g.unit_velocity


# def dedt_calc(M, rho, T_hot, L, mu):
#     """
#     Returns required dedt for a given Mach number, density, temperature
#     and  box size
#     """

#     cs_new = cs_calc(T_hot,mu)
#     # print(f'cs_new: {cs_new}')

#     dedt_req = rho*(cs_new**3)*(L**2)*(M**3)/(alpha**3)

#     return dedt_req


def v_turb_contour(
    x_range,
    y_range,
    const_value,
    rho_flag=False,
    L_flag=True,
    dedt_flag=True,
    cs_flag=False,
):
    N = 100
    M = 100

    x = np.logspace(np.log10(x_range[0]), np.log10(x_range[1]))
    y = np.logspace(np.log10(y_range[0]), np.log10(y_range[1]))

    X, Y = np.meshgrid(x, y)

    if not (rho_flag):
        rho = const_value
        Z = v_turb_calc(rho, X, Y)
        x_label = "L_box"
        y_label = "dedt"

    elif not (L_flag):
        L_box = const_value
        Z = v_turb_calc(X, L_box, Y)
        x_label = "rho"
        y_label = "dedt"

    elif not (dedt_flag):
        dedt = const_value
        Z = v_turb_calc(X, Y, dedt)
        x_label = "rho"
        y_label = "L_box"

    fig, ax = plt.subplots(1, 1, figsize=(10, 8))

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)

    # ax.contour(X, Y, Z)

    if cs_flag:
        cf = ax.contour(X, Y, np.log10(Z / cs_ini), linewidths=3, levels=5)
    else:
        cf = ax.contour(X, Y, np.log10(Z), linewidths=3, levels=25)

    ax.set_title("Contour Plot")
    fig.colorbar(cf, ax=ax)
    plt.show()


# if __name__=="__main__":

#     L_box_range = [1,10000]
#     dedt_range = [1,250]
#     rho = 1

#     v_turb_contour(L_box_range,dedt_range,rho,cs_flag=True)
