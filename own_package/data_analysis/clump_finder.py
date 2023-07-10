import numpy as np
import matplotlib.pyplot as plt


def neighbourhood(
    i,
    j,
    L,
    type="edges",
    # type="diagonal",
):
    if type == "diagonal":
        if (i > 0) and (i < L[0] - 1):
            sl_i = slice(i - 1, i + 2)
        elif i == 0:
            sl_i = slice(i, i + 2)
        elif i == L[0] - 1:
            sl_i = slice(i - 1, i + 1)

        if (j > 0) and (j < L[1] - 1):
            sl_j = slice(j - 1, j + 2)
        elif j == 0:
            sl_j = slice(j, j + 2)
        elif j == L[1] - 1:
            sl_j = slice(j - 1, j + 1)

        return sl_i, sl_j

    elif type == "edges":
        neigh = np.zeros(L, dtype=bool)

        if (i > 0) and (i < L[0] - 1):
            N1 = -1
            N2 = 2
        elif i == 0:
            N1 = 0
            N2 = 2
        elif i == L[0] - 1:
            N1 = -1
            N2 = 1

        if (j > 0) and (j < L[1] - 1):
            M1 = -1
            M2 = 2
        elif j == 0:
            M1 = 0
            M2 = 2
        elif j == L[1] - 1:
            M1 = -1
            M2 = 1

        neigh[i, j + M1 : j + M2] = True
        neigh[i + N1 : i + N2, j] = True

        return neigh


def clump_finder_multiply(arr):
    temp_arr = np.copy(arr).astype(float)  # + 1
    L = np.shape(temp_arr)

    # for _ in range(int(np.max(L) / 2)):
    for _ in range(4):  #
        temp_arr *= temp_arr
        temp_arr *= (
            np.roll(temp_arr, 1, axis=0)
            + np.roll(temp_arr, -1, axis=0)
            + np.roll(temp_arr, 1, axis=1)
            + np.roll(temp_arr, -1, axis=1)
            + np.roll(temp_arr, (1, 1), axis=(0, 1))
            + np.roll(temp_arr, (1, -1), axis=(0, 1))
            + np.roll(temp_arr, (-1, 1), axis=(0, 1))
            + np.roll(temp_arr, (-1, -1), axis=(0, 1))
        )
        # To scale things down a bit and prevent overflow
        temp_arr = temp_arr**0.1

    temp_arr = np.abs(temp_arr)

    plt.figure()
    plt.imshow(np.log10(temp_arr), cmap="plasma")
    # plt.imshow(temp_arr, cmap="plasma")
    plt.colorbar()

    clump_arr = np.zeros_like(temp_arr)
    clump_count = 1

    for i in range(1, L[0] - 1):
        for j in range(1, L[1] - 1):
            if temp_arr[i, j] != 0:
                if temp_arr[i, j] == np.max(temp_arr[neighbourhood(i, j, L)]):
                    # Check if the cell has the highest value in neighbourhood

                    if np.sum(clump_arr[neighbourhood(i, j, L)]) == 0:
                        # Check if there was another cell which is
                        # already filled as the maximum

                        print(f"Hello! I'm in.. {i, j}")
                        clump_arr[i, j] = clump_count
                        clump_count += 1

    return clump_arr, clump_count - 1  # .astype(bool).astype(int)


def clump_finder_traverse(arr):
    temp_arr_for = np.zeros_like(arr)
    L = np.shape(temp_arr_for)

    clump_count = 1

    for i in range(L[0]):
        for j in range(L[1]):
            if arr[i, j] == 1:
                if temp_arr_for[i, j] == 0:
                    if np.max(temp_arr_for[neighbourhood(i, j, L)]) == 0:
                        temp_arr_for[neighbourhood(i, j, L)] = (
                            clump_count * arr[neighbourhood(i, j, L)]
                        )
                        clump_count += 1
                    else:
                        temp_arr_for[neighbourhood(i, j, L)] = (
                            np.max(temp_arr_for[neighbourhood(i, j, L)])
                            * arr[neighbourhood(i, j, L)]
                        )

    plt.figure()
    plt.imshow(
        temp_arr_for,
        cmap="Paired",
        # vmax=5,
        # vmin=0,
    )
    plt.title(f"Forward, clump: {np.max(temp_arr_for)}")
    plt.colorbar()

    clump_list = [np.max(temp_arr_for)]

    for n in range(np.max(L) // 2):
        for i in range(L[0]):
            for j in range(L[1]):
                if temp_arr_for[i, j] != 0:
                    neigh = temp_arr_for[neighbourhood(i, j, L)]
                    temp_arr_for[i, j] = np.min(neigh[neigh != 0])

        clump_list.append(len(set(np.ravel(temp_arr_for))))

        # plt.figure()
        # plt.imshow(
        #     temp_arr_for,
        #     cmap="Paired",
        #     # vmax=5,
        #     # vmin=0,
        # )
        # plt.title(f" {n+2}th pass: clumps: {clump_list[-1]}")
        # plt.colorbar()

    # temp_arr_back = np.zeros_like(arr)
    # L = np.shape(temp_arr_for)

    # clump_count = 1

    # for i in range(L[0] - 1, -1, -1):
    #     for j in range(L[1] - 1, -1, -1):
    #         if arr[i, j] == 1:
    #             if temp_arr_back[i, j] == 0:
    #                 if np.max(temp_arr_back[neighbourhood(i, j, L)]) == 0:
    #                     temp_arr_back[neighbourhood(i, j, L)] = (
    #                         clump_count * arr[neighbourhood(i, j, L)]
    #                     )
    #                     clump_count += 1
    #                 else:
    #                     temp_arr_back[neighbourhood(i, j, L)] = (
    #                         np.max(temp_arr_back[neighbourhood(i, j, L)])
    #                         * arr[neighbourhood(i, j, L)]
    #                     )

    # plt.figure()
    # plt.imshow(temp_arr_back, cmap="Paired", vmax=5, vmin=0)
    # plt.title("Backward")
    # plt.colorbar()

    # temp_arr[temp_arr == -1] = 0

    return temp_arr_for, np.max(temp_arr_for), clump_list


if __name__ == "__main__":
    import time

    N = 1000
    M = 1000

    fixed_arr = np.zeros((N, M), dtype=int)
    fixed_arr[1:3, 1:3] = 1
    fixed_arr[N - 5 : N - 3, M - 4 : M] = 1
    fixed_arr[N - 4 : N - 2, M - 7 : M] = 1
    fixed_arr[N - 2 : N - 1, M - 4 : M - 2] = 1
    fixed_arr[5, 3] = 1
    fixed_arr[8, 2] = 1

    fixed_arr = np.random.randint(2, size=(N, M))

    plt.figure()
    plt.imshow(fixed_arr, cmap="gray")

    # clump_arr, clump_count = clump_finder_multiply(fixed_arr)

    time_a = time.time()
    clump_arr, clump_count, clump_list = clump_finder_traverse(fixed_arr)
    time_b = time.time()

    print(f"time for hi-tech:{time_b-time_a}")

    clump_arr[clump_arr == 0] = -5

    plt.figure()
    plt.imshow(
        clump_arr,
        cmap="Paired",
        # vmin=0,
        # vmax=5,
    )
    plt.title(f"clump count = {clump_list[-1]-1}")
    plt.colorbar()

    plt.figure()
    plt.plot(range(len(clump_list)), clump_list)
    plt.yscale("log")
    plt.xscale("log")

    lake_map_arr = np.copy(fixed_arr)

    def find_lake(i, j):
        if i < 0 or i >= lake_map_arr.shape[0]:
            return False

        if j < 0 or j >= lake_map_arr.shape[1]:
            return False

        if lake_map_arr[i, j] == 0:
            return False

        lake_map_arr[i, j] = 0

        find_lake(i - 1, j)
        find_lake(i + 1, j)
        find_lake(i, j + 1)
        find_lake(i, j - 1)

        return True

    def find_lakes():
        lake_counter = 0

        for i in range(lake_map_arr.shape[0]):
            for j in range(lake_map_arr.shape[1]):
                if find_lake(i, j):
                    lake_counter += 1

        return lake_counter

    time_a = time.time()
    print(find_lakes())
    time_b = time.time()

    print(f"time for caustic:{time_b-time_a}")
