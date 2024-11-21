"""
@Author: Hitesh Kishore Das 
@Date: 2022-09-01 19:07:23 
"""

import numpy as np
import cmasher as cr
import sys
import os

import matplotlib as mt
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

cwd = os.path.dirname(__file__)
package_abs_path = cwd[: -len(cwd.split("/")[-1])]

sys.path.insert(0, f"{package_abs_path}utils/")
from timer import timer
import units as un

sys.path.insert(0, f"{package_abs_path}data_analysis/")
import array_operations as ao


# TODO: Convert all the usual plt.plot args, that are list, into **kwargs, and then parse it to get the lists...
def plot_multiline(
    x_data_list: list,
    y_data_list: list,
    color_list: list = None,
    ax_log={"x_log": False, "y_log": False, "col_log": False},
    normalise_list={"x_norm": None, "y_norm": None},
    label_list: list = None,
    linestyle="solid",
    linewidth=mt.rcParams["lines.linewidth"],
    mark_flag: bool = False,
    markevery: int = 10,
    smooth_flag: bool = False,
    smooth_window: int = 5,
    cmap=cr.rainforest,
    new_fig: bool = True,
    fig=None,
    ax=None,
    border_width=1,
    **kwargs,
):
    """_summary_

    Args:
        x_data_list (list): list of 1D Numpy arrays with x-values
        y_data_list (list): list of 1D Numpy arrays with y-values

        color_list  (list): list of 1D Numpy arrays with values for color

        ax_log (dict): Dictionary to define scale of x-axis, y-axis and color

        normalise_list (dict): Dictionary to define list of normalisation constants

        label_list (dict): list of labels for the lines

        linestyle (optional): list of strings to define linestyle. Defaults to 'solid'.

        mark_flag (bool, optional): Flag to mark the lines with points. Defaults to False.
        markevery (int, optional): Number of datapoints for which one marker will be places. Defaults to 10.

        smooth_flag (bool, optional): Flag to define if lines will be smoothened or not. Defaults to False.
        smooth_window (int, optional): Smoothening window. Defaults to 5.

        cmap (optional): Colormap for linecolors. Defaults to cr.rainforest.

        new_fig (bool, optional): Flag to define if a new figure needs to be created. Defaults to True.
        fig (optional): figure object to be reused, if new_fig=False. Defaults to None.
        ax (optional): axis object to be reused, if new_fig=False. Defaults to None.

    Returns:
        Dict: Dictionary with the figure and axis object
    """

    line_border_color = mt.rcParams["lines.color"]

    if new_fig:
        fig, ax = plt.subplots(nrows=1, ncols=1)

    if len(x_data_list) != len(y_data_list):
        print(
            "plot_2d_line.py::plot_multiline(): x_data_list and y_data_list are of different lengths..."
        )
        print("plot_2d_line.py::plot_multiline(): Exiting...")
        sys.exit()

    L = len(y_data_list)

    print(f"{color_list = }")

    if color_list == None:
        print("plot_2d_line.py::plot_multiline(): Creating color_list...")
        line_col = [f"C{i}" for i in range(L)]

    elif np.product(np.array([isinstance(col, str) for col in color_list])) != 0:
        line_col = color_list.copy()
        print(f"{line_col = }")

    else:
        if ax_log["col_log"]:
            cb_qnt = np.log10(np.array(color_list))
        else:
            cb_qnt = np.array(color_list)

        cmap_fn = mt.cm.get_cmap(cmap)
        line_col = cmap_fn((cb_qnt - cb_qnt.min()) / (cb_qnt.max() - cb_qnt.min()))

    if isinstance(normalise_list["x_norm"], float):
        print("plot_2d: float found in normalise_list['x_norm'] ...")
        print(f"plot_2d: x-axis normalisation set to {normalise_list['x_norm']} ...")

        normalise_list["x_norm"] = [
            normalise_list["x_norm"] for i in range(len(x_data_list))
        ]

    else:
        # if normalise_list["x_norm"] == None:
        print("plot_2d: None found in normalise_list['x_norm'] ...")
        print("plot_2d: x-axis normalisation set to 1.0 ...")

        normalise_list["x_norm"] = [1.0] * L

        print(f"Yo! {normalise_list['x_norm'] = }")

    if isinstance(normalise_list["y_norm"], float):
        print("plot_2d: float found in normalise_list['y_norm'] ...")
        print(f"plot_2d: y-axis normalisation set to {normalise_list['y_norm']} ...")

        normalise_list["y_norm"] = [
            normalise_list["y_norm"] for i in range(len(y_data_list))
        ]
    else:
        # else normalise_list["y_norm"] == None:
        print("plot_2d: None found in normalise_list['y_norm'] ...")
        print("plot_2d: y-axis normalisation set to 1.0 ...")

        normalise_list["y_norm"] = [1.0] * L

    if label_list == None:
        label_list = [None for i in range(len(y_data_list))]

    linestyle_arr_flag = True
    linewidth_arr_flag = True

    if isinstance(linestyle, str):
        linestyle_arr_flag = False
        linestyle_i = linestyle
    if isinstance(linewidth, float):
        linewidth_arr_flag = False
        linewidth_i = linewidth

    for i in range(L):

        print("----------------------")
        print(f"{i = }")
        print(f"L = {L}")
        print(f"len(x_data_list) = {len(x_data_list)}")
        print(f"len(y_data_list) = {len(y_data_list)}")
        print(f"{len(normalise_list['x_norm']) = }")
        print(f"{len(normalise_list['y_norm']) = }")

        if smooth_flag:
            plot_y = ao.smoothen(y_data_list[i], window=smooth_window)
            plot_x = x_data_list[i][int(smooth_window / 2) : -int(smooth_window / 2)]
        else:
            plot_y = np.copy(y_data_list[i])
            plot_x = np.copy(x_data_list[i])

        if linestyle_arr_flag:
            linestyle_i = linestyle[i]
        if linewidth_arr_flag:
            linewidth_i = linewidth[i]

        line_border_width = linewidth_i + border_width

        if mark_flag:
            ax.plot(
                np.array(plot_x) / np.array(normalise_list["x_norm"][i]),
                np.array(plot_y) / np.array(normalise_list["y_norm"][i]),
                "-o",
                color=line_col[i],
                linestyle=linestyle_i,
                linewidth=linewidth_i,
                label=label_list[i],
                markevery=markevery,
                path_effects=[
                    pe.Stroke(
                        linewidth=line_border_width, foreground=line_border_color
                    ),
                    pe.Normal(),
                ],
                **kwargs,
            )
        else:
            ax.plot(
                np.array(plot_x) / np.array(normalise_list["x_norm"][i]),
                np.array(plot_y) / np.array(normalise_list["y_norm"][i]),
                color=line_col[i],
                linestyle=linestyle_i,
                linewidth=linewidth_i,
                label=label_list[i],
                path_effects=[
                    pe.Stroke(
                        linewidth=line_border_width, foreground=line_border_color
                    ),
                    pe.Normal(),
                ],
                **kwargs,
            )
    if ax_log["x_log"]:
        ax.set_xscale("log")
    if ax_log["y_log"]:
        ax.set_yscale("log")

    plt_dict = {}
    plt_dict["fig"] = fig
    plt_dict["ax"] = ax

    return plt_dict


if __name__ == "__main__":
    from PIL import Image, ImageOps

    style_lib = "../plot/style_lib/"
    # pallette = style_lib + "new_dark_pallette.mplstyle"
    pallette = style_lib + "new_bright_pallette.mplstyle"
    plot_style = style_lib + "plot_style.mplstyle"
    text_style = style_lib + "text.mplstyle"

    plt.style.use([pallette, plot_style, text_style])

    x_data_list = []
    x_data_list.append(np.linspace(0, 1, num=100))
    x_data_list.append(np.linspace(0, 1, num=100))
    x_data_list.append(np.linspace(0, 1, num=100))
    x_data_list.append(np.linspace(0, 1, num=100))
    x_data_list.append(np.linspace(0, 1, num=100))

    y_data_list = []
    y_data_list.append(np.sin(6 * np.linspace(0, 1, num=100)))
    y_data_list.append(np.sin(-2 * np.linspace(0, 1, num=100)))
    y_data_list.append(np.sin(3 * np.linspace(0, 1, num=100)))
    y_data_list.append(np.sin(-4 * np.linspace(0, 1, num=100)))
    y_data_list.append(np.sin(5 * np.linspace(0, 1, num=100)))

    plt_dict = plot_multiline(x_data_list, y_data_list)
    fig = plt_dict["fig"]
    fig.canvas.draw()

    im = Image.frombytes(
        "RGB", fig.canvas.get_width_height(), fig.canvas.tostring_rgb()
    )

    gray_im = ImageOps.grayscale(im)

    gray_im.show()
