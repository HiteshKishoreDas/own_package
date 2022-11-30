'''
Created Date: 2022-11-04 14:49:55 
Author: Hitesh Kishore Das
'''

import numpy as np
import cmasher as cr
import sys
import os

import matplotlib as mt
import matplotlib.pyplot as plt

def add_legend(plot_args_lst, ax=None, legend_type='line', legend_loc = 'lower left', default_plot_args = {'color' : 'black'},
               **kwargs):
    """Adds another legend to plot. (Stolen from Max! :D )

    Keyword Arguments:
    plot_args_lst      -- List of plotting arguments to show.
    legend_type        -- Type of legend, 'line' or 'point' (default 'line')
    legend_loc         -- Location of new legend (default 'best')
    default_plot_args  -- Arguments will be used for every item in new legend.
    kwargs             -- Will be passed to `plt.legend` of new legend.

    Example 1:
           > maxpy.plot.add_legend([{'ls' : '-', 'label' : '8'}, {'ls' : '--', 'label' : '16'}],
           >                   default_plot_args = {'c' : 'k'},
           >                   title = r'$l_{\rm cell} / r_{\rm cl}$')
    Will add a legend with two different lines (both black).
    Example 2:
            add_legend([{'ls' : '-', 'label' : 'MHD'}, {'ls' : '--', 'label' : 'HD'}],
                             default_plot_args = {'c' : 'k'})
    Will add two different line with 'HD' and 'MHD' as labels.
    """
    if ax is None:
        ax = plt.gca()

    leg = ax.get_legend()

    linelst = []
    for cargs in plot_args_lst:
        for k, v in default_plot_args.items():
            if k not in cargs:
                cargs[k] = v
        if legend_type == 'point': 
            l = ax.scatter(np.nan, np.nan, **cargs)
        else:
            l, = ax.plot(np.nan, **cargs)

        linelst.append(l)

    o = kwargs.copy()
    if 'loc' not in o:
        o['loc'] = legend_loc
    if legend_loc == 'above':
        o['loc'] = 'lower left'
        o['bbox_to_anchor'] = (0.5, 1.01)

    ax.legend(handles = linelst, **o)
    if leg is not None:
        ax.add_artist(leg) # Add old legend

