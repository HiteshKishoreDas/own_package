"""
Author: Hitesh Kishore Das 
Date: 2021-10-18 15:15:02 
Last Modified by:   Hitesh Kishore Das 
Last Modified time: 2021-10-18 15:15:02 
"""

import numpy as np
from matplotlib import pyplot as plt
import pwlf

import cooling_fn as cf


def power_fit_discontinuous(N_bin, bin_n, Z):
    T_min, T_max = cf.Lam_range()

    # Z = 1.0

    # N_bin = 10    # Number of bins
    # bin_n = 100    # Number of points in each bin

    T_arr = np.logspace(np.log10(T_min), np.log10(T_max), num=N_bin * bin_n)
    T_arr[0] = T_min
    T_arr[-1] = T_max

    Lam_arr = np.vectorize(cf.Lam_fn)(T_arr, Z)

    Lam_fit_arr = np.zeros(N_bin + 1, dtype=float)
    alp_fit_arr = np.zeros_like(Lam_fit_arr)
    T_fit_arr = np.zeros_like(Lam_fit_arr)

    for k in range(N_bin):
        print(k)
        plt.axvline(T_arr[(k + 1) * bin_n - 1], linestyle="dotted")

        # Arrays with points to do the fitting
        Lam_k = Lam_arr[k * bin_n : (k + 1) * bin_n]
        T_k = T_arr[k * bin_n : (k + 1) * bin_n]

        alp_fit_arr[k], Lam_fit_arr[k] = np.polyfit(np.log10(T_k), np.log10(Lam_k), 1)
        Lam_fit_arr[k] = 10 ** Lam_fit_arr[k]
        Lam_fit_arr[k] *= T_k[0] ** alp_fit_arr[k]
        T_fit_arr[k] = np.min(T_k)

    Lam_fit_arr[-1] = 0
    alp_fit_arr[-1] = 0
    T_fit_arr[-1] = T_max

    return Lam_fit_arr, alp_fit_arr, T_fit_arr


def power_fit_cont(N_bin, bin_n, Z):
    T_min, T_max = cf.Lam_range()

    T_arr = np.logspace(np.log10(T_min), np.log10(T_max), num=N_bin * bin_n)
    T_arr[0] = T_min
    T_arr[-1] = T_max

    Lam_arr = np.vectorize(cf.Lam_fn)(T_arr, Z)

    pwlf_fit = pwlf.PiecewiseLinFit(np.log10(T_arr), np.log10(Lam_arr))
    T_breaks = pwlf_fit.fitfast(N_bin)

    T_breaks = 10 ** (T_breaks)
    T_breaks[0] = T_min
    T_breaks[-1] = T_max

    lam0_fit = 10 ** (pwlf_fit.predict(np.log10(T_breaks)))

    dlam_log = np.log10(np.roll(lam0_fit, -1)[:-1]) - np.log10(lam0_fit[:-1])
    dT_log = np.log10(np.roll(T_breaks, -1)[:-1]) - np.log10(T_breaks[:-1])
    alp_fit = dlam_log / dT_log

    alp_fit = np.append(alp_fit, 0)

    return lam0_fit, alp_fit, T_breaks


if __name__ == "__main__":
    T_min, T_max = cf.Lam_range()

    N_bin = 40
    bin_n = 100
    Z = 1.0  # Solar metallicity

    T_arr = np.logspace(np.log10(T_min), np.log10(T_max), num=N_bin * bin_n)
    T_arr[0] = T_min
    T_arr[-1] = T_max

    Lam_arr = np.vectorize(cf.Lam_fn)(T_arr, Z)

    plt.figure(figsize=(10, 10))
    plt.xscale("log")
    plt.yscale("log")

    plt.plot(
        T_arr,
        Lam_arr,
        linestyle="dashed",
        linewidth=2,
        color="k",
        label="Cooling function",
    )

    labelsize = 15
    ticksize = 12
    titlesize = 15
    legendsize = 15

    lam0_fit, alp_fit, T_breaks = power_fit_cont(N_bin, bin_n, Z)

    for i_t, t in enumerate(T_breaks[:-1]):
        plt.axvline(t, linestyle="dotted")

        T_k = np.logspace(
            np.log10(T_breaks[i_t]), np.log10(T_breaks[i_t + 1]), num=bin_n
        )

        plt.plot(T_k, lam0_fit[i_t] * (T_k / T_breaks[i_t]) ** alp_fit[i_t])

    plt.title(
        "Piecewise power law fit for cooling function using PWLF", fontsize=titlesize
    )
    plt.xlabel("T (K)", fontsize=labelsize)
    plt.ylabel(r"$\Lambda$ (T)", fontsize=labelsize)
    plt.legend(fontsize=legendsize)
    plt.tick_params(labelsize=ticksize)

    plt.savefig(f"power_law_fit_pwlf_Nbins_{N_bin}.png")
