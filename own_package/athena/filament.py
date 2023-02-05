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
import gc
import pickle as pk

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
import coherence as ch

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_3d as pt
import video as vid 

sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
from units import KELVIN, mu

#%%
N_procs_default  = 1
file_ind_default = 0
test_array_type_default = None

n_arg = len(sys.argv)
if n_arg<=2:
    print(f"Need atleast two arguments. Only {n_arg} were provided.")
    print(f"N_procs set to default: {N_procs_default} processors...")
    print(f"file_int set to default: {file_ind_default}...")
    N_procs  = N_procs_default
    file_ind = file_ind_default

elif n_arg==3:
    N_procs  = int(sys.argv[1])
    file_ind = int(sys.argv[2])
    test_array_type = test_array_type_default
    print(f"N_procs set  : {N_procs} processors...")
    print(f"file_int set : {file_ind}...")
    print(f"test_array_type : {test_array_type}...")

elif n_arg==4:
    N_procs  = int(sys.argv[1])
    file_ind = int(sys.argv[2])
    test_array_type = sys.argv[3]
    print(f"N_procs set  : {N_procs} processors...")
    print(f"file_int set : {file_ind}...")
    print(f"test_array_type : {test_array_type}...")

else:
    print(f"Too many arguments provided...")
    print(f"N_procs set to default: {N_procs_default} processors..")
    print(f"file_int set to default: {file_ind_default}...")
    print(f"test_array_type set to: {test_array_type_default}...")
    N_procs = N_procs_default
    file_ind = file_ind_default
    test_array_type = test_array_type_default

# file_loc  = '/afs/mpa/home/hitesh/remote/cobra/athena_fork_turb_box/turb_v2/'
# file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_beta_100/'
# file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_hydro/'
# file_loc += 'para_scan_Rlsh4_2500_res0_128_rseed_1_M_0.5_chi_100_hydro/'
# file_loc += 'Turb.out2.00600.athdf'

data_dir = '/ptmp/mpa/hitesh/data/'

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


# MHD_flag = True
MHD_flag = False 

# test_array_type = None
# test_array_type = "random"
# test_array_type = "filament"

# for i_file, file_loc in enumerate(file_loc_list):

out_dict = dr.get_array_athena(file_loc_list[file_ind], fields=["rho"],MHD_flag=MHD_flag)

# rho = out_dict['rho']
T = out_dict['T']
T_cut = 4e5
T_max = T.max()
T_min = T.min()

# rho[rho<10.0] = 1.0

# prs = out_dict['P']
# T = (prs/rho) * KELVIN * mu



if test_array_type=="random":
    np.random.seed(file_ind)
    T = np.random.rand(*np.shape(T)) # Uniform random num between 0 to 1

    T = T_min + (T_max-T_min)*T # Uniform random num between T_min to T_max

elif test_array_type=="filament":
    k = 5
    L = np.shape(T)
    r = np.indices(L)
    T  = np.sin(2*np.pi * k * (file_ind+1) *r[0]/L[0])
    T += np.sin(2*np.pi * k * (file_ind+1) *r[1]/L[1])
    T += 0.1*np.sin(2*np.pi*r[2]/L[2])
    T -= T.min()
    T /= T.max()   # Filament between 0 to 1

    T = T_min + (T_max-T_min)*T  # Filament between T_min to T_max

    plt.figure()
    plt.imshow(T[:,int(L[2]/2),:])
    plt.savefig(f"filament_test_{file_ind}.png")

avg_mask = (T<np.sqrt(T.min()*T.max()))

devices = N_procs*['cpu']
parallel_flag = True
coh_list, wnd_list = ch.frac_aniso_window_variation(inp_arr=T, num=25,  \
                                                    avg_mask=avg_mask, \
                                                    parallel_flag=parallel_flag, devices=devices)

save_dict={}
save_dict['coherence'] = coh_list
save_dict['wnd_list' ] = wnd_list

if test_array_type in ["random", "filament"]:
    save_dict['inp_arr'] = T


if test_array_type=="random":
    save_loc = './save_arr/anisotropy/random_array/'
    with open(f'{save_loc}/anisotropy_filamentariness_seed_{file_ind}.pkl', 'wb') as f:
        pk.dump(save_dict, f)
elif test_array_type=="filament":
    save_loc = './save_arr/anisotropy/filament_test/'
    with open(f'{save_loc}/anisotropy_filamentariness_filament_{file_ind}.pkl', 'wb') as f:
        pk.dump(save_dict, f)
else:
    save_loc = './save_arr/anisotropy/'+sim_list[file_ind]
    with open(f'{save_loc}/anisotropy_filamentariness_{N_snap}.pkl', 'wb') as f:
        pk.dump(save_dict, f)

del(coh_list)
del(wnd_list)
del(save_dict)
gc.collect()


# plt.figure()

# plt.plot(wnd_list[0], coh_list[0], label='HD')
# # plt.plot(wnd_list[1], coh_list[1], label='MHD')

# plt.xlabel('Window (in grid cells)')
# plt.ylabel('Anisotropy')

# # plt.yscale('log')
# # plt.xscale('log')
# plt.legend()

# # plt.show()
# plt.savefig('anisotropy.png')
