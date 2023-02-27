import numpy as np
import matplotlib
import matplotlib as mt


import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import cmasher as cr


def new_plot():

    fig = plt.figure(figsize=(10, 10))
    ax = plt.axes(projection="3d")

    return fig, ax


def const_alpha(x, cut=0.0, cut_above=False, log_flag=False):

    alpha_0 = 0.5
    return np.ones_like(x) * alpha_0


def poly_alpha(c_arr, order=2, alpha0=1.0, log_flag=False, cut=None, cut_above=False):

    # alpha0 = 1.0

    if log_flag:
        arr = np.log10(c_arr)
        arr_min = arr.min()
        arr_max = arr.max()

    else:
        arr = np.copy(c_arr)
        arr_min = arr.min()
        arr_max = arr.max()

    # Returns min() if cut is None
    # Returns cut if not None
    if cut_above:
        c_min = arr_min
        c_max = cut or arr_max
        if c_max < arr_max:
            c_max = arr_max
    else:
        c_min = cut or arr_min
        c_max = arr_max
        if c_min > arr_min:
            c_min = arr_min

    alp = alpha0 * (arr - c_min) ** order / (c_max - c_min) ** order

    if cut_above:
        alp[c_arr > (c_arr.min() + (cut or 0))] = 0.0
    else:
        alp[c_arr < (c_arr.min() + (cut or 0))] = 0.0

    alp[c_arr == 0] = 0.0

    return alp


def lin_alpha(c_arr, log_flag=False, cut=0.0, cut_above=False):

    alpha0 = 1.0

    if log_flag:
        log_c_arr = np.log10(c_arr)
        alp = (
            alpha0 * (log_c_arr - log_c_arr.min()) / (log_c_arr.max() - log_c_arr.min())
        )
    else:
        alp = alpha0 * (c_arr - c_arr.min()) / (c_arr.max() - c_arr.min())

    if cut_above:
        alp[c_arr > (c_arr.min() + cut)] = 0.0
    else:
        alp[c_arr < (c_arr.min() + cut)] = 0.0

    alp[c_arr == 0] = 0.0

    return alp


def make_color(c_arr, alpha_arr, cmap_name, log_flag=False):

    cmap = mt.cm.get_cmap(cmap_name)

    if log_flag:
        cb_qnt = np.copy(np.log10(c_arr))
    else:
        cb_qnt = np.copy(c_arr)

    line_col = cmap(cb_qnt / cb_qnt.max())

    line_col[:, 3] = alpha_arr

    return line_col


def make_color_voxel(c_arr, alpha_arr, cmap_name, log_flag=False):

    cmap = mt.cm.get_cmap(cmap_name)

    if log_flag:
        cb_qnt = np.copy(np.log10(c_arr))
    else:
        cb_qnt = np.copy(c_arr)

    line_col = cmap(cb_qnt / cb_qnt.max())

    line_col[:, :, :, 3] = alpha_arr

    return line_col


def make_plot_list(inp_arr, col_data, cond_arr):

    L = np.shape(inp_arr)

    plot_list = []

    for i in range(L[0]):
        for j in range(L[1]):
            for k in range(L[2]):

                if cond_arr[i, j, k]:
                    plot_list.append([i, j, k, col_data[i, j, k]])

    return plot_list


# TODO: Add the interactive feature in this function instead

# TODO: Add the feature to plot using voxel plot instead of scatter


def scatter_3d(
    inp_arr,
    cut,
    col_data,
    cmap=cr.rainforest,
    above_cut=True,
    alpha_fn=const_alpha,
    pnt_size=50,
    log_flag=False,
    view=[30, -60],
    new_fig=True,
    fig=None,
    ax=None,
):

    if new_fig:
        fig, ax = new_plot()

    if above_cut:
        cond_arr = inp_arr > cut
    else:
        cond_arr = inp_arr < cut

    plot_list = make_plot_list(inp_arr, col_data, cond_arr)
    plot_list = np.array(plot_list)

    i_arr = plot_list[:, 0]
    j_arr = plot_list[:, 1]
    k_arr = plot_list[:, 2]

    c_arr = plot_list[:, 3]
    alpha_arr = alpha_fn(c_arr, log_flag=log_flag)

    color = make_color(c_arr, alpha_arr, cmap, log_flag=log_flag)

    sc = ax.scatter3D(
        i_arr,
        j_arr,
        k_arr,
        c=color,
        s=pnt_size,
        edgecolors="None",
        cmap=cmap,
        depthshade=True,
    )

    ax.view_init(elev=view[0], azim=view[1])

    return fig, ax, sc


def render_scatter_3d(
    inp_arr,
    cmap=cr.rainforest,
    alpha_fn=const_alpha,
    pnt_size=50,
    log_flag=False,
    view=[30, -60],
    coord=[None, None, None],
    new_fig=True,
    fig=None,
    ax=None,
    **kwargs,
):

    if new_fig:
        fig, ax = new_plot()

    if None in coord:
        L = np.shape(inp_arr)
        i = np.array(range(L[0]))
        j = np.array(range(L[1]))
        k = np.array(range(L[2]))

        i_arr, j_arr, k_arr = np.meshgrid(i, j, k)

        i_arr = np.ravel(i_arr, order="C")
        j_arr = np.ravel(j_arr, order="C")
        k_arr = np.ravel(k_arr, order="C")
    else:

        i_arr = coord[0]
        j_arr = coord[1]
        k_arr = coord[2]

        i_arr = np.ravel(i_arr, order="C")
        j_arr = np.ravel(j_arr, order="C")
        k_arr = np.ravel(k_arr, order="C")

    c_arr = np.ravel(inp_arr, order="C")

    # TODO: Add log scaling in alpha_fn
    alpha_arr = alpha_fn(c_arr, log_flag=log_flag)

    color_arr = make_color(c_arr, alpha_arr, cmap, log_flag=log_flag)

    sc = ax.scatter3D(
        i_arr,
        j_arr,
        k_arr,
        c=color_arr,
        s=pnt_size,
        edgecolors="None",
        cmap=cmap,
        depthshade=True,
        **kwargs,
    )

    ax.view_init(elev=view[0], azim=view[1])

    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    return fig, ax, sc


def render_voxel_3d(
    inp_arr,
    cmap=cr.rainforest,
    alpha_fn=const_alpha,
    log_flag=False,
    view=[30, -60],
    vertices=[None, None, None],
    new_fig=True,
    fig=None,
    ax=None,
):

    if new_fig:
        fig, ax = new_plot()

    if None in vertices:
        L = np.shape(inp_arr)
        i = np.array(range(L[0] + 1))
        j = np.array(range(L[1] + 1))
        k = np.array(range(L[2] + 1))

        i_arr, j_arr, k_arr = np.meshgrid(i, j, k)

        # i_arr = np.ravel(i_arr, order='C')
        # j_arr = np.ravel(j_arr, order='C')
        # k_arr = np.ravel(k_arr, order='C')
    else:

        i_arr = vertices[0]
        j_arr = vertices[1]
        k_arr = vertices[2]

        # i_arr = np.ravel(i_arr, order='C')
        # j_arr = np.ravel(j_arr, order='C')
        # k_arr = np.ravel(k_arr, order='C')

    # c_arr = np.ravel(inp_arr, order='C')
    c_arr = np.copy(inp_arr)

    # TODO: Add log scaling in alpha_fn
    alpha_arr = alpha_fn(c_arr, log_flag=log_flag)

    color = make_color_voxel(c_arr, alpha_arr, cmap, log_flag=log_flag)

    print(np.shape(color))

    for i in range(L[0]):
        print(f"i: {i}")
        for j in range(L[1]):
            for k in range(L[2]):

                ax.voxels(
                    i_arr[i : i + 1, j : j + 1, k : k + 1],
                    j_arr[i : i + 1, j : j + 1, k : k + 1],
                    k_arr[i : i + 1, j : j + 1, k : k + 1],
                    filled=np.ones((1, 1, 1), dtype=bool),
                    facecolors=color[i, j, k],
                    edgecolors=color[i, j, k],
                    cmap=cmap,
                )

    #  filled=(np.ones_like(inp_arr)).astype(bool),           \

    ax.view_init(elev=view[0], azim=view[1])

    ax.w_xaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_yaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))
    ax.w_zaxis.set_pane_color((1.0, 1.0, 1.0, 0.0))

    return fig, ax


def full_render(
    inp_arr,
    view_dir,
    cmap=cr.rainforest,
    fig=None,
    ax=None,
):
    def alpha_plot(c_arr, log_flag=False):
        return poly_alpha(c_arr, log_flag=log_flag, order=1, cut=5, alpha0=0.75)

    def alpha_plot_smooth1(c_arr, log_flag=False):
        return poly_alpha(c_arr, log_flag=log_flag, order=1, cut=5, alpha0=0.6)

    def alpha_plot_smooth2(c_arr, log_flag=False):
        return poly_alpha(c_arr, log_flag=log_flag, order=1, cut=5, alpha0=0.4)

    def alpha_plot_smooth3(c_arr, log_flag=False):
        return poly_alpha(c_arr, log_flag=log_flag, order=1, cut=5, alpha0=0.2)

    fig, ax, sc = render_scatter_3d(
        inp_arr=inp_arr, alpha_fn=alpha_plot, pnt_size=1, cmap=cmap, view=[30, view_dir]
    )
    print("First layer is done!...")

    fig, ax, sc = render_scatter_3d(
        inp_arr=inp_arr,
        alpha_fn=alpha_plot_smooth1,
        pnt_size=2,
        cmap=cmap,
        new_fig=False,
        ax=ax,
        fig=fig,
        view=[30, view_dir],
    )
    print("Second layer is done!...")

    fig, ax, sc = render_scatter_3d(
        inp_arr=inp_arr,
        alpha_fn=alpha_plot_smooth2,
        pnt_size=3,
        cmap=cmap,
        new_fig=False,
        ax=ax,
        fig=fig,
        view=[30, view_dir],
    )
    print("Third layer is done!...")

    fig, ax, sc = render_scatter_3d(
        inp_arr=inp_arr,
        alpha_fn=alpha_plot_smooth3,
        pnt_size=4,
        cmap=cmap,
        new_fig=False,
        ax=ax,
        fig=fig,
        view=[30, view_dir],
    )
    print("Fourth and last layer is done!...")

    ax.grid(False)
    ax.set_axis_off()
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])

    return fig, ax


# *_________________________________________________

if __name__ == "__main__":

    # import matplotlib
    # %matplotlib qt

    rho = np.load("../data_analysis/data/rho.npy")

    cut = 5

    style_lib = "../plot/style_lib/"
    # pallette   = style_lib + 'cup_pallette.mplstyle'
    pallette = style_lib + "dark_pallette.mplstyle"
    # pallette = style_lib + "bright_pallette.mplstyle"
    plot_style = style_lib + "plot_style.mplstyle"
    text_style = style_lib + "text.mplstyle"

    plt.style.use([pallette, plot_style, text_style])

    def alpha_plot(c_arr, log_flag=False):
        return poly_alpha(c_arr, log_flag=log_flag, order=1, cut=5)

    # fig, ax = render_voxel_3d(rho, alpha_fn=alpha_plot, log_flag=True)
    # fig, ax = render_voxel_3d(rho, alpha_fn=alpha_plot, log_flag=True)
    fig, ax = full_render(rho, view=[30, -60], cmap=cr.bubblegum)

    plt.show()
