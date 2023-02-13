
'''
Created Date: 2023-02-07 10:26:22
Author: Hitesh Kishore Das

'''

import matplotlib.pyplot as plt

import numpy as np
import cmasher as cmr 
import sys
import os
import gc
import pickle as pk

cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import clump_analysis as ca

sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
from units import KELVIN, mu

# data_dir = '/ptmp/mpa/hitesh/data/'
data_dir = '/afs/mpa/home/hitesh/remote/freya/data/'
save_dir = './save_arr/clump_size'

sim_list  = []

sim_list += ['Rlsh_1000_res_256_M_0.5_hydro/']
sim_list += ['Rlsh_1000_res_256_M_0.5_beta_100/']

sim_list += ['Rlsh_250_res_256_M_0.5_hydro/']
sim_list += ['Rlsh_250_res_256_M_0.5_beta_100/']

sim_list += ['Rlsh_250_res_256_M_0.25_hydro/']
sim_list += ['Rlsh_250_res_256_M_0.25_beta_100/']

N_sim = len(sim_list)
file_loc_list = N_sim*[data_dir]

N_snap = 600
file_name = f'Turb.out2.{str(N_snap).zfill(5)}.athdf'

for i in range(N_sim):
    file_loc_list[i] += sim_list[i] + file_name


MHD_flag = False 

file_ind = 0
out_dict = dr.get_array_athena(file_loc_list[file_ind], fields=["T"],MHD_flag=MHD_flag)

T = out_dict['T']
T_max = T.max()
T_min = T.min()
T_cut = 2*4e4#T_min

print(T_min)

# T_plot = np.copy(T)
# T_plot[T>T_cut] = 0

# plt.figure()
# plt.imshow(np.average(T_plot, axis=0))