import numpy as np
import scipy.ndimage as ndi


def dot_product(A, B):
    A_dot_B = A[0] * B[0]
    A_dot_B += A[1] * B[1]
    A_dot_B += A[2] * B[2]

    A_mag = A[0] ** 2 + A[1] ** 2 + A[2] ** 2
    B_mag = B[0] ** 2 + B[1] ** 2 + B[2] ** 2

    A_mag = np.sqrt(A_mag)
    B_mag = np.sqrt(B_mag)

    AB_cos = A_dot_B / (A_mag * B_mag)

    return A_dot_B, AB_cos


def gradient(A, *args, **kwargs):
    grad = np.gradient(A, *args, **kwargs)
    # return [grad[1], grad[0], grad[2]]
    return grad


def magnitude(A):
    dim = len(A)

    A_mag = 0.0

    for i in range(dim):
        A_mag += A[i] ** 2

    return np.sqrt(A_mag)


def radial_vector(A_list):
    L = np.array(np.shape(A_list[0]))
    dim = len(L)

    mid = (L / 2).astype(int)

    r = [np.array(range(L[i])) - mid[i] for i in range(dim)]

    # print(len(r))
    # print(tuple(r))

    R_mesh = np.meshgrid(*r)

    # print(np.shape(R_mesh))

    R = 0
    for i in range(dim):
        R += R_mesh[i] ** 2
    R = np.sqrt(R)

    AdotR = 0
    for i in range(dim):
        if i == 0:
            AdotR += A_list[0] * R_mesh[1]
        elif i == 1:
            AdotR += A_list[1] * R_mesh[0]
        else:
            AdotR += A_list[i] * R_mesh[i]

    AdotR = AdotR / R

    return AdotR


def smoothen(A, window):
    A_smooth = np.convolve(A, np.ones(window) / window, mode="valid")
    return A_smooth


def array_column_sort(A, axis=0):
    return A[A[:, axis].argsort()]


def match_array(t_A, A, t_B, B):
    if len(t_A) >= len(t_B):
        # * Short array
        short_t = np.copy(t_B)
        short_arr = np.copy(B)

        # * Long array
        long_t = np.copy(t_A)
        long_arr = np.copy(A)
    else:
        # * Short array
        short_t = np.copy(t_A)
        short_arr = np.copy(A)

        # * Long array
        long_t = np.copy(t_B)
        long_arr = np.copy(B)

    # #* Placeholder for final matched array
    # match_arr = np.ones_like(short_arr, dtype=float) * -1

    # * Array like long_arr, for index of match_arr corresponding to each element
    ind_arr = np.ones_like(long_arr) * -1

    def elements_greater_than(i):
        return np.sum(np.greater_equal(i, short_t))

    ind_arr += np.vectorize(elements_greater_than)(long_t)

    # * Averaging the elements with same ind_arr values

    def select_average(i):
        return np.average(long_arr[np.argwhere(ind_arr == i)])

    match_arr = np.vectorize(select_average)(np.array(range(len(short_arr))))
    # print(long_arr[np.argwhere(ind_arr==1)])

    return match_arr


def gaussian_filter(A, sigma=1.0):
    A_gauss = ndi.gaussian_filter(A, sigma=sigma * 0.5)
    # In sp.ndimage.gaussian_filter(), sigma of 1.0 give a standard deviation of 2.0 cells.

    return A_gauss


def make_array_periodic(arr):
    shape = np.array(arr.shape)

    # N_dim = len(shape)

    # shape = (shape / 1.1).astype(int)
    padded_shape = shape * 3
    padded_arr = np.zeros(padded_shape, dtype=arr.dtype)
    if len(shape) == 3:
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    padded_arr[
                        shape[0] * i : shape[0] * (i + 1),
                        shape[1] * j : shape[1] * (j + 1),
                        shape[2] * k : shape[2] * (k + 1),
                    ] = arr[: shape[0], : shape[1], : shape[2]]
    else:
        raise ValueError(
            "array_operations::surround_array(): Only 3D arrays are supported..."
        )

    return padded_arr


def radial_profile(arr, center=None, bins=10):
    L = np.array(np.shape(arr))

    if len(L) not in [2, 3]:
        raise ValueError(
            "radial_profile()::array_operations: Array dimensions should 2 or 3..."
        )

    if center is None:
        center = (L / 2).astype(int)

    # Find the ends, so that center is at 0,0
    box_start = -2 * center / L
    box_end = box_start + 2

    if len(L) == 2:
        X, Y = np.meshgrid(
            np.linspace(box_start[0], box_end[0], num=L[0]),
            np.linspace(box_start[1], box_end[1], num=L[1]),
        )

        R = np.sqrt(X * X + Y * Y)

    else:  # len(L) == 3
        X, Y, Z = np.meshgrid(
            np.linspace(box_start[0], box_end[0], num=L[0]),
            np.linspace(box_start[1], box_end[1], num=L[1]),
            np.linspace(box_start[2], box_end[2], num=L[2]),
        )

        R = np.sqrt(X * X + Y * Y + Z * Z)

    R_bin_edges = np.linspace(R.min(), R.max(), num=bins + 1)

    R_arr = R_bin_edges[:-1] + np.diff(R_bin_edges) / 2
    arr_rad = np.zeros_like(R_arr)

    for i_r, _ in enumerate(R_arr):
        cond_i = (R >= R_bin_edges[i_r]) * (R < R_bin_edges[i_r + 1])

        arr_rad[i_r] = np.average(arr[cond_i])

    return_dict = {}
    return_dict["r"] = R_arr
    return_dict["radial_profile"] = arr_rad

    return return_dict


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    A = np.array([0, 1, 4, 1, 4])
    t_A = np.array([0, 1, 5, 6, 9])

    B = np.array([0, 4, 2, 1, 4, 15, 9, 7, 7, 9])
    t_B = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])

    match_arr = match_array(t_A, A, t_B, B)

    print(f"{A         = }")
    print(f"{B         = }\n")
    print(f"{t_A       = }")
    print(f"{t_B       = }\n")
    # print(f'{ind_arr   = }')
    print(f"{match_arr = }")

    # A_img = np.random.random((25,25))
    A_img = np.zeros((25, 25), dtype=float)
    A_img[12, 12] = 1.0

    A_img_gauss = gaussian_filter(A_img, sigma=1.0)

    plt.figure()
    plt.imshow(A_img)

    plt.figure()
    plt.imshow(A_img_gauss)
