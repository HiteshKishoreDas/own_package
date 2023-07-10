import numpy as np
import math

import os

cwd = os.path.dirname(__file__)
package_abs_path = cwd[: -len(cwd.split("/")[-1])]

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


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    T_arr = np.logspace(2, 8.1, num=81)
    T_arr = np.round(T_arr)
    Lambda_val = np.vectorize(Lam_fn)(T_arr)

    # plt.plot(T_arr, Lambda_val)
    # plt.loglog()

    cool_t = []
    cool_coef = []
    cool_ind = []

    for i_T, T in enumerate(T_arr[:-1]):
        cool_t.append(np.copy(T))
        cool_coef.append(np.copy(Lambda_val[i_T]))

        ind = np.log10(Lambda_val[i_T + 1] / Lambda_val[i_T]) / np.log10(
            T_arr[i_T + 1] / T_arr[i_T]
        )
        cool_ind.append(ind)

    def Lam_fn_powerlaw(T, Zsol=1.0, Lambda_fac=1.0):
        T_min = np.min(cool_t)
        T_max = np.max(cool_t)

        N = len(cool_t)

        if T < T_min or T > T_max:
            return 0.0

        else:
            i_a = 0
            i_b = N - 1

            while i_a != i_b - 1:
                mid = int((i_a + i_b) / 2)

                if T > cool_t[mid]:
                    i_a = mid
                else:
                    i_b = mid

            T_a = cool_t[i_a]
            T_b = cool_t[i_b]

            Lam = (cool_coef[i_a]) * (T / cool_t[i_a]) ** cool_ind[i_a]

            return Lam * Lambda_fac

    T_arr = np.logspace(2, 8.1, num=100)
    Lambda_val = np.vectorize(Lam_fn)(T_arr)
    Lambda_powlaw = np.vectorize(Lam_fn_powerlaw)(T_arr)

    plt.plot(T_arr, Lambda_val, linestyle=":")
    plt.plot(T_arr, Lambda_powlaw)

    plt.loglog()

    for i_T, T in enumerate(cool_t):
        print(f"cool_t({i_T}) = {T};")

    print("\n\n")

    for i_T, T in enumerate(cool_coef):
        print(f"cool_coef({i_T}) = {T/1e-23};")

    print("\n\n")

    for i_T, T in enumerate(cool_ind):
        print(f"cool_index({i_T}) = {T};")
