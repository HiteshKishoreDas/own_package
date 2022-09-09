'''
@Author: Hitesh Kishore Das 
@Date: 2022-08-30 13:54:29 
'''

#%%

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np
import cmasher as cmr 
# from cmasher import * 
import sys
import os

style_lib  = '../plot/style_lib/' 
# pallette   = style_lib + 'cup_pallette.mplstyle'
pallette   = style_lib + 'dark_pallette.mplstyle'
# pallette   = style_lib + 'bright_pallette.mplstyle'
plot_style = style_lib + 'plot_style.mplstyle'
text_style = style_lib + 'text.mplstyle'

plt.style.use([pallette, plot_style, text_style])

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import clump_analysis as ca
import structure_tensor_own as st

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt
import video as vid 

sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
from units import KELVIN, mu

#%%

# file_loc  = '/afs/mpa/home/hitesh/remote/cobra/athena_fork_turb_box/turb_v2/'
# file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_beta_100/'
# file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_hydro/'
# file_loc += 'para_scan_Rlsh4_2500_res0_128_rseed_1_M_0.5_chi_100_hydro/'
# file_loc += 'Turb.out2.00600.athdf'

file_loc1 = '../../../Turb.hydro.out2.00600.athdf'
file_loc2 = '../../../Turb.mhd.out2.00600.athdf'


MHD_flag = True
MHD_flag = False 

wnd_list = []
coh_list = []

for file_loc in [file_loc1, file_loc2]:

    out_dict = dr.get_array(file_loc, fields=["rho"],MHD_flag=MHD_flag)

    rho = out_dict['rho']
    # prs = out_dict['P']

    # T = (prs/rho) * KELVIN * mu

    coh_list_i = []
    wnd_list_i = []

    L = np.array(np.shape(rho))

    for wnd in np.linspace(1.5,50.5, num=25):
        # coh_avg = np.sum(st.coherence(rho, window=wnd))/np.product(L)
        coh_avg = np.sum(st.fractional_anisotropy(rho, window=wnd))/np.product(L)

        print(f'coh_avg: {coh_avg}')
        print(f'wnd    : {wnd}')

        coh_list_i.append(coh_avg)
        wnd_list_i.append(wnd)
        
    wnd_list.append(wnd_list_i)
    coh_list.append(coh_list_i)

#%% 
plt.figure()

plt.plot(wnd_list[0], coh_list[0], label='HD')
plt.plot(wnd_list[1], coh_list[1], label='MHD')

plt.xlabel('Window (in grid cells)')
plt.ylabel('Anisotropy')

# plt.yscale('log')
# plt.xscale('log')
plt.legend()

plt.savefig('anisotropy.png')


# %%
