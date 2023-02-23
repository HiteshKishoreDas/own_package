"""
Author: Hitesh Kishore Das 
Date: 2021-10-18 14:23:49 
Last Modified by:   Hitesh Kishore Das 
Last Modified time: 2021-10-18 14:23:49 
"""


import numpy as np

import os
import sys

cwd = os.path.dirname(__file__)
package_abs_path = cwd[: -len(cwd.split("/")[-1])]

sys.path.insert(0, f"{package_abs_path}utils/")
import units as un

sys.path.insert(0, f"{package_abs_path}cooling/")
import power_law_fit_max as pm

cwd = os.getcwd()
repo_abs_path = cwd[: -len(cwd.split("/")[-1])]

cooling_dir = f"{package_abs_path}cooling/"


def Lam_fn(T, Zsol=1.0, Lambda_fac=1.0):

    Lam_file = np.loadtxt(cooling_dir + "CT_WSS09.dat")

    T_min = np.min(Lam_file[:, 0])
    T_max = np.max(Lam_file[:, 0])

    N = np.shape(Lam_file)[0]

    if T < T_min or T > T_max:
        return 0.0

    else:

        i_a = 0
        i_b = N - 1

        while i_a != i_b - 1:

            mid = int((i_a + i_b) / 2)

            if T > Lam_file[mid, 0]:
                i_a = mid
            else:
                i_b = mid

        T_a = Lam_file[i_a, 0]
        T_b = Lam_file[i_b, 0]

        LamH_a = Lam_file[i_a, 1]
        LamH_b = Lam_file[i_b, 1]

        LamZ_a = Lam_file[i_a, 2]
        LamZ_b = Lam_file[i_b, 2]

        dT = T_b - T_a

        LamH = LamH_a * (T_b - T) / dT + LamH_b * (T - T_a) / dT
        LamZ = LamZ_a * (T_b - T) / dT + LamZ_b * (T - T_a) / dT

    return (LamH + LamZ * Zsol) * Lambda_fac


def Lam_fn_powerlaw_pwlf_fit(T, Zsol=1.0, Lambda_fac=1.0):

    Lam_file = np.loadtxt(cooling_dir + "power_law_fit_Z_1.0.txt")

    T_min = np.min(Lam_file[:, 0])
    T_max = np.max(Lam_file[:, 0])

    N = np.shape(Lam_file)[0]

    if T < T_min or T > T_max:
        return 0.0

    else:

        i_a = 0
        i_b = N - 1

        while i_a != i_b - 1:

            mid = int((i_a + i_b) / 2)

            if T > Lam_file[mid, 0]:
                i_a = mid
            else:
                i_b = mid

        T_a = Lam_file[i_a, 0]
        T_b = Lam_file[i_b, 0]

        Lam = Lam_file[i_a, 1] * (T / Lam_file[i_a, 0]) ** Lam_file[i_a, 2]

        return Lam * Lambda_fac


def Lam_fn_powerlaw(T, Zsol=1.0, Lambda_fac=1.0):

    T_min = np.min(pm.cool_t)
    T_max = np.max(pm.cool_t)

    N = len(pm.cool_t)

    if T < T_min or T > T_max:
        return 0.0

    else:

        i_a = 0
        i_b = N - 1

        while i_a != i_b - 1:

            mid = int((i_a + i_b) / 2)

            if T > pm.cool_t[mid]:
                i_a = mid
            else:
                i_b = mid

        T_a = pm.cool_t[i_a]
        T_b = pm.cool_t[i_b]

        Lam = (pm.cool_coef[i_a] * 1e-23) * (T / pm.cool_t[i_a]) ** pm.cool_index[i_a]

        return Lam * Lambda_fac


def Lam_range():

    Lam_file = np.loadtxt("CT_WSS09.dat")

    T_min = np.min(Lam_file[:, 0])
    T_max = np.max(Lam_file[:, 0])

    return T_min, T_max


def tcool_calc(rho, T, Zsol=1.0, Lambda_fac=1.0, fit_type="max"):

    n_H = rho * un.unit_density / (un.muH * un.CONST_amu)

    fit_dict = {}
    fit_dict["max"] = Lam_fn_powerlaw
    # fit_dict['5pnt_pwlf'] = Lam_fn_powerlaw_pwlf_fit
    # fit_dict['continuous'] = Lam_fn

    lam_arr = fit_dict[fit_type](T=T, Zsol=Zsol, Lambda_fac=Lambda_fac)
    # print(f"{lam_arr=}")

    p = rho * T / (un.KELVIN * un.mu)  # in code units
    # print(f"{p= }")

    q = n_H * n_H * lam_arr / un.unit_q  # in code units
    # print(f"{un.muH= }")

    tc = p / (q * (un.g - 1))  # in code units
    # print(f"{tc= }")

    return tc
    # in code units


if __name__ == "__main__":

    T = 4e4
    print(Lam_fn(T))
    print(tcool_calc(1, T))
