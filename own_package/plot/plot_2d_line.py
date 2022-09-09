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


def plot_multiline(x_data_list, y_data_list, \
                   color_list=None, \
                   ax_log= {'x_log': False, 'y_log':False, 'col_log':False}, \
                   normalise_list = {'x_norm':[None], 'y_norm':[None]}, \
                   label_list = None, linestyle='solid', \
                   cmap=cr.rainforest):

    line_border_color = mt.rcParams['lines.color']
    line_border_width = mt.rcParams['lines.linewidth'] + 1

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



    for i in range(L):

        # ax.plot(x_data_list[i]/normalise_list['x_norm'][i], \
        #         y_data_list[i]/normalise_list['y_norm'][i], \
        #         linestyle = linestyle, \
        #         color=line_border_color, linewidth = line_border_width)

        ax.plot(x_data_list[i]/normalise_list['x_norm'][i], \
                y_data_list[i]/normalise_list['y_norm'][i], \
                color=line_col[i],  linestyle=linestyle, \
                label = label_list[i], 
                path_effects=[pe.Stroke(linewidth=line_border_width, \
                                        foreground=line_border_color), pe.Normal()])

    if ax_log['x_log']:
        ax.set_xscale('log')
    if ax_log['y_log']:
        ax.set_yscale('log')

    return fig, ax