import numpy as np


def rotate_vector(vec, theta=0):
    new_vec = np.zeros_like(vec)

    new_vec[0] = vec[0] * np.cos(theta) - vec[1] * np.sin(theta)
    new_vec[1] = vec[0] * np.sin(theta) + vec[1] * np.cos(theta)

    return new_vec


def flatten(S):
    if S == []:
        return S
    if isinstance(S[0], list):
        return flatten(S[0]) + flatten(S[1:])
    return S[:1] + flatten(S[1:])


def fractal_section(section_list, min_length=0.1, theta=np.pi / 4, dir=1):
    length = np.sum((section_list[1] - section_list[0]) ** 2)
    length = np.sqrt(length)

    # theta_i = theta * 0.5
    theta_i = theta * 1.0

    if ((0.5 * (length / np.cos(theta_i))) < min_length) or (theta_i < 0.01 * np.pi):
        return section_list
    else:
        mid_point = section_list[1] - section_list[0]
        mid_point /= np.sqrt(np.sum(mid_point**2))

        mid_point = section_list[0] + 0.5 * (length / np.cos(theta_i)) * rotate_vector(
            mid_point, dir * theta_i
        )

        # print(section_list)
        # print(mid_point)
        # print(length)
        # print(length / np.cos(theta))
        # print("\n")

        return [
            fractal_section([section_list[0], mid_point], min_length, theta_i, dir=1),
            fractal_section([mid_point, section_list[1]], min_length, theta_i, dir=-1),
        ]


def plot_fractal(
    lstream=1.0,
    new_fig=True,
    fig=None,
    ax=None,
):
    a = np.zeros(2, dtype=float)
    b = np.zeros(2, dtype=float)
    b[0] = lstream

    ret_list = fractal_section([a, b], theta=np.arccos(3 / 8), min_length=0.05)
    ret_list = flatten(ret_list)

    print(f"{np.shape(ret_list) = }")

    ret_list = np.array(ret_list)

    # a /= lstream
    # b /= lstream
    # ret_list /= lstream

    if new_fig:
        fig, ax = plt.subplots(nrows=1, ncols=1)

    ax.scatter([a[0], b[0]], [a[1], b[1]])
    ax.plot(ret_list[:, 0], ret_list[:, 1], label=f"l_stream = {lstream}")
    ax.axis("equal")

    N = np.shape(ret_list)[0] - 1
    dl = np.sum((ret_list[1, :] - ret_list[0, :]) ** 2)
    dl = np.sqrt(dl)

    del ret_list

    return fig, ax, N * dl


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    frac_length_arr = []
    lstream_arr = np.linspace(0.05, 1.0, num=100)
    # lstream_arr = np.linspace(0.05, 100.0, num=2)

    fig, ax = plt.subplots(nrows=1, ncols=1)

    for lstream in lstream_arr:
        fig, ax, frac_length = plot_fractal(
            lstream=lstream,
            new_fig=False,
            fig=fig,
            ax=ax,
        )

        frac_length_arr.append(frac_length)

    frac_length_arr = np.array(frac_length_arr)

    # ax.legend()

    plt.figure()

    plt.plot(frac_length_arr, frac_length_arr / lstream_arr)
    plt.scatter(frac_length_arr, frac_length_arr / lstream_arr)
    # plt.plot(frac_length_arr, 2.5 * frac_length_arr + 1.0)

    # plt.xlim(0, 1.0)
    # plt.ylim(0.9, 5.0)
