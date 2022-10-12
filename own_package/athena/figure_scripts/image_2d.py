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


dir_loc = '/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/mixing_layer_shift/'
# dir_loc = '/home/hitesh/remote/mpa/remote/freya/athena_fork_turb_box/mixing_layer_shift/'
# dir_loc += f'mix_L4_Ma0_Bnot_hydro_moving_wshift/'
# dir_loc += f'mix_L4_Ma0_Bnot_hydro_moving/'
# dir_loc += f'mix_L2_Ma0_Bnot_hydro_moving/'

# dir_loc += f'mix_L0_Ma0_B0_moving/'

dir_loc1 = dir_loc + f'Trial_1_half_shift/mix_L0_Ma0_B0_moving/'
# dir_loc1 = dir_loc + f'mix_L0_Ma0_B0_moving/'
# dir_loc1 = dir_loc + f'Trial_1_half_shift/mix_L0_Ma0_Bnot_hydro_moving/'
# dir_loc2 = dir_loc + f'mix_L0_Ma0_B0_moving_2/'
# dir_loc3 = dir_loc + f'mix_L0_Ma0_B0_moving_3/'
# dir_loc4 = dir_loc + f'mix_L0_Ma0_B0_moving_4_no_shift/'
# dir_loc5 = dir_loc + f'mix_L0_Ma0_B0_moving/'

print(f" Analysing files in {dir_loc} ... ")

N = 170
# N = 0

file_loc = dir_loc1 + f'Turb.out2.{str(N).zfill(5)}.athdf'
# file_loc = dir_loc2 + f'Turb.out2.{str(N).zfill(5)}.athdf'
# file_loc = dir_loc3 + f'Turb.out2.{str(N).zfill(5)}.athdf'
# file_loc = dir_loc4 + f'Turb.out2.{str(N).zfill(5)}.athdf'
# file_loc = dir_loc5 + f'Turb.out2.{str(N).zfill(5)}.athdf'

# MHD_flag = False 
MHD_flag = True

# plot_range = [0.0, 10.0]

out_dict = dr.get_array_athena(file_loc, fields=['rho', 'prs', 'vel', 'B'], MHD_flag=MHD_flag)
# out_dict2 = dr.get_array_athena(file_loc2, fields=['rho', 'prs', 'vel'], MHD_flag=MHD_flag)

T = (out_dict['prs']/out_dict['rho']) * un.KELVIN * un.mu

plt_dict = p2i.plot_slice(np.log10(out_dict['rho']), slice_dir =1, color_range=[-5,-1], cmap='plasma')
plt_dict['ax'].set_title('Log_10 Density')
plt.show()

plt_dict = p2i.plot_slice( out_dict['prs'] , slice_dir =1, cmap='plasma')
plt_dict['ax'].set_title('Pressure')
plt.show()

plt_dict = p2i.plot_slice(np.log10(T), slice_dir =1, color_range=[np.log10(4e4), np.log10(1e7)], cmap='plasma')
# plt_dict = p2i.plot_slice(np.log10(T), slice_dir =1, cmap='plasma')
plt_dict['ax'].set_title('log_10 T')
plt.show()

plt_dict = p2i.plot_slice(T, slice_dir =1, color_range=[4e4, 4e6], cmap='plasma')
plt_dict['ax'].set_title('T')
plt.show()

# plt_dict = p2i.plot_slice(out_dict['vel'][2], slice_dir =1, cmap='plasma')
plt_dict = p2i.plot_slice(out_dict['vel'][2] - np.average(out_dict['vel'][2]), slice_dir =1, cmap='bwr')
plt_dict['ax'].set_title('v_z')
plt.show()

# plt_dict = p2i.plot_slice(out_dict['vel'][1], slice_dir =1, cmap='plasma')
# plt_dict['ax'].set_title('v_y')
# plt.show()

plt_dict = p2i.plot_slice(ao.magnitude(out_dict['vel']), slice_dir =1, cmap='plasma')
plt_dict['ax'].set_title('|v|')
plt.show()

plt_dict = p2i.plot_slice(out_dict['B'][1], slice_dir =1, cmap='plasma')
plt_dict['ax'].set_title('B')
plt.show()

# plt_dict = p2i.plot_slice(out_dict['rho'] -  out_dict2['rho'], slice_dir =1, cmap='bwr')
# plt_dict = p2i.plot_slice(out_dict['vel'][2] -  out_dict2['vel'][2], slice_dir =1, \
#            color_range=[-0.0001, 0.0001] ,cmap='bwr')
# plt_dict['ax'].set_title('Diff')
# plt.show()

print('____________________________________________')
print('Time             : ', out_dict['time'])
print('____________________________________________')
print('Density min : ', out_dict['rho'].min())
print('Density max : ', out_dict['rho'].max())
print('____________________________________________')
print('Pressure min     : ', out_dict['prs'].min())
print('Pressure max     : ', out_dict['prs'].max())
print('____________________________________________')
print('Temp min         : ', T.min())
print('Temp max         : ', T.max())
print('____________________________________________')
print('v_z min         : ', out_dict['vel'][2].min())
print('v_z max         : ', out_dict['vel'][2].max())
print('____________________________________________')
print('Average v_z      : ', np.average(out_dict['vel'][2]))
print('____________________________________________')

# plt_dict = p2i.plot_slice(out_dict['vel'][2], slice_dir =1, cmap='plasma')
# plt.show()

# plt_dict['ax'].set_title(f"t/t_KH = {out_dict['time']/si.t_KH[L_i]: .2f}")


# plot_field='rho'
# B_list = ['hydro', 'B_x', 'B_y', 'B_z']
# plot_range = [None, None]

# for L_i in range(1,10,2):
#     for B_flag in [False]:
#         for k in range(3):

#             dir_loc = '/afs/mpa/home/hitesh/remote/freya/athena_fork_turb_box/mixing_layer_brent/'
            
#             if (not B_flag) and k==0:
#                 dir_loc += f'mix_L{L_i}_Ma0_Bnot_hydro_moving/'
#                 B_k = 0
#             elif (not B_flag) and k!=0:
#                 break
#             else:
#                 B_k = k+1
#                 dir_loc += f'mix_L{L_i}_Ma0_B{k}_moving/'

#             print(f" Analysing files in {dir_loc} ... ")

#             try:
#                 os.system(f'mkdir ../plots/Slices/L{L_i}_{B_list[B_k]}')
#                 os.system(f'mkdir ../plots/Slices/L{L_i}_{B_list[B_k]}/{plot_field}')
#             except:
#                 print("Failed to create the directory...\n")

#             for N in range(201):
#                 file_loc = dir_loc + f'Turb.out2.{str(N).zfill(5)}.athdf'

#                 MHD_flag = False 

#                 try:
#                     out_dict = dr.get_array_athena(file_loc, fields=[plot_field])
#                 except:
#                     print(f'Reached the end at {N = } .... \n')
#                     break

#                 plt_dict = p2i.plot_slice(np.log10(out_dict[plot_field]), slice_dir = 1, color_range=plot_range, cmap='plasma')
#                 plt_dict['ax'].set_title(f"t/t_KH = {out_dict['time']/si.t_KH[L_i]: .2f}")

#                 plt_dict['fig'].savefig(f'../plots/Slices/L{L_i}_{B_list[B_k]}/{plot_field}/{plot_field}_{N}.png')

#                 print('Plot saved ......... \n')

#                 del out_dict
#                 del plt_dict
#                 gc.collect()


    
