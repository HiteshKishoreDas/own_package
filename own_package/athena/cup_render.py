'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-07 16:40:50 
'''

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np
import cmasher as cmr 
# from cmasher import * 
import sys
import os
import gc

style_lib  = '../plot/style_lib/' 
pallette   = style_lib + 'cup_pallette.mplstyle'
# pallette   = style_lib + 'dark_pallette.mplstyle'
# pallette   = style_lib + 'bright_pallette.mplstyle'
plot_style = style_lib + 'plot_style.mplstyle'
text_style = style_lib + 'text.mplstyle'

plt.style.use([pallette, plot_style, text_style])

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt
import video as vid 

sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
from units import KELVIN, mu


# file_loc  = '/afs/mpa/home/hitesh/remote/cobra/athena_fork_turb_box/turb_v2/'
# file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_beta_100/'
# file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_hydro/'
# file_loc += 'para_scan_Rlsh4_2500_res0_128_rseed_1_M_0.5_chi_100_hydro/'
# file_loc += 'Turb.out2.00600.athdf'

file_loc1 = '../../../Turb.hydro.out2.00600.athdf'
file_loc2 = '../../../Turb.mhd.out2.00600.athdf'

def alpha_plot(c_arr, log_flag=False):
    return pt.poly_alpha(c_arr,log_flag=log_flag, order=1,cut=5, alpha0=0.75)

def alpha_plot_smooth1(c_arr, log_flag=False):
    return pt.poly_alpha(c_arr,log_flag=log_flag, order=1,cut=5, alpha0=0.6)
def alpha_plot_smooth2(c_arr, log_flag=False):
    return pt.poly_alpha(c_arr,log_flag=log_flag, order=1,cut=5, alpha0=0.4)
def alpha_plot_smooth3(c_arr, log_flag=False):
    return pt.poly_alpha(c_arr,log_flag=log_flag, order=1,cut=5, alpha0=0.2)

def alpha_plot_T(c_arr, log_flag=False):
    return pt.poly_alpha(c_arr,log_flag=log_flag, order=1,cut=8e4, cut_above=True)

# fig, ax, sc  = pt.render_scatter_3d(inp_arr = coh*rho, \
#                                     alpha_fn = alpha_plot,\
#                                     cmap=cmr.neon)
# fig.savefig("./coh_rho.png")

# # MHD_flag = True
MHD_flag = False 
MHD_label = ['HD', 'MHD']
cmp = 'gist_rainbow'

for i_fl, file_loc in enumerate([file_loc1, file_loc2]):

    out_dict = dr.get_array(file_loc, fields=['rho','prs'],MHD_flag=MHD_flag)

    rho = out_dict['rho']
    prs = out_dict['prs']

    T = (prs/rho) * KELVIN * mu

    del(prs)
    del(out_dict)

    gc.collect()

    #*_______________________________________________________

    if True:
        fig, ax, sc  = pt.render_scatter_3d(inp_arr = rho, \
                                            alpha_fn = alpha_plot,
                                            pnt_size = 1, \
                                            cmap=cmp)

        fig, ax, sc  = pt.render_scatter_3d(inp_arr = rho, \
                                            alpha_fn = alpha_plot_smooth1,
                                            pnt_size = 2, \
                                            cmap=cmp, new_fig=False,   \
                                            ax=ax, fig=fig)

        fig, ax, sc  = pt.render_scatter_3d(inp_arr = rho, \
                                            alpha_fn = alpha_plot_smooth2,
                                            pnt_size = 3, \
                                            cmap=cmp, new_fig=False,   \
                                            ax=ax, fig=fig)
                                            
        fig, ax, sc  = pt.render_scatter_3d(inp_arr = rho, \
                                            alpha_fn = alpha_plot_smooth3,
                                            pnt_size = 4, \
                                            cmap=cmp, new_fig=False,   \
                                            ax=ax, fig=fig)

        ax.grid(False)
        ax.set_axis_off()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        ax.set_title(MHD_label[i_fl])

        fig.savefig(f"./rho_smooth_{MHD_label[i_fl]}_{cmp}.png", format='png', dpi=2000)

        plt.close()
        plt.clf()
        plt.cla()
        try:
            del(fig)
            del(ax)
            del(sc)
        except:
            pass

    del(rho)

    gc.collect()

    #*_______________________________________________________

    if False:
        fig, ax, sc  = pt.render_scatter_3d(inp_arr = T, \
                                            alpha_fn = alpha_plot_T,
                                            pnt_size = 2, \
                                            cmap=cmp)

        ax.grid(False)
        ax.set_axis_off()
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

        ax.set_title(MHD_label[i_fl])

        fig.savefig(f"./T_{MHD_label[i_fl]}_{cmp}.png", format='png', dpi=200)

        plt.close()
        plt.clf()
        plt.cla()
        try:
            del(fig)
            del(ax)
            del(sc)
        except:
            pass

    del(T)

    gc.collect()

    #*_______________________________________________________
    