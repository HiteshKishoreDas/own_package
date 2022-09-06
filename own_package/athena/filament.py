'''
@Author: Hitesh Kishore Das 
@Date: 2022-08-30 13:54:29 
'''

import matplotlib.pyplot as plt

import numpy as np
import cmasher as cmr 
# from cmasher import * 
import sys
import os

style_lib  = '../plot/style_lib/' 
pallette   = style_lib + 'cup_pallette.mplstyle'
# pallette   = style_lib + 'dark_pallette.mplstyle'
# pallette   = style_lib + 'bright_pallette.mplstyle'
plot_style = style_lib + 'plot_style.mplstyle'
text_style = style_lib + 'text.mplstyle'

plt.style.use([pallette, plot_style, text_style])

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import clump_analysis as ca
import structure_tensor as st

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt
import video as vid 

sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
from units import KELVIN, mu



file_loc  = '/afs/mpa/home/hitesh/remote/cobra/athena_fork_turb_box/turb_v2/'
file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_beta_100/'
# file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_hydro/'
# file_loc += 'para_scan_Rlsh4_2500_res0_128_rseed_1_M_0.5_chi_100_hydro/'
file_loc += 'Turb.out2.00600.athdf'

file_loc = '../../../Turb.out2.00600.athdf'

# MHD_flag = True
MHD_flag = False 

out_dict = dr.get_array(file_loc, fields=["rho"],MHD_flag=MHD_flag)

rho = out_dict['rho']
# prs = out_dict['P']

# T = (prs/rho) * KELVIN * mu

# coh = np.sum(st.coherence(rho), axis=0)


def alpha_plot(c_arr, log_flag=False):
    return pt.poly_alpha(c_arr,log_flag=log_flag, order=1,cut=5)

# fig, ax, sc  = pt.render_scatter_3d(inp_arr = coh*rho, \
#                                     alpha_fn = alpha_plot,\
#                                     cmap=cr.neon)
# fig.savefig("./coh_rho.png")

# cmap_list = cmr.get_cmap_list()
# cmap_list = ['cmr.' + cmp for cmp in cmap_list]

cmap_list = plt.colormaps()

# cmap_list = [cr.ember]

for i_cmap, cmp in enumerate(cmap_list):

    fig, ax, sc  = pt.render_scatter_3d(inp_arr = rho, \
                                        alpha_fn = alpha_plot,
                                        pnt_size = 5, \
                                        cmap=cmp)

    ax.grid(False)
    ax.set_axis_off()
    ax.set_title(cmp)

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])


    # fig.savefig(f"./cmap_comparison/rho_{i_cmap}.pdf", format='pdf', dpi=300)
    fig.savefig(f"./cmap_comparison/rho_{i_cmap}.png", format='png', dpi=300)

