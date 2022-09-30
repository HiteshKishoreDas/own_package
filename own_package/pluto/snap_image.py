'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-21 13:54:57 
'''

import numpy as np
import pickle as pk
import os
import sys
import gc

import matplotlib.pyplot as plt

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import array_operations as ao
import clump_analysis as ca

sys.path.insert(0, f'{package_abs_path}plot/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}pluto/')
import plot_2d_image as p2i

sys.path.insert(0, f'{package_abs_path}utils/')
import units as un

#*_________________________________

# wdir_dir = "/afs/mpa/home/hitesh/remote/freya/PLUTO/TI/"
wdir_dir = "/afs/mpa/temp/hitesh/NAS"

# wdir = f"{wdir_dir}/2D_nl_parascan_MG21_R2_Chif_96/output/"
wdir = f"{wdir_dir}/2D_nl_parascan_MG21_R4/output/"

# wdir = f"{wdir_dir}/2D_nl_parascan_MG21_R4_Chif_1200/output/"

#*_________________________________


T_cut = 4e4
T_cloud = 6e4


D = dr.get_array(8, wdir, fields=['prs','rho', 'vel'])    

T = (D['prs']/D['rho']) * un.KELVIN * un.mu
v_r = ao.radial_vector(D['vel'])


#%%

plt.figure()
plt.imshow(np.log10(D['rho']))
plt.colorbar()


plt.figure()
plt.imshow(v_r, vmin=-0.1, vmax=0.1, cmap='bwr')
plt.colorbar()

n_blob, label_arr = ca.clump_finder_scipy(T, 1e6)

print(f'{n_blob=}')

# del(D)
# gc.collect()
# %%
