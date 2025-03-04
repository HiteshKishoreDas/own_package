import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as si


def plot_fractal():
    x = np.linspace(0, 4 * np.pi, num=int(1e8))
    y = np.zeros_like(x)

    plt.figure()

    def fractal_sin(x, y, n=2, lp=[2 * np.pi]):
        if n == 0:
            return x, y, lp

        elif n == 1:
            yp = np.sin(x)

            dxp = np.array(list(np.diff(x)) + [x[1] - x[0]])
            dyp = np.array(list(np.diff(yp)) + [0.0])

            # plt.plot(x, yp, label="yp_1")

            return x, yp, lp + [np.trapz(np.sqrt(dxp**2 + dyp**2))]

        else:
            xp, yp, lp = fractal_sin(x, y, n=n - 1)
            # print(f"{n = }:{lp = }")

            dxp = np.array(list(np.diff(xp)) + [x[1] - x[0]])
            dyp = np.array(list(np.diff(yp)) + [0.0])

            # print(dxp)
            # print(dyp)

            slope = np.arctan(dyp / dxp)

            y_int = si.cumulative_trapezoid(np.sqrt(dxp**2 + dyp**2), initial=0.0)

            l = np.sin(y_int)

            xp += -l * np.sin(slope)
            yp += l * np.cos(slope)

            lp += [np.trapz(yp)]

            # plt.plot(xp, yp, label=f"yp_{n}")  # , s=1.0)
            # plt.plot(xp, y_int, label="yint")
            # plt.plot(xp, y_int, label="l")

            return xp, yp, lp

    plt.plot(x, y, linestyle=":")

    xp, yp, lp = fractal_sin(x, y, n=10)

    plt.plot(xp, yp, linestyle=":")

    plt.legend()

    plt.figure()

    plt.plot(range(len(lp)), lp)

    plt.show()


def path_length(x, y):
    dxp = np.diff(x)
    dyp = np.diff(y)

    return np.sum(np.sqrt(dxp**2 + dyp**2))


if __name__ == "__main__":
    # plot_fractal()

    x = np.linspace(0, 2 * np.pi, num=1000)

    n = np.linspace(1, 100, num=100)
    # k = 2 * np.pi * n

    plt.figure()

    slope_list = []
    inter_list = []

    amp = list(range(1, 11))

    for a in amp:
        path_list = []
        wave_list = []
        for i in n:
            wave_list.append(i * 2 * np.pi)
            path_list.append(path_length(a * np.sin(i * x), x))

        fit = np.polyfit(x=wave_list, y=path_list, deg=1)

        slope_list.append(fit[0])
        inter_list.append(fit[1])

        plt.plot(wave_list, path_list)

# %%

amp = np.array(amp)

plt.figure()
plt.scatter(amp, slope_list, label="slope")
plt.scatter(amp, inter_list, label="intercept")

# fit_slope = np.polyfit(x=np.log10(amp), y=np.log10(slope_list), deg=1)
fit_slope = np.polyfit(x=amp, y=slope_list, deg=1)
fit_inter = np.polyfit(x=amp, y=inter_list, deg=1)
# fit_inter = np.polyfit(x=np.log10(amp), y=np.log10(inter_list), deg=1)

plt.plot(amp, fit_slope[0] * amp + fit_slope[1])
# plt.plot(amp, (amp ** fit_slope[0]) * 10 ** fit_slope[1])
# plt.plot(amp, (amp ** fit_inter[0]) * 10 ** fit_inter[1])
plt.plot(amp, fit_inter[0] * amp + fit_inter[1])

print(f"slope = {fit_slope[0]}A + {fit_slope[1]}")
print(f"inter = {fit_inter[0]}A + {fit_inter[1]}")

plt.legend()

# plt.loglog()

# %%
