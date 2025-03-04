import numpy as np
from timebudget import timebudget
from scipy.fft import fft, ifft

timebudget.set_quiet()  # don't show measurements as they happen
# timebudget.report_at_exit()  # Generate report when the program exits


@timebudget
def coloumb(sigma, x, k_coloumb=1.0):
    E = []
    dx = x[1] - x[0]
    for i in range(len(x)):
        r = x - x[i]
        cond = r != 0
        E_i = np.sum(-k_coloumb * np.sign(r[cond]) * sigma[cond] * dx / r[cond] ** 2)
        E.append(E_i)

    E = np.array(E)

    return E


@timebudget
def potential_slow(sigma, x):
    E = []
    for i in range(len(x)):
        r = np.abs(x - x[i])
        cond = r != 0
        E_i = np.trapz(sigma[cond], x=x[cond])
        E.append(E_i)

    E = np.array(E)

    return E


@timebudget
def solve_poisson_eqn(charge_density, dx):
    # Compute the shape of the charge density array
    shape = charge_density.shape

    # Compute the wave numbers in each dimension
    kx = 2 * np.pi * np.fft.fftfreq(shape[0], dx)
    # ky = 2 * np.pi * np.fft.fftfreq(shape[1], dx)
    # kz = 2 * np.pi * np.fft.fftfreq(shape[2], dx)

    # Compute the squared wave numbers
    # kx2, ky2, kz2 = np.meshgrid(kx**2, ky**2, kz**2, indexing="ij")

    # Compute the Fourier transform of the charge density
    rho_hat = fft(charge_density)

    plt.figure()
    plt.plot(kx, rho_hat)
    plt.xscale("symlog")

    print(kx[np.argmax(rho_hat)])

    # Solve the Poisson equation in Fourier space
    # phi_hat = -rho_hat / (kx2 + ky2 + kz2)
    phi_hat = np.zeros_like(kx, dtype=complex)
    phi_hat[kx != 0] = -rho_hat[kx != 0] / (kx[kx != 0] ** 2)

    # Compute the inverse Fourier transform to obtain the potential
    potential = ifft(phi_hat).real

    return potential, kx


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    x = np.linspace(-0.5, 0.5, num=10000)
    # sigma = np.zeros_like(x)

    # sigma[np.abs(x) < 0.01] = 1.0

    sigma = np.sin(2 * 2 * np.pi * x) + 1.0

    V_slow = potential_slow(sigma, x)
    V_fft, kx = solve_poisson_eqn(sigma, x[1] - x[0])

    plt.figure()
    plt.plot(x, sigma)

    plt.figure()
    plt.plot(x, V_slow, label="potential_slow")
    plt.legend()

    plt.figure()
    plt.plot(x, V_fft, label="potential_fft")
    plt.legend()

    timebudget.report(reset=True)
