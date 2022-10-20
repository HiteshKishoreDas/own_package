'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-01 19:07:23 
'''

# TODO: Add function to plot multicolor line plots

import numpy as np
import cmasher as cr
import sys
import os

import matplotlib as mt
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
import units as un

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import array_operations as ao


def plot_multiline(x_data_list: list,         \
                   y_data_list: list,         \
                   color_list: list = None,   \
                   ax_log = {'x_log': False, 'y_log':False, 'col_log':False}, \
                   normalise_list = {'x_norm':[None], 'y_norm':[None]},       \
                   label_list: list = None,   \
                   linestyle='solid',         \
                   mark_flag: bool = False,   \
                   markevery: int = 10,       \
                   smooth_flag: bool = False, \
                   smooth_window: int = 5,    \
                   cmap = cr.rainforest,      \
                   new_fig: bool = True,      \
                   fig = None, ax = None      ):
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

    line_border_color = mt.rcParams['lines.color']
    line_border_width = mt.rcParams['lines.linewidth'] + 1

    if new_fig:
        fig, ax = plt.subplots(nrows=1, ncols=1)

    L = len(y_data_list)

    if color_list==None:
        line_col = [f'C{i}' for i in range(L)]

    else:
        if ax_log['col_log']:
            cb_qnt = np.log10(np.array(color_list))
        else:
            cb_qnt = np.array(color_list)

        cmap_fn = mt.cm.get_cmap(cmap)
        line_col = cmap_fn((cb_qnt-cb_qnt.min())/(cb_qnt.max()-cb_qnt.min()))



    if None in normalise_list['x_norm']:
        print("plot_2d: None found in normalise_list['x_norm'] ...")
        print("plot_2d: x-axis normalisation set to 1.0 ...")

        normalise_list['x_norm'] = [1.0 for i in range(len(y_data_list))]

    if None in normalise_list['y_norm']:
        print("plot_2d: None found in normalise_list['y_norm'] ...")
        print("plot_2d: y-axis normalisation set to 1.0 ...")

        normalise_list['y_norm'] = [1.0 for i in range(len(y_data_list))]
        

    if label_list == None:
        label_list = [None for i in range(len(y_data_list))]

    if isinstance(linestyle, str):
        style_arr_flag = False
        linestyle_i = linestyle
    else:
        style_arr_flag = True


    for i in range(L):

        if smooth_flag:
            y_data_list[i] = ao.smoothen(y_data_list[i], window=smooth_window)
            x_data_list[i] = x_data_list[i][int(smooth_window/2):-int(smooth_window/2)]

        if style_arr_flag:
            linestyle_i = linestyle[i]

        if mark_flag: 
            ax.plot(np.array(x_data_list[i])/np.array(normalise_list['x_norm'][i]), \
                    np.array(y_data_list[i])/np.array(normalise_list['y_norm'][i]), '-o',\
                    color=line_col[i],  linestyle=linestyle_i, \
                    label = label_list[i], markevery=markevery,  \
                    path_effects=[pe.Stroke(linewidth=line_border_width, \
                                            foreground=line_border_color), pe.Normal()])
        else:
            ax.plot(np.array(x_data_list[i])/np.array(normalise_list['x_norm'][i]), \
                    np.array(y_data_list[i])/np.array(normalise_list['y_norm'][i]), \
                    color=line_col[i],  linestyle=linestyle_i, \
                    label = label_list[i], 
                    path_effects=[pe.Stroke(linewidth=line_border_width, \
                                            foreground=line_border_color), pe.Normal()])
    if ax_log['x_log']:
        ax.set_xscale('log')
    if ax_log['y_log']:
        ax.set_yscale('log')

    plt_dict = {}
    plt_dict['fig'] = fig
    plt_dict['ax']  = ax

    return plt_dict