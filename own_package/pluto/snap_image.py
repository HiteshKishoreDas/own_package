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

sys.path.insert(0, f'{package_abs_path}plot/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}pluto/')
import plot_2d_image as p2i


#*_________________________________

# wdir_dir = "/afs/mpa/home/hitesh/remote/freya/PLUTO/TI/"
wdir_dir = "/afs/mpa/temp/hitesh/NAS"

# wdir = f"{wdir_dir}/2D_nl_parascan_MG21_R2_Chif_96/output/"
wdir = f"{wdir_dir}/2D_nl_parascan_MG21_R2/output/"

# wdir = f"{wdir_dir}/2D_nl_parascan_MG21_R4_Chif_1200/output/"

#*_________________________________


T_cut = 4e4
T_cloud = 6e4


D = dr.get_array(50, wdir, fields=['prs','rho','vel'])    

# v_r = ao.radial_vector(D['vel'])

plt.imshow(np.log10(D['rho']), vmin=-2.0, vmax=1.5)
# plt.imshow(v_r, vmin=-0.1, vmax=0.0)
plt.colorbar()


print(D['rho'].min())
print(D['rho'].max())
print(D['rho'].max()/D['rho'].min())

del(D)
gc.collect()