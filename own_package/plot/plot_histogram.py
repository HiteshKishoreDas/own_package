'''
@Author: Hitesh Kishore Das 
@Date: 2022-11-24 14:07:23 
'''

import numpy as np
import cmasher as cr
import sys
import os

import matplotlib as mt
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

# sys.path.insert(0, f'{package_abs_path}utils/')
# from timer import timer 
# import units as un


def plot_histogram_1d  (hist_data, \
                        bins=None, log_bin=False, \
                        new_fig=True, fig=None, ax=None, \
                        kwargs={}, bar_args={} , return_hist = False, with_fig=True):

    line_border_color = mt.rcParams['lines.color']

    if new_fig and with_fig:
        fig, ax = plt.subplots(nrows=1, ncols=1)

    if bins is None:
        bins=10

    if log_bin:
        hist_data_temp = np.log10(hist_data)
    else:
        hist_data_temp = hist_data


    hst = np.histogram(hist_data_temp, bins, **kwargs)

    if return_hist and not(with_fig):
        return hst

    if log_bin:
        bar_edges = 10**hst[1]
    else:
        bar_edges = hst[1]


    bar_height = hst[0]
    bar_posn   = bar_edges[:-1]
    bar_width  = np.diff(bar_edges) #bar_edges[1:] - bar_edges[:-1]

    ax.bar(x=bar_posn, height=bar_height, width=bar_width, \
           edgecolor=line_border_color, align='edge', **bar_args)

    if log_bin:
        ax.set_xscale('log')

    if return_hist:
        return fig, ax, hst
    else:
        return fig, ax
    
def plot_histogram_2d  (hist_data_x, hist_data_y, \
                        bins=None, log_bin=[False, False], hist_log=False,\
                        cmap=cr.bubblegum, color_range=[None, None], \
                        new_fig=True, fig=None, ax=None, norm=1.0,\
                        kwargs={}, cbar_args={} ):

    line_border_color = mt.rcParams['lines.color']

    if new_fig:
        fig, ax = plt.subplots(nrows=1, ncols=1)

    if bins is None:
        bins=10

    if log_bin[0]:
        hist_temp_x = np.log10(hist_data_x)
    else:
        hist_temp_x = hist_data_x

    if log_bin[1]:
        hist_temp_y = np.log10(hist_data_y)
    else:
        hist_temp_y = hist_data_y


    hst, xedges, yedges = np.histogram2d(hist_temp_x, hist_temp_y, bins, **kwargs)

    if log_bin[0]:
        bar_edges_x = 10**xedges
    else:
        bar_edges_x = xedges

    if log_bin[1]:
        bar_edges_y = 10**yedges
    else:
        bar_edges_y = yedges

    hst = hst.T

    if hist_log:
        hst_plot = np.log10(hst)
        if None not in color_range:
            color_range = np.log10(np.array(color_range))
        if None in color_range:
            if not(color_range[0] is None ):
                color_range[0] = np.log10(color_range[0])
            if not(color_range[1] is None ):
                color_range[1] = np.log10(color_range[1])
    else:
        hst_plot = hst


    himg = ax.pcolormesh(bar_edges_x, bar_edges_y, hst_plot/norm, \
                        vmin=color_range[0], vmax=color_range[1],  \
                        cmap=cmap, **kwargs )    

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size=0.2, pad=0.05)

    if hist_log:
        if None in color_range:
            print("plot_histogram.py::plot_histogram_2d(): None in color_range, using extents of histogram for colorbar...")
            cbar = plt.colorbar(mt.cm.ScalarMappable(norm=mt.colors.LogNorm(vmin=1/float(norm), vmax=hst.max()/float(norm)), cmap=cmap), \
                            cax=cax, **cbar_args)
        else:
            cbar = plt.colorbar(mt.cm.ScalarMappable(norm=mt.colors.LogNorm(vmin=10**color_range[0], vmax=10**color_range[1]), cmap=cmap), \
                            cax=cax, **cbar_args)

    else:
        if None in color_range:
            print("plot_histogram.py::plot_histogram_2d(): None in color_range, using extents of histogram for colorbar...")
            cbar = plt.colorbar(mt.cm.ScalarMappable(norm=mt.colors.Normalize(vmin=hst.min()/float(norm), vmax=hst.max()/float(norm)), cmap=cmap), \
                            cax=cax, **cbar_args)
        else:
            cbar = plt.colorbar(mt.cm.ScalarMappable(norm=mt.colors.Normalize(vmin=color_range[0], vmax=color_range[1]), cmap=cmap), \
                            cax=cax, **cbar_args)
    
    if log_bin[0]:
        ax.set_xscale('log')
    if log_bin[1]:
        ax.set_yscale('log')

    return fig, ax

if __name__=='__main__':

    cwd = os.path.dirname(__file__)
    package_abs_path = cwd[:-len(cwd.split('/')[-1])]

    style_lib  = f'{package_abs_path}plot/style_lib/' 
    # pallette   = style_lib + 'dark_pallette.mplstyle'
    pallette   = style_lib + 'bright_pallette.mplstyle'
    plot_style = style_lib + 'plot_style.mplstyle'
    text_style = style_lib + 'text.mplstyle'
    
    plt.style.use([pallette, plot_style, text_style])
    
    A = np.random.random(100000)*5
    B = np.random.random(100000)*5

    bin_arr = np.logspace(0,5, num=25)
    fig, ax = plot_histogram_1d(10**A, bins=bin_arr, bar_args={'alpha':0.3})
    ax.set_xscale('log')
    fig.show()

    fig, ax = plot_histogram_1d(A, bins=25,log_bin=False, bar_args={'alpha':0.3})
    fig.show()

    fig, ax = plot_histogram_2d(10**A, 10**B, bins=100,log_bin=[True,True], hist_log=True,norm=2)
    fig.show()