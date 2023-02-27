"""
Created Date: Thursday, January 1st 1970, 1:00:00 am
Author: Hitesh Kishore Das
"""

import numpy as np
import cmasher as cr
import sys
import os
import gc

from multiprocessing import Pool

import matplotlib as mt
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

cwd = os.path.dirname(__file__)
package_abs_path = cwd[: -len(cwd.split("/")[-1])]


def parallelise(fn, iter_list=None, processes=2):
    """
    Function to distribute a repeated function call over multiple processors

    Args:
        fn (function): Function to be run parallely
        iter_list (list, optional): List with elements to iterate over. Defaults to None.
        processes (int, optional): Number of cores to send the jobs. Defaults to 2.
    """

    if iter_list == None:
        iter_list = [i for i in range(processes)]

    with Pool(processes) as pool:
        processed = pool.map(fn, iter_list)

    return processed


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
        ] = f"{sim_loc}Plots/{save_dir}_{plot_fn.__name__}/rho/rho_{str(n_snap).zfill(5)}.png"

        quant_dict["rho"]["arg_dict"] = {}
        # quant_dict["rho"]["arg_dict"]["color_range"] = [0.1, 100]
        quant_dict["rho"]["arg_dict"]["inp_arr"] = out_dict["rho"]
        quant_dict["rho"]["arg_dict"]["cmap"] = cmap

        print("rho added to dictionary....")

    if ("log_rho" in field_list) or ("all" in field_list):
        quant_dict["log_rho"] = {}
        quant_dict["log_rho"]["title"] = "Log_10 Density"
        quant_dict["log_rho"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}_{plot_fn.__name__}/log_rho/log_rho_{str(n_snap).zfill(5)}.png"
        quant_dict["log_rho"]["arg_dict"] = {}
        quant_dict["log_rho"]["arg_dict"]["inp_arr"] = np.log10(out_dict["rho"])
        # quant_dict["log_rho"]["arg_dict"]["color_range"] = [-5, -1]
        quant_dict["log_rho"]["arg_dict"]["cmap"] = cmap

        print("log_rho added to dictionary....")

    if ("prs" in field_list) or ("all" in field_list):
        quant_dict["prs"] = {}
        quant_dict["prs"]["title"] = "Pressure"
        quant_dict["prs"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}_{plot_fn.__name__}/prs/prs_{str(n_snap).zfill(5)}.png"

        quant_dict["prs"]["arg_dict"] = {}
        quant_dict["prs"]["arg_dict"]["inp_arr"] = np.log10(out_dict["rho"])
        quant_dict["prs"]["arg_dict"]["cmap"] = cmap

        print("prs added to dictionary....")

    if ("logT" in field_list) or ("all" in field_list):
        quant_dict["logT"] = {}
        quant_dict["logT"]["title"] = "log_10 T"
        quant_dict["logT"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}_{plot_fn.__name__}/logT/logT_{str(n_snap).zfill(5)}.png"

        quant_dict["logT"]["arg_dict"] = {}
        quant_dict["logT"]["arg_dict"]["inp_arr"] = out_dict["logT"]
        quant_dict["logT"]["arg_dict"]["cmap"] = cmap

        print("logT added to dictionary....")

    if ("vx" in field_list) or ("all" in field_list):
        quant_dict["vx"] = {}
        quant_dict["vx"]["title"] = "v_x"
        quant_dict["vx"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}_{plot_fn.__name__}/vx/vx_{str(n_snap).zfill(5)}.png"

        quant_dict["vx"]["arg_dict"] = {}
        quant_dict["vx"]["arg_dict"]["inp_arr"] = out_dict["vel"][0]
        quant_dict["vx"]["arg_dict"]["cmap"] = cmap

        print("vx added to dictionary....")

    if ("vy" in field_list) or ("all" in field_list):
        quant_dict["vy"] = {}
        quant_dict["vy"]["title"] = "v_y"
        quant_dict["vy"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}_{plot_fn.__name__}/vy/vy_{str(n_snap).zfill(5)}.png"

        quant_dict["vy"]["arg_dict"] = {}
        quant_dict["vy"]["arg_dict"]["inp_arr"] = out_dict["vel"][1]
        quant_dict["vy"]["arg_dict"]["cmap"] = cmap

        print("vy added to dictionary....")

    if ("vz" in field_list) or ("all" in field_list):
        quant_dict["vz"] = {}
        quant_dict["vz"]["title"] = "v_z"
        quant_dict["vz"][
            "save_loc"
        ] = f"{sim_loc}Plots/{save_dir}_{plot_fn.__name__}/vz/vz_{str(n_snap).zfill(5)}.png"

        quant_dict["vz"]["arg_dict"] = {}
        quant_dict["vz"]["arg_dict"]["inp_arr"] = out_dict["vel"][2]
        quant_dict["vz"]["arg_dict"]["cmap"] = cmap

        print("vz added to dictionary....")

    if MHD_flag and (("Bx" in field_list) or ("all" in field_list)):
        quant_dict["Bx"] = {}
        quant_dict["Bx"]["title"] = "B_x"
        quant_dict["Bx"][
            "save_loc"
        ] = f"{sim_loc}Plots/slices/{save_dir}_{plot_fn.__name__}/Bx_{str(n_snap).zfill(5)}.png"

        quant_dict["Bx"]["arg_dict"] = {}
        quant_dict["Bx"]["arg_dict"]["inp_arr"] = out_dict["B"][0]
        quant_dict["Bx"]["arg_dict"]["cmap"] = cmap

        print("Bx added to dictionary....")

    if MHD_flag and (("By" in field_list) or ("all" in field_list)):
        quant_dict["By"] = {}
        quant_dict["By"]["title"] = "B_y"
        quant_dict["By"][
            "save_loc"
        ] = f"{sim_loc}Plots/slices/{save_dir}_{plot_fn.__name__}/By_{str(n_snap).zfill(5)}.png"

        quant_dict["By"]["arg_dict"] = {}
        quant_dict["By"]["arg_dict"]["inp_arr"] = out_dict["B"][1]
        quant_dict["By"]["arg_dict"]["cmap"] = cmap

        print("By added to dictionary....")

    if MHD_flag and (("Bz" in field_list) or ("all" in field_list)):
        quant_dict["Bz"] = {}
        quant_dict["Bz"]["title"] = "B_z"
        quant_dict["Bz"][
            "save_loc"
        ] = f"{sim_loc}Plots/slices/{save_dir}_{plot_fn.__name__}/Bz_{str(n_snap).zfill(5)}.png"

        quant_dict["Bz"]["arg_dict"] = {}
        quant_dict["Bz"]["arg_dict"]["inp_arr"] = out_dict["B"][2]
        quant_dict["Bz"]["arg_dict"]["cmap"] = cmap

        print("Bz added to dictionary....")

    if not (os.path.exists(f"{sim_loc}Plots")):
        os.system(f"mkdir {sim_loc}Plots")
    if not (os.path.exists(f"{sim_loc}Plots/{save_dir}_{plot_fn.__name__}")):
        os.system(f"mkdir {sim_loc}Plots/{save_dir}_{plot_fn.__name__}")

    # * To loop over the different quantities and plot them
    for key in quant_dict:

        if not (os.path.exists(f"{sim_loc}Plots/{save_dir}_{plot_fn.__name__}/{key}")):
            try:
                os.system(f"mkdir {sim_loc}Plots/{save_dir}_{plot_fn.__name__}/{key}")
            except:
                print("Couldn't create the directory for {out_loc} ...")

        plt_dict = plot_fn(
            **quant_dict[key]["arg_dict"],
            view_dir=n_snap - 501,
            **arg_dict,
        )
        plt_dict["ax"].set_title(quant_dict[key]["title"])
        plt.savefig(quant_dict[key]["save_loc"])

        print(f"{key} saved for {n_snap = } ...")

        plt.close()
        plt.clf()
        plt.cla()
        del plt_dict

        gc.collect()
