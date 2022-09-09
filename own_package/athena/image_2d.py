'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-09 13:33:23 
'''
import matplotlib
# matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np
import cmasher as cr 
import sys
import gc
import os


cwd = os.path.dirname(__file__)
package_abs_path = cwd[:-len(cwd.split('/')[-1])]

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_2d_image as p2i
import video as vid 

sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}utils/')
from timer import timer 
import units as un
from v_turb import cs_calc


file_loc  = '/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/mixing_layer_brent/'
file_loc += 'mix_L0_Ma0_Bnot_hydro_moving/'
dir_loc   = file_loc
# file_loc += 'Turbulence/para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_beta_100/'
# file_loc += 'para_scan_Rlsh5_1000_res0_256_rseed_1_M_0.5_chi_100_hydro/'
# file_loc += 'para_scan_Rlsh4_2500_res0_128_rseed_1_M_0.5_chi_100_hydro/'

MHD_flag = False 

# for i in range(50,51):

    # file_loc_i = file_loc + f'Turb.out2.{str(i).zfill(5)}.athdf'

    # out_dict = dr.get_array(file_loc_i, fields=['rho'],MHD_flag=MHD_flag)

    # rho = out_dict['rho']
    # vel = out_dict['vel']
    # prs = out_dict['P']
    # T = (prs/rho) * KELVIN * mu

    # fig, ax, slc, cb = p2i.plot_slice(rho, slice_dir=1)
    # plt.savefig(f'{dir_loc}/Plots/rho/rho_{str(i).zfill(5)}.png')

    # plt.close()
    # plt.cla()
    # plt.clf()

    # del(rho)
    # gc.collect()

    # print(i)


vid.make_video(image_path=f'{dir_loc}Plots/rho/rho', video_path=f'{dir_loc}Plots/rho/rho')