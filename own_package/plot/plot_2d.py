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

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
import units as un


def plot_multiline(y_data_list, x_data_list, \
                   color_list=None, \
                   ax_log= {'x_log': False, 'y_log':False, 'col_log':False}, \
                   cmap=cr.rainforest):

    fig, ax = plt.subplots(nrow=1, ncols=1)

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

    for i in range(L):
        ax.plot(y_data_list[i], x_data_list[i], color=line_col[i])


    if ax_log['x_log']:
        ax.xscale('log')
    if ax_log['y_log']:
        ax.yscale('log')

    return fig, ax