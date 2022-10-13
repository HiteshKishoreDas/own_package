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


def plot_slice  (img_data, \
                 view_dir: int = 2, \
                 x_data = None, y_data=None, z_data=None, \
                 z_slice: int = None,\
                 color_range: list = [None, None],\
                 cmap = cr.rainforest):

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
    """

    fig, ax = plt.subplots(nrows=1, ncols=1)
    plt.tight_layout()

    L = np.shape(img_data)
    dim = len(L) 

    x_dir = (view_dir+1)%dim
    y_dir = (view_dir+2)%dim
    z_dir = view_dir

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

    if view_dir==1:
        slc = ax.pcolormesh(x_data, y_data, slice_plot, \
                        vmin=color_range[0], vmax=color_range[1],  \
                        cmap=cmap  )
    else:
        slc = ax.pcolormesh(y_data, x_data, slice_plot, \
                        vmin=color_range[0], vmax=color_range[1],  \
                        cmap=cmap  )

    cbar = fig.colorbar(slc, ax=ax)

    ax.set_aspect('equal')

    plt_dict = {}
    plt_dict['fig']  = fig
    plt_dict['ax']   = ax
    plt_dict['slc']  = slc
    plt_dict['cbar'] = cbar

    return plt_dict

def plot_projection (img_data, \
                     view_dir:int = 2, \
                     x_data = None, y_data = None, z_data = None, \
                     weight_data = None,\
                     color_range: list = [None, None],\
                     cmap = cr.rainforest):

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
    """

    fig, ax = plt.subplots(nrows=1, ncols=1)
    plt.tight_layout()

    L = np.shape(img_data)
    dim = len(L) 

    x_dir = (view_dir+1)%dim
    y_dir = (view_dir+2)%dim
    z_dir = view_dir

    if x_data == None:
        x_data = np.linspace(0, L[x_dir], num=L[x_dir]+1)
    if y_data == None:
        y_data = np.linspace(0, L[y_dir], num=L[y_dir]+1)
    if z_data == None:
        z_data = np.linspace(0, L[z_dir], num=L[z_dir]+1)

    if weight_data == None:
        weight_data = np.ones_like(img_data)

    proj_plot = np.average(img_data, weights=weight_data, axis=view_dir)

    if view_dir==1:
        slc = ax.pcolormesh(x_data, y_data, proj_plot, \
                        vmin=color_range[0], vmax=color_range[1],  \
                        cmap=cmap  )
    else:
        slc = ax.pcolormesh(y_data, x_data, proj_plot, \
                        vmin=color_range[0], vmax=color_range[1],  \
                        cmap=cmap  )

    cbar = fig.colorbar(slc, ax=ax)

    ax.set_aspect('equal')

    plt_dict = {}
    plt_dict['fig']  = fig
    plt_dict['ax']   = ax
    plt_dict['slc']  = slc
    plt_dict['cbar'] = cbar

    return plt_dict

def parallel_plot_fn (n_snap: int,  \
                      plot_fn,  \
                      sim_loc: str, \
                      snap_name_fn, \
                      data_read_fn, \
                      arg_dict={} , \
                      field_list: list = ['all'], \
                      save_dir: str = 'save_dir', \
                      MHD_flag: bool = False,       \
                      n_start:int = 0,  \
                      cmap = 'plasma'  ):
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
        n_start (int, optional): Starting snapshot number. Defaults to 0.
        cmap (str, optional): Colormap name. Defaults to 'plasma'.
    """


    print(f"{n_snap = }")

    print(f"Analysing files in {sim_loc}...")

    file_loc = sim_loc + snap_name_fn(n_snap)

    out_dict = data_read_fn(file_loc, fields=field_list, MHD_flag=MHD_flag)
    T = (out_dict['prs']/out_dict['rho']) * un.KELVIN * un.mu


    #* Nested dictionary for plotting the different quantities

    quant_dict = {}

    if 'rho' or 'all' in field_list:
        quant_dict['rho'] = {}
        quant_dict['rho']['title'] = 'Log_10 Density'
        quant_dict['rho']['save_loc'] = f"{sim_loc}Plots/slices/rho/rho_{str(n_snap).zfill(5)}.png"

        quant_dict['rho']['arg_dict'] = {}
        quant_dict['rho']['arg_dict']['img_data'] = np.log10(out_dict['rho'])
        quant_dict['rho']['arg_dict']['color_range'] = [-5,-1]
        quant_dict['rho']['arg_dict']['cmap'] = cmap
        quant_dict['rho']['arg_dict']['view_dir'] = 1 

    if 'prs' or 'all' in field_list:
        quant_dict['prs'] = {}
        quant_dict['prs']['title'] = 'Pressure'
        quant_dict['prs']['save_loc'] = f"{sim_loc}Plots/slices/prs/prs_{str(n_snap).zfill(5)}.png"

        quant_dict['prs']['arg_dict'] = {}
        quant_dict['prs']['arg_dict']['img_data'] = np.log10(out_dict['rho'])
        quant_dict['prs']['arg_dict']['cmap'] = cmap
        quant_dict['prs']['arg_dict']['view_dir'] = 1 

    if 'logT' or 'all' in field_list:
        quant_dict['logT'] = {}
        quant_dict['logT']['title'] = 'log_10 T'
        quant_dict['logT']['save_loc'] = f"{sim_loc}Plots/slices/logT/logT_{str(n_snap).zfill(5)}.png"

        quant_dict['logT']['arg_dict'] = {}
        quant_dict['logT']['arg_dict']['img_data'] = out_dict['logT']
        quant_dict['logT']['arg_dict']['cmap'] = cmap
        quant_dict['logT']['arg_dict']['view_dir'] = 1 

    if 'vx' or 'all' in field_list:
        quant_dict['vx'] = {}
        quant_dict['vx']['title'] = 'v_x'
        quant_dict['vx']['save_loc'] = f"{sim_loc}Plots/slices/vx/vx_{str(n_snap).zfill(5)}.png"

        quant_dict['vx']['arg_dict'] = {}
        quant_dict['vx']['arg_dict']['img_data'] = out_dict['vel'][0]
        quant_dict['vx']['arg_dict']['cmap'] = cmap
        quant_dict['vx']['arg_dict']['view_dir'] = 1 

    if 'vy' or 'all' in field_list:
        quant_dict['vy'] = {}
        quant_dict['vy']['title'] = 'v_y'
        quant_dict['vy']['save_loc'] = f"{sim_loc}Plots/slices/vy/vy_{str(n_snap).zfill(5)}.png"

        quant_dict['vy']['arg_dict'] = {}
        quant_dict['vy']['arg_dict']['img_data'] = out_dict['vel'][1]
        quant_dict['vy']['arg_dict']['cmap'] = cmap
        quant_dict['vy']['arg_dict']['view_dir'] = 1 

    if 'vz' or 'all' in field_list:
        quant_dict['vz'] = {}
        quant_dict['vz']['title'] = 'v_z'
        quant_dict['vz']['save_loc'] = f"{sim_loc}Plots/slices/vz/vz_{str(n_snap).zfill(5)}.png"

        quant_dict['vz']['arg_dict'] = {}
        quant_dict['vz']['arg_dict']['img_data'] = out_dict['vel'][2]
        quant_dict['vz']['arg_dict']['cmap'] = cmap
        quant_dict['vz']['arg_dict']['view_dir'] = 1 

    if MHD_flag and ('Bx' or 'all' in field_list):
        quant_dict['Bx'] = {}
        quant_dict['Bx']['title'] = 'B_x'
        quant_dict['Bx']['save_loc'] = f"{sim_loc}Plots/slices/Bx/Bx_{str(n_snap).zfill(5)}.png"

        quant_dict['Bx']['arg_dict'] = {}
        quant_dict['Bx']['arg_dict']['img_data'] = out_dict['B'][0]
        quant_dict['Bx']['arg_dict']['cmap'] = cmap
        quant_dict['Bx']['arg_dict']['view_dir'] = 1 

    if MHD_flag and ('By' or 'all' in field_list):
        quant_dict['By'] = {}
        quant_dict['By']['title'] = 'B_y'
        quant_dict['By']['save_loc'] = f"{sim_loc}Plots/slices/By/By_{str(n_snap).zfill(5)}.png"

        quant_dict['By']['arg_dict'] = {}
        quant_dict['By']['arg_dict']['img_data'] = out_dict['B'][1]
        quant_dict['By']['arg_dict']['cmap'] = cmap
        quant_dict['By']['arg_dict']['view_dir'] = 1 

    if MHD_flag and ('Bz' or 'all' in field_list):
        quant_dict['Bz'] = {}
        quant_dict['Bz']['title'] = 'B_z'
        quant_dict['Bz']['save_loc'] = f"{sim_loc}Plots/slices/Bz/Bz_{str(n_snap).zfill(5)}.png"

        quant_dict['Bz']['arg_dict'] = {}
        quant_dict['Bz']['arg_dict']['img_data'] = out_dict['B'][2]
        quant_dict['Bz']['arg_dict']['cmap'] = cmap
        quant_dict['Bz']['arg_dict']['view_dir'] = 1 


    #* To loop over the different quantities and plot them
    for key in quant_dict:

        if n_snap==n_start:
            try:
                os.system(f"mkdir {sim_loc}Plots")
                os.system(f"mkdir {sim_loc}Plots/{save_dir}")
                os.system(f"mkdir {sim_loc}Plots/{save_dir}/{key}")
            except:
                print("Couldn't create the directory for {out_loc} ...")
                # return

        plt_dict = plot_fn(**quant_dict[key]['arg_dict'], **arg_dict)
        plt_dict['ax'].set_title(quant_dict[key]['title'])
        plt.savefig(quant_dict[key]['save_loc'])

        plt.close()
        plt.clf()
        plt.cla()
        del(plt_dict)

        gc.collect()



if __name__ == "__main__":

    rho = np.load('../data_analysis/data/rho.npy')

    style_lib  = '../plot/style_lib/' 
    # pallette   = style_lib + 'cup_pallette.mplstyle'
    # pallette   = style_lib + 'dark_pallette.mplstyle'
    pallette   = style_lib + 'bright_pallette.mplstyle'
    plot_style = style_lib + 'plot_style.mplstyle'
    text_style = style_lib + 'text.mplstyle'

    plt.style.use([pallette, plot_style, text_style])

    plot_dict = plot_slice(rho[:10,:20,:30], slice_dir=2)
    plot_dict['cbar'].set_label('Colorbar label') 
    plot_dict['ax'].set_title('plot_slice test') 
    plot_dict['ax'].set_xlabel('x label') 
    plot_dict['ax'].set_ylabel('y label') 

    plt.show()

    plot_dict = plot_projection(rho[:10,:20,:30], proj_dir=2)
    plot_dict['cbar'].set_label('Colorbar label') 
    plot_dict['ax'].set_title('plot_projection test') 
    plot_dict['ax'].set_xlabel('x label') 
    plot_dict['ax'].set_ylabel('y label') 

    plt.show()
