'''
@Author: Hitesh Kishore Das 
@Date: 2022-09-09 13:33:23 
'''
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt

import numpy as np
import cmasher as cr 
import sys
import gc
import os


cwd = os.path.dirname(__file__)
tail_cut = len(cwd.split('/')[-1])+len(cwd.split('/')[-2])+1
package_abs_path = cwd[:-tail_cut]

sys.path.insert(0, f'{package_abs_path}data_analysis/')
import array_operations as ao

sys.path.insert(0, f'{package_abs_path}plot/')
import plot_2d_image as p2i
import video as vd

sys.path.insert(0, f'{package_abs_path}athena/')
import data_read as dr

sys.path.insert(0, f'{package_abs_path}athena/figure_scripts/')
import sim_info as si

sys.path.insert(0, f'{package_abs_path}utils/')
import v_turb as vt
import units as un

# style_lib  = f'{package_abs_path}plot/style_lib/' 
# # pallette   = style_lib + 'dark_pallette.mplstyle'
# pallette   = style_lib + 'bright_pallette.mplstyle'
# plot_style = style_lib + 'plot_style.mplstyle'
# text_style = style_lib + 'text.mplstyle'

# plt.style.use([pallette, plot_style, text_style])


plot_field = 'rho'
plot_range = [0.0, 0.02]

cs = vt.cs_calc(4e6, un.mu)

for L_i in range(7,9):

    dir_loc = '/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/mixing_layer_brent/'
    dir_loc += f'mix_L{L_i}_Ma0_Bnot_hydro_moving/'

    print(f" Analysing files in {dir_loc} ... ")

    try:
        os.system(f'mkdir ../plots/Slices/L{L_i}')
        os.system(f'mkdir ../plots/Slices/L{L_i}/{plot_field}')
    except:
        print("Failed to create the directory...\n")

    for N in range(101):
        file_loc = dir_loc + f'Turb.out2.{str(N).zfill(5)}.athdf'

        MHD_flag = False 

        try:
            out_dict = dr.get_array_athena(file_loc, fields=[plot_field])
        except:
            print(f'Reached the end at {N = } .... \n')
            break

        plt_dict = p2i.plot_slice(out_dict[plot_field], color_range=plot_range, cmap='plasma')
        plt_dict['ax'].set_title(f"t/t_KH = {out_dict['time']/si.t_KH[L_i]: .2f}")

        plt_dict['fig'].savefig(f'../plots/Slices/L{L_i}/{plot_field}/{plot_field}_{N}.png')

        print('Plot saved ......... \n')

        del out_dict
        del plt_dict
        gc.collect()


    