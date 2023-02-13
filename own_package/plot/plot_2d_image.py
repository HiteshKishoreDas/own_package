"""
@Author: Hitesh Kishore Das 
@Date: 2022-09-01 19:07:23 
"""

import numpy as np
import cmasher as cr
import sys
import os
import gc
import lic

import matplotlib as mt
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from mpl_toolkits.axes_grid1 import make_axes_locatable

cwd = os.path.dirname(__file__)
package_abs_path = cwd[: -len(cwd.split("/")[-1])]

sys.path.insert(0, f"{package_abs_path}utils/")
from timer import timer
import units as un


def plot_slice(
    img_data,
    view_dir: int = 2,
    x_data=None,
    y_data=None,
    z_data=None,
    z_slice: int = None,
    color_range: list = [None, None],
    cbar_flag: bool = True,
    cmap=cr.rainforest,
    new_fig=True,
    ax=None,
    fig=None,
    kwargs={},
    cbar_args={},
):

    """
    Plot 2d slice plots for 3D data

    Args:
        img_data (numpy array): Numpy 3D array for the slice plot
        view_dir (int, optional): Viewing direction, normal to the screen. Defaults to 2.
        x_data (numpy array, optional): 1D numpy array to define vertices in x axis. Defaults to integer array.
        y_data (numpy array, optional): 1D numpy array to define vertices in y axis. Defaults to integer array.
        z_data (numpy array, optional): 1D numpy array to define vertices in z axis. Defaults to integer array.
        z_slice (int, optional): Position in z-axis for slicing. Defaults to midpoint in z-axis.
        color_range (list, optional): List for color range. Defaults to [None, None].
        cmap (optional): Colormap name. Defaults to cr.rainforest.
        new_fig (bool, optional): True if a new figure has to be created. Defaults to True.
        ax (optional): Axis object, used if new_fig is False. Defaults to None.
        fig (optional): Figure object, used if new_fig is False. Defaults to None.
    """

    if new_fig:
        fig, ax = plt.subplots(nrows=1, ncols=1)
    else:
        if None in [fig, ax]:
            raise ValueError(
                "plot_2d_image.py::image_to_plot(): new_flag set to False, but fig or ax not provided..."
            )

    plt.tight_layout()

    L = np.shape(img_data)
    dim = len(L)

    x_dir = (view_dir + 1) % dim
    y_dir = (view_dir + 2) % dim
    z_dir = view_dir

    if x_data == None:
        x_data = np.linspace(0, L[x_dir], num=L[x_dir] + 1)
    if y_data == None:
        y_data = np.linspace(0, L[y_dir], num=L[y_dir] + 1)
    if z_data == None:
        z_data = np.linspace(0, L[z_dir], num=L[z_dir] + 1)

    if z_slice == None:
        z_slice_i = int(L[z_dir] / 2)
    else:
        dz_data = z_data[1] - z_data[0]
        z_slice_i = int(z_slice / dz_data)

    slice_syntax = [""] * 3

    slice_syntax[x_dir] = slice(None)
    slice_syntax[y_dir] = slice(None)
    slice_syntax[z_dir] = z_slice_i

    slice_syntax = tuple(slice_syntax)

    slice_plot = img_data[slice_syntax]

    if view_dir == 1:
        slc = ax.pcolormesh(
            x_data,
            y_data,
            slice_plot,
            vmin=color_range[0],
            vmax=color_range[1],
            cmap=cmap,
            **kwargs,
        )
    else:
        slc = ax.pcolormesh(
            y_data,
            x_data,
            slice_plot,
            vmin=color_range[0],
            vmax=color_range[1],
            cmap=cmap,
            **kwargs,
        )

    ax.set_aspect("equal")

    plt_dict = {}
    plt_dict["fig"] = fig
    plt_dict["ax"] = ax
    plt_dict["slc"] = slc

    if cbar_flag:

        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="5%", pad=0.05)

        cbar = fig.colorbar(slc, cax=cax, **cbar_args)
        plt_dict["cbar"] = cbar

    return plt_dict


def plot_projection(
    img_data,
    view_dir: int = 2,
    x_data=None,
    y_data=None,
    z_data=None,
    weight_data=None,
    color_range: list = [None, None],
    cmap=cr.rainforest,
    cbar_flag: bool = True,
    new_fig=True,
    ax=None,
    fig=None,
    kwargs={},
    cbar_args={},
):

    """
    Plot 2d projection plots for 3D data

    Args:
        img_data (numpy array): Numpy 3D array for the projection plot
        view_dir (int, optional): Viewing direction, normal to the screen. Defaults to 2.
        x_data (numpy array, optional): 1D numpy array to define vertices in x axis. Defaults to integer array.
        y_data (numpy array, optional): 1D numpy array to define vertices in y axis. Defaults to integer array.
        z_data (numpy array, optional): 1D numpy array to define vertices in z axis. Defaults to integer array.
        weight_data (numpy array, optional): 3D numpy array as weight for the averaging. Defaults to unit array.
        color_range (list, optional): List for color range. Defaults to [None, None].
        cmap (optional): Colormap name. Defaults to cr.rainforest.
        new_fig (bool, optional): True if a new figure has to be created. Defaults to True.
        ax (optional): Axis object, used if new_fig is False. Defaults to None.
        fig (optional): Figure object, used if new_fig is False. Defaults to None.
    """

    if new_fig:
        fig, ax = plt.subplots(nrows=1, ncols=1)
    else:
        if None in [fig, ax]:
            raise ValueError(
                "plot_2d_image.py::image_to_plot(): new_flag set to False, but fig or ax not provided..."
            )

    plt.tight_layout()

    L = np.shape(img_data)
    dim = len(L)

    x_dir = (view_dir + 1) % dim
    y_dir = (view_dir + 2) % dim
    z_dir = view_dir

    if x_data == None:
        x_data = np.linspace(0, L[x_dir], num=L[x_dir] + 1)
    if y_data == None:
        y_data = np.linspace(0, L[y_dir], num=L[y_dir] + 1)
    if z_data == None:
        z_data = np.linspace(0, L[z_dir], num=L[z_dir] + 1)

    if weight_data == None:
        weight_data = np.ones_like(img_data)

    proj_plot = np.average(img_data, weights=weight_data, axis=view_dir)

    if view_dir == 1:
        slc = ax.pcolormesh(
            x_data,
            y_data,
            proj_plot,
            vmin=color_range[0],
            vmax=color_range[1],
            cmap=cmap,
            **kwargs,
        )
    else:
        slc = ax.pcolormesh(
            y_data,
            x_data,
            proj_plot,
            vmin=color_range[0],
            vmax=color_range[1],
            cmap=cmap,
            **kwargs,
        )

    ax.set_aspect("equal")

    plt_dict = {}
    plt_dict["fig"] = fig
    plt_dict["ax"] = ax
    plt_dict["slc"] = slc

    if cbar_flag:

        # create an axes on the right side of ax. The width of cax will be 5%
        # of ax and the padding between cax and ax will be fixed at 0.05 inch.
        divider = make_axes_locatable(ax)
        cax = divider.append_axes("right", size="10%", pad=0.05)

        cbar = fig.colorbar(slc, cax=cax, **cbar_args)
        plt_dict["cbar"] = cbar

    return plt_dict


def plot_streamline(
    img_data_x,
    img_data_y,
    view_dir: int = 2,
    mode: str = "slice",
    x_data=None,
    y_data=None,
    z_data=None,
    z_slice: int = None,
    weight_data=None,
    color="tab:orange",
    cmap="plasma",
    new_fig=True,
    ax=None,
    fig=None,
    kwargs={},
):

    """
    Plot steamlines for 3D data

    Args:
        img_data_x (numpy array): Numpy 3D array for the vector component along x
        img_data_y (numpy array): Numpy 3D array for the vector component along y

        view_dir (int, optional): Viewing direction, normal to the screen. Defaults to 2.

        x_data (numpy array, optional): 1D numpy array to define vertices in x axis. Defaults to integer array.
        y_data (numpy array, optional): 1D numpy array to define vertices in y axis. Defaults to integer array.
        z_data (numpy array, optional): 1D numpy array to define vertices in z axis. Defaults to integer array.
        z_slice (int, optional): Position in z-axis for slicing. Defaults to midpoint in z-axis.

        mode (str, optional): Mode of streamline plot. Can be 'slice' or 'average'. Defaults to 'slice'.
        weight_data (numpy array, optional): Weight array, when mode is 'average'.

        color (string or numpy array, optional): String gives a solid color, 2D numpy array will give a colormap. Defaults to [None, None].
        cmap (optional): Colormap name, used if color is a numpy array. Defaults to plasma.

        new_fig (bool, optional): True if a new figure has to be created. Defaults to True.
        ax (optional): Axis object, used if new_fig is False. Defaults to None.
        fig (optional): Figure object, used if new_fig is False. Defaults to None.
    """

    if new_fig:
        fig, ax = plt.subplots(nrows=1, ncols=1)
    else:
        if None in [fig, ax]:
            raise ValueError(
                "plot_2d_image.py::image_to_plot(): new_flag set to False, but fig or ax not provided..."
            )

    plt.tight_layout()

    L = np.shape(img_data_x)
    dim = len(L)

    x_dir = (view_dir + 1) % dim
    y_dir = (view_dir + 2) % dim
    z_dir = view_dir

    if x_data == None:
        x_data = np.linspace(0, L[x_dir], num=L[x_dir])
    if y_data == None:
        y_data = np.linspace(0, L[y_dir], num=L[y_dir])
    if z_data == None:
        z_data = np.linspace(0, L[z_dir], num=L[z_dir])

    if mode == "slice":
        if z_slice == None:
            z_slice_i = int(L[z_dir] / 2)
        else:
            dz_data = z_data[1] - z_data[0]
            z_slice_i = int(z_slice / dz_data)

        slice_syntax = [""] * 3

        slice_syntax[x_dir] = slice(None)
        slice_syntax[y_dir] = slice(None)
        slice_syntax[z_dir] = z_slice_i

        slice_syntax = tuple(slice_syntax)

        stream_data_x = img_data_x[slice_syntax]
        stream_data_y = img_data_y[slice_syntax]

    elif mode == "average":

        if weight_data == None:
            weight_data = np.ones_like(img_data_x)

        stream_data_x = np.average(img_data_x, weights=weight_data, axis=view_dir)
        stream_data_y = np.average(img_data_y, weights=weight_data, axis=view_dir)

    else:
        print("get_array(): Invalid mode, choose betwee 'slice' and 'average' ... ")
        exit()

    slc = ax.streamplot(
        x_data,
        y_data,
        stream_data_x,
        stream_data_y,
        color=color,
        cmap=cmap,
        broken_streamline=False,
        arrowsize=0,
        **kwargs,
    )

    ax.set_aspect("equal")

    plt_dict = {}
    plt_dict["fig"] = fig
    plt_dict["ax"] = ax
    plt_dict["slc"] = slc

    if len(np.shape(color)) == 2:
        cbar = fig.colorbar(slc, ax=ax)
        plt_dict["cbar"] = cbar

    return plt_dict


def plot_line_integral_convolution(
    img_data_x,
    img_data_y,
    view_dir: int = 2,
    mode: str = "slice",
    x_data=None,
    y_data=None,
    z_data=None,
    z_slice: int = None,
    weight_data=None,
    alpha_arr=0.5,
    color="tab:orange",
    cmap="plasma",
    new_fig=True,
    ax=None,
    fig=None,
    kwargs={},
):

    """
    Plot line integral convolution for 3D data

    Args:
        img_data_x (numpy array): Numpy 3D array for the vector component along x
        img_data_y (numpy array): Numpy 3D array for the vector component along y

        view_dir (int, optional): Viewing direction, normal to the screen. Defaults to 2.

        x_data (numpy array, optional): 1D numpy array to define vertices in x axis. Defaults to integer array.
        y_data (numpy array, optional): 1D numpy array to define vertices in y axis. Defaults to integer array.
        z_data (numpy array, optional): 1D numpy array to define vertices in z axis. Defaults to integer array.
        z_slice (int, optional): Position in z-axis for slicing. Defaults to midpoint in z-axis.

        mode (str, optional): Mode of streamline plot. Can be 'slice' or 'average'. Defaults to 'slice'.
        weight_data (numpy array, optional): Weight array, when mode is 'average'.

        color (string or numpy array, optional): String gives a solid color, 2D numpy array will give a colormap. Defaults to [None, None].
        cmap (optional): Colormap name, used if color is a numpy array. Defaults to plasma.

        new_fig (bool, optional): True if a new figure has to be created. Defaults to True.
        ax (optional): Axis object, used if new_fig is False. Defaults to None.
        fig (optional): Figure object, used if new_fig is False. Defaults to None.
    """

    if new_fig:
        fig, ax = plt.subplots(nrows=1, ncols=1)

    plt.tight_layout()

    L = np.shape(img_data_x)
    dim = len(L)

    x_dir = (view_dir + 1) % dim
    y_dir = (view_dir + 2) % dim
    z_dir = view_dir

    if x_data == None:
        x_data = np.linspace(0, L[x_dir], num=L[x_dir])
    if y_data == None:
        y_data = np.linspace(0, L[y_dir], num=L[y_dir])
    if z_data == None:
        z_data = np.linspace(0, L[z_dir], num=L[z_dir])

    if mode == "slice":
        if z_slice == None:
            z_slice_i = int(L[z_dir] / 2)
        else:
            dz_data = z_data[1] - z_data[0]
            z_slice_i = int(z_slice / dz_data)

        slice_syntax = [""] * 3

        slice_syntax[x_dir] = slice(None)
        slice_syntax[y_dir] = slice(None)
        slice_syntax[z_dir] = z_slice_i

        slice_syntax = tuple(slice_syntax)

        stream_data_x = img_data_x[slice_syntax]
        stream_data_y = img_data_y[slice_syntax]

        if not isinstance(alpha_arr, float):
            alpha_arr = alpha_arr[slice_syntax]

    elif mode == "average":

        if weight_data == None:
            weight_data = np.ones_like(img_data_x)

        stream_data_x = np.average(img_data_x, weights=weight_data, axis=view_dir)
        stream_data_y = np.average(img_data_y, weights=weight_data, axis=view_dir)
        if not isinstance(alpha_arr, float):
            alpha_arr = np.average(alpha_arr, weights=weight_data, axis=view_dir)

    else:
        print("get_array(): Invalid mode, choose between 'slice' and 'average' ... ")
        exit()

    lic_result = lic.lic(stream_data_y, stream_data_x, length=50)

    stream_mag = np.sqrt(stream_data_x**2 + stream_data_x**2)

    slc = ax.pcolormesh(
        x_data, y_data, lic_result, cmap="gray", alpha=alpha_arr, **kwargs
    )

    # slc = plt.imshow(lic_result, origin='lower', cmap='gray')

    ax.set_aspect("equal")

    plt_dict = {}
    plt_dict["fig"] = fig
    plt_dict["ax"] = ax
    plt_dict["slc"] = slc

    if len(np.shape(color)) == 2:
        cbar = fig.colorbar(slc, ax=ax)
        plt_dict["cbar"] = cbar

    return plt_dict


def parallel_plot_fn(
    n_snap: int,
    plot_fn,
    sim_loc: str,
    snap_name_fn,
    data_read_fn,
    arg_dict={},
    field_list: list = ["rho"],  # ['all'], \
    save_dir: str = "save_dir",
    MHD_flag: bool = False,
    cmap="plasma",
    theme="bright",
):
    """
    Function to iterate when parallelising plot routine

    Args:
        plot_fn (func): Function to do the plotting, supported functions: plot_slice, plot_projection
        n_snap (int) : Snapshot number
        sim_loc (str): Path to directory with simlulation data
        snap_name_fn (func): Function that takes an int and returns name of file with data
        arg_dict (dict, optional): Dictionary with additional arguments. Defaults to {}
        field_list (list, optional): List fields to plot. Defaults to ['all'].
        save_dir (str, optional): Directory name to save plots in. Defaults to 'save_dir'
        MHD_flag (bool, optional): Magnetic field enabled or not. Defaults to False
        cmap (str, optional): Colormap name. Defaults to 'plasma'.
    """

    style_lib = f"{package_abs_path}/plot/style_lib/"

    if theme == "dark":
        pallette = style_lib + "dark_pallette.mplstyle"
    else:
        pallette = style_lib + "bright_pallette.mplstyle"
    plot_style = style_lib + "plot_style.mplstyle"
    text_style = style_lib + "text.mplstyle"

    plt.style.use([pallette, plot_style, text_style])

    line_border_color = mt.rcParams["lines.color"]
    fig_face_color = mt.rcParams["figure.facecolor"]

    print(f"{n_snap = }")

    print(f"Analysing files in {sim_loc}...")

    file_loc = sim_loc + snap_name_fn(n_snap)

    try:
        out_dict = data_read_fn(file_loc, fields=field_list, MHD_flag=MHD_flag)
    except:
        print(f"[plot_2d_image.py] File couln't be opened! ... \n{file_loc}...")
        return

    # * Nested dictionary for plotting the different quantities

    quant_dict = {}

    print(f"{field_list}")

    if ("rho" in field_list) or ("all" in field_list):
        quant_dict["rho"] = {}
        quant_dict["rho"]["title"] = "Density"
        quant_dict["rho"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}/rho/rho_{str(n_snap).zfill(5)}.png"

        quant_dict["rho"]["arg_dict"] = {}
        quant_dict["rho"]["arg_dict"]["color_range"] = [1.0, 5.0]
        quant_dict["rho"]["arg_dict"]["img_data"] = out_dict["rho"]
        quant_dict["rho"]["arg_dict"]["cmap"] = cmap
        quant_dict["rho"]["arg_dict"]["view_dir"] = 1

        print("rho added to dictionary....")

    if ("log_rho" in field_list) or ("all" in field_list):
        quant_dict["log_rho"] = {}
        quant_dict["log_rho"]["title"] = "Log_10 Density"
        quant_dict["log_rho"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}/log_rho/log_rho_{str(n_snap).zfill(5)}.png"
        quant_dict["log_rho"]["arg_dict"] = {}
        quant_dict["log_rho"]["arg_dict"]["img_data"] = np.log10(out_dict["rho"])
        quant_dict["log_rho"]["arg_dict"]["color_range"] = [-5, -1]
        quant_dict["log_rho"]["arg_dict"]["cmap"] = cmap
        quant_dict["log_rho"]["arg_dict"]["view_dir"] = 1

        print("log_rho added to dictionary....")

    if ("prs" in field_list) or ("all" in field_list):
        quant_dict["prs"] = {}
        quant_dict["prs"]["title"] = "Pressure"
        quant_dict["prs"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}/prs/prs_{str(n_snap).zfill(5)}.png"

        quant_dict["prs"]["arg_dict"] = {}
        quant_dict["prs"]["arg_dict"]["img_data"] = np.log10(out_dict["rho"])
        quant_dict["prs"]["arg_dict"]["cmap"] = cmap
        quant_dict["prs"]["arg_dict"]["view_dir"] = 1

        print("prs added to dictionary....")

    if ("logT" in field_list) or ("all" in field_list):
        quant_dict["logT"] = {}
        quant_dict["logT"]["title"] = "log_10 T"
        quant_dict["logT"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}/logT/logT_{str(n_snap).zfill(5)}.png"

        quant_dict["logT"]["arg_dict"] = {}
        quant_dict["logT"]["arg_dict"]["img_data"] = out_dict["logT"]
        quant_dict["logT"]["arg_dict"]["cmap"] = cmap
        quant_dict["logT"]["arg_dict"]["view_dir"] = 1

        print("logT added to dictionary....")

    if ("vx" in field_list) or ("all" in field_list):
        quant_dict["vx"] = {}
        quant_dict["vx"]["title"] = "v_x"
        quant_dict["vx"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}/vx/vx_{str(n_snap).zfill(5)}.png"

        quant_dict["vx"]["arg_dict"] = {}
        quant_dict["vx"]["arg_dict"]["img_data"] = out_dict["vel"][0]
        quant_dict["vx"]["arg_dict"]["cmap"] = cmap
        quant_dict["vx"]["arg_dict"]["view_dir"] = 1

        print("vx added to dictionary....")

    if ("vy" in field_list) or ("all" in field_list):
        quant_dict["vy"] = {}
        quant_dict["vy"]["title"] = "v_y"
        quant_dict["vy"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}/vy/vy_{str(n_snap).zfill(5)}.png"

        quant_dict["vy"]["arg_dict"] = {}
        quant_dict["vy"]["arg_dict"]["img_data"] = out_dict["vel"][1]
        quant_dict["vy"]["arg_dict"]["cmap"] = cmap
        quant_dict["vy"]["arg_dict"]["view_dir"] = 1

        print("vy added to dictionary....")

    if ("vz" in field_list) or ("all" in field_list):
        quant_dict["vz"] = {}
        quant_dict["vz"]["title"] = "v_z"
        quant_dict["vz"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}/vz/vz_{str(n_snap).zfill(5)}.png"

        quant_dict["vz"]["arg_dict"] = {}
        quant_dict["vz"]["arg_dict"]["img_data"] = out_dict["vel"][2]
        quant_dict["vz"]["arg_dict"]["cmap"] = cmap
        quant_dict["vz"]["arg_dict"]["view_dir"] = 1

        print("vz added to dictionary....")

    if MHD_flag and (("Bx" in field_list) or ("all" in field_list)):
        quant_dict["Bx"] = {}
        quant_dict["Bx"]["title"] = "B_x"
        quant_dict["Bx"][
            "save_loc"
        ] = f"{sim_loc}Plots/slices/{save_dir}/Bx_{str(n_snap).zfill(5)}.png"

        quant_dict["Bx"]["arg_dict"] = {}
        quant_dict["Bx"]["arg_dict"]["img_data"] = out_dict["B"][0]
        quant_dict["Bx"]["arg_dict"]["cmap"] = cmap
        quant_dict["Bx"]["arg_dict"]["view_dir"] = 1

        print("Bx added to dictionary....")

    if MHD_flag and (("By" in field_list) or ("all" in field_list)):
        quant_dict["By"] = {}
        quant_dict["By"]["title"] = "B_y"
        quant_dict["By"][
            "save_loc"
        ] = f"{sim_loc}Plots/slices/{save_dir}/By_{str(n_snap).zfill(5)}.png"

        quant_dict["By"]["arg_dict"] = {}
        quant_dict["By"]["arg_dict"]["img_data"] = out_dict["B"][1]
        quant_dict["By"]["arg_dict"]["cmap"] = cmap
        quant_dict["By"]["arg_dict"]["view_dir"] = 1

        print("By added to dictionary....")

    if MHD_flag and (("Bz" in field_list) or ("all" in field_list)):
        quant_dict["Bz"] = {}
        quant_dict["Bz"]["title"] = "B_z"
        quant_dict["Bz"][
            "save_loc"
        ] = f"{sim_loc}Plots/slices/{save_dir}/Bz_{str(n_snap).zfill(5)}.png"

        quant_dict["Bz"]["arg_dict"] = {}
        quant_dict["Bz"]["arg_dict"]["img_data"] = out_dict["B"][2]
        quant_dict["Bz"]["arg_dict"]["cmap"] = cmap
        quant_dict["Bz"]["arg_dict"]["view_dir"] = 1

        print("Bz added to dictionary....")

    if not (os.path.exists(f"{sim_loc}Plots")):
        os.system(f"mkdir {sim_loc}Plots")
    if not (os.path.exists(f"{sim_loc}Plots/{save_dir}")):
        os.system(f"mkdir {sim_loc}Plots/{save_dir}")

    # * To loop over the different quantities and plot them
    for key in quant_dict:

        if not (os.path.exists(f"{sim_loc}Plots/{save_dir}/{key}")):
            try:
                os.system(f"mkdir {sim_loc}Plots/{save_dir}/{key}")
            except:
                print("Couldn't create the directory for {out_loc} ...")
                # return

        plt_dict = plot_fn(**quant_dict[key]["arg_dict"], **arg_dict)
        plt_dict["ax"].set_title(quant_dict[key]["title"])
        plt.savefig(quant_dict[key]["save_loc"])

        print(f"{key} saved for {n_snap = } ...")

        plt.close()
        plt.clf()
        plt.cla()
        del plt_dict

        gc.collect()

    # del(quant_dict)
    # gc.collect()


if __name__ == "__main__":

    rho = np.load("../data_analysis/data/rho.npy")
    v1 = np.load("../data_analysis/data/v1.npy")
    v2 = np.load("../data_analysis/data/v2.npy")

    style_lib = "../plot/style_lib/"
    # pallette   = style_lib + 'cup_pallette.mplstyle'
    # pallette   = style_lib + 'dark_pallette.mplstyle'
    pallette = style_lib + "bright_pallette.mplstyle"
    plot_style = style_lib + "plot_style.mplstyle"
    text_style = style_lib + "text.mplstyle"

    plt.style.use([pallette, plot_style, text_style])

    plot_dict = plot_slice(rho[:10, :20, :30], view_dir=2)
    plot_dict["cbar"].set_label("Colorbar label")
    plot_dict["ax"].set_title("plot_slice test")
    plot_dict["ax"].set_xlabel("x label")
    plot_dict["ax"].set_ylabel("y label")

    plt.show()

    plot_dict = plot_projection(rho[:10, :20, :30], view_dir=1)
    plot_dict["cbar"].set_label("Colorbar label")
    plot_dict["ax"].set_title("plot_projection test")
    plot_dict["ax"].set_xlabel("x label")
    plot_dict["ax"].set_ylabel("y label")

    # plt.show()

    plot_dict = plot_streamline(
        v1[:10, :20, :30],
        v2[:10, :20, :30],
        mode="average",
        view_dir=1,
        new_fig=False,
        ax=plot_dict["ax"],
        fig=plot_dict["fig"],
    )
    # plot_dict['cbar'].set_label('Colorbar label')
    plot_dict["ax"].set_title("plot_projection test")
    plot_dict["ax"].set_xlabel("x label")
    plot_dict["ax"].set_ylabel("y label")

    plt.show()

    plot_dict = plot_streamline(v1, v2, mode="average", view_dir=1)
    plot_dict = plot_line_integral_convolution(
        v1,
        v2,
        mode="average",
        view_dir=1,
        new_fig=False,
        ax=plot_dict["ax"],
        fig=plot_dict["fig"],
    )
    # plot_dict['cbar'].set_label('Colorbar label')
    plot_dict["ax"].set_title("line integral convolution test")
    plot_dict["ax"].set_xlabel("x label")
    plot_dict["ax"].set_ylabel("y label")

    plt.show()
