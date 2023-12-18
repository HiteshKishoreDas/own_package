import numpy as np


def coloumb(sigma, x):
    E = []
    for i in range(len(x)):
        r = x - x[i]
        cond = r != 0
        E_i = np.trapz(-np.sign(r[cond]) * sigma[cond] / r[cond] ** 2, x=x[cond])
        E.append(E_i)

    E = np.array(E)

    return E


def electrostatic_energy(
    x,
    sigma,
    debug=False,
):
    pair_dist = np.subtract.outer(x, x) ** 2
    pair_charge = np.multiply.outer(sigma, sigma)

    cond = pair_dist != 0
    energy = pair_charge / pair_dist

    energy *= cond
    energy[np.isnan(energy)] = 0.0
    energy = np.sum(energy, axis=0)

    if debug:
        plt.figure()
        plt.plot(x, sigma)
        plt.xlabel("x")
        plt.xlabel(r"$\sigma$")

        plt.figure()
        plt.imshow(pair_dist)
        plt.title("Distance^2")

        plt.figure()
        plt.imshow(pair_charge)
        plt.title("sigma^2")

        plt.figure()
        plt.imshow(np.log10(pair_charge / pair_dist), vmin=-2)
        # plt.imshow(pair_charge / pair_dist, vmin=-2)
        plt.colorbar()
        plt.title("sigma^2/r^2")

        plt.figure()
        plt.plot(x, energy)
        plt.xlabel("x")
        plt.xlabel(r"E")

    return energy


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    x = np.linspace(-1, 1, num=101)
    # sigma = np.sin(np.pi * x)
    sigma = np.abs(np.sin(np.pi * x))

    _ = electrostatic_energy(x, sigma, debug=True)
