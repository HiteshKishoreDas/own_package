'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-01 19:07:23 
'''

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


def plot_slice  (img_data, slice_dir=2, x_data=None, y_data=None, \
                 z_data=None, z_slice=None, \
                 ax_log= {'x_log': False, 'y_log':False, 'col_log':False}, \
                 normalise_list = {'x_norm':[None], 'y_norm':[None]}, \
                 cmap=cr.rainforest):

    fig, ax = plt.subplots(nrows=1, ncols=1)

    L = np.shape(img_data)
    dim = len(L) 

    x_dir = (slice_dir+1)%dim
    y_dir = (slice_dir+2)%dim
    z_dir = slice_dir

    if x_data == None:
        x_data = np.linspace(0, L[x_dir], num=L[x_dir]+1)
    if y_data == None:
        y_data = np.linspace(0, L[y_dir], num=L[y_dir]+1)
    if z_data == None:
        z_data = np.linspace(0, L[z_dir], num=L[z_dir]+1)

    if z_slice==None:
        z_slice_i = int(L[z_dir]/2)
    else:
        dz_data   = z_data[1]-z_data[0]
        z_slice_i = int(z_slice/dz_data)

    slice_syntax = ['']*3

    slice_syntax[x_dir] = slice(None)
    slice_syntax[y_dir] = slice(None)
    slice_syntax[z_dir] = z_slice_i

    slice_syntax = tuple(slice_syntax)

    slice_plot = img_data[slice_syntax]

    slc = ax.pcolormesh(x_data, y_data, slice_plot, cmap=cmap)
    cbar = fig.colorbar(slc, ax=ax)

    ax.set_aspect('equal')

    return fig, ax, slc, cbar



if __name__ == "__main__":

    rho = np.load('../data_analysis/data/rho.npy')

    style_lib  = '../plot/style_lib/' 
    # pallette   = style_lib + 'cup_pallette.mplstyle'
    # pallette   = style_lib + 'dark_pallette.mplstyle'
    pallette   = style_lib + 'bright_pallette.mplstyle'
    plot_style = style_lib + 'plot_style.mplstyle'
    text_style = style_lib + 'text.mplstyle'

    plt.style.use([pallette, plot_style, text_style])

    fig, ax, slc, cb = plot_slice(rho, slice_dir=2)
    cb.set_label('Colorbar label') 
    ax.set_title('plot_slice test') 
    ax.set_xlabel('x label') 
    ax.set_ylabel('y label') 

    plt.show()