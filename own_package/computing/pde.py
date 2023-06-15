import numpy as np


def periodic(u):
    return u


def reflective(u):
    if len(np.shape(u)) != 1:
        u[:, 0] = u[:, 1]
        u[:, -1] = u[:, -2]
    else:
        u[0] = u[1]
        u[-1] = u[-2]
    return u


boundary_dict = {}
boundary_dict["periodic"] = periodic
boundary_dict["reflective"] = reflective


def diffusion_solve(
    u0,
    dx,
    tlim=1.0,
    tdiff=None,
    tcool=None,
    N_t=None,
    r=0.1,
    D=1.0,
    cooling_flag=False,
    boundary="periodic",
    return_series=None,
):
    peak_value = np.max(u0)
    amb_value = np.min(u0)

    dt = r * dx * dx / np.max(D)
    u = np.copy(u0)

    # * Check for cooling_flag
    if cooling_flag:
        if tcool in None:
            raise ValueError(
                "pde.py::diffusion_solve(): c_diff is required with cooling_flag as True..."
            )

        def cool_rate(u):
            cool = np.zeros_like(u)

            cond = peak_value > u
            cond *= u > np.sqrt(peak_value * amb_value)

            cool[cond] = 1 / tcool

            return cool

        print(f"{tdiff = }")
        print(f"{tcool = }")

        dt = min(dt, tcool / 25)
        N_t_calc = int(2 * tcool / dt)

    else:

        def cool_rate(u):
            return 0.0

        N_t_calc = int(tlim / dt)

    if N_t is not None:
        N_t_calc = int(N_t)
        dt = tlim / N_t_calc

    # * Check for return series
    if return_series is not None:
        if not (
            # isinstance(return_series, list) or isinstance(return_series, np.ndarray)
            isinstance(return_series, int)
        ):
            raise TypeError(
                "pde.py::diffusion_solve(): return_series has to be a list or numpy.ndarray, if not None..."
            )

    print(f"{N_t_calc = }")

    result_dict = {}
    result_dict["u"] = []
    result_dict["u_return_t"] = [0]
    result_dict["u"].append(u0.tolist())

    peak_list = []
    time_list = []
    cold_gas_list = []

    r_arr = dt * D / dx**2
    if len(r_arr) != 1:
        r_arr = r_arr[:, np.newaxis]

    for t in range(N_t_calc):
        u += (np.roll(u, -1) - 2 * u + np.roll(u, 1)) * r_arr + dt * cool_rate(u)

        u = boundary_dict[boundary](u)

        u[u > peak_value] = peak_value

        if return_series is not None:
            if t % int(N_t_calc / return_series) == 0:
                result_dict["u"].append(np.copy(u).tolist())
                result_dict["u_return_t"].append(t)

        if cooling_flag:
            cold_gas_list.append(np.sum(u[u > np.sqrt(peak_value * amb_value)]))

        peak_list.append(u.max())
        time_list.append(t)

    peak_list = np.array(peak_list)
    time_list = np.array(time_list)
    cold_gas_list = np.array(cold_gas_list)

    if cooling_flag:
        result_dict["tcool"] = tcool
        result_dict["cold_gas_list"] = cold_gas_list.tolist()

    result_dict["u"].append(np.copy(u).tolist())
    result_dict["u_return_t"].append(N_t_calc - 1)

    result_dict["tdiff"] = tdiff
    result_dict["N_t"] = N_t_calc
    result_dict["dt"] = dt

    result_dict["peak_list"] = peak_list.tolist()
    result_dict["time_list"] = time_list.tolist()

    return result_dict


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    L = 500

    peak_value = 100
    amb_value = 1

    x = np.linspace(-100, 100, L)
    u0 = np.ones(L) * amb_value

    w = 5
    D = 1.0
    c_diff = 0.01  # Ratio t_diff/t_cool

    cond = x < 0
    u0[cond] = peak_value

    dx = x[1] - x[0]
    r = 0.25

    result_dict = diffusion_solve(
        u0,
        dx=dx,
        # c_diff=c_diff,
        cooling_flag=False,
        boundary="reflective",
    )

    fig, ax = plt.subplots(figsize=(20, 10))

    ax.plot(x, u0, linewidth=5, linestyle="dotted")
    ax.plot(x, result_dict["u"], linewidth=3, linestyle="solid")

    ax.axhline(50.5, linestyle="dotted")

    # ax.set_yscale("log")

    plt.show()
